from transformers import AutoModelForSequenceClassification, AutoModel, AutoConfig
from transformers import AutoTokenizer
from transformers import logging
logging.set_verbosity_error()

import torch
import torch.nn as nn
import numpy as np
import json

class JointIntentAndSlotFillingModel(nn.Module):
    def __init__(self, bert, config, intent_labels_num, slot_labels_num):
        super(JointIntentAndSlotFillingModel,self).__init__()
        self.bert = bert
        self.fc1 = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(0.1)
        self.intent_classifier = nn.Linear(config.hidden_size, intent_labels_num)
        self.fc2 = nn.Linear(config.hidden_size, config.hidden_size)
        self.slot_classifier = nn.Linear(config.hidden_size, slot_labels_num)

    # @amp.autocast()
    def forward(self, input_ids, attention_mask):
        # two outputs from BERT
        outputs = self.bert(input_ids, attention_mask)
        
        cls_token = outputs[1]
        dense_for_intent = self.fc1(cls_token)
        intent_logits = self.intent_classifier(self.dropout(dense_for_intent))
 
        last_hidden_state = outputs[0]                          
        dense_for_slot = self.fc2(last_hidden_state)
        slot_logits = self.slot_classifier(self.dropout(dense_for_slot))
        
        return intent_logits, slot_logits

class NLUModel():
    def __init__(self):
        self._load_label2ids()
        self._load_model()
    
    def _load_label2ids(self):
        with open("/home/ubuntu/NLU/API-Run/data/intent_label2id.json") as f:
            self.intent_label2id = json.load(f)
            
        self.intent_id2label = dict([(v,k) for k,v in self.intent_label2id.items()])


        with open("/home/ubuntu/NLU/API-Run/data/slot_label2id.json") as f:
            self.slot_label2id = json.load(f)
        
        self.slot_id2label = dict([(y,x) for x,y in self.slot_label2id.items()])

    def _load_model(self):
        # Load model directly
        # from transformers import AutoTokenizer, AutoModelForMaskedLM

        # tokenizer = AutoTokenizer.from_pretrained("FacebookAI/xlm-roberta-large")
        # model = AutoModelForMaskedLM.from_pretrained("FacebookAI/xlm-roberta-large")
        
        
        model_name = "xlm-roberta-large"
        # model_name = "FacebookAI/xlm-roberta-large"
        
        config = AutoConfig.from_pretrained(model_name)
        bert = AutoModel.from_pretrained(model_name,output_hidden_states=True) 
                
        # pass the pre-trained BERT to our define architecture
        self.model = JointIntentAndSlotFillingModel(bert, config,
                                                    intent_labels_num=len(self.intent_label2id),
                                                    slot_labels_num=len(self.slot_label2id))

        # push the model to GPU
        self.model = self.model.to('cpu')
        
        path = '/home/ubuntu/NLU/models/nlu_xlmlarge_14030513_multiturn_formatB.pt'
        self.model.load_state_dict(torch.load(path, map_location='cpu'))
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def inference(self, text):
        text = ' '.join(text.split())
        MAX_SEQ_LEN = 64

        tokenized_inputs = self.tokenizer(text.split(),
                                          truncation=True, padding="max_length", max_length=MAX_SEQ_LEN,
                                          is_split_into_words=True, return_token_type_ids=False,
                                          return_tensors='pt').to('cpu')

        with torch.no_grad():
            intent_logits, slot_prob = self.model(tokenized_inputs['input_ids'], tokenized_inputs['attention_mask'])

        # Top 10 intents
        intent_scores, intent_indices = torch.topk(intent_logits, 10)

        # Calculate softmax scores
        softmax = nn.Softmax(dim=1)(intent_logits)
        softmax_scores, _ = torch.topk(softmax, 10)

        # Calculate min-max normalization on logits
        min_score = torch.min(intent_scores)
        max_score = torch.max(intent_scores)
        range_score = max_score - min_score
        normalized_scores = (intent_scores - min_score) / range_score if range_score != 0 else torch.zeros_like(intent_scores)

        # Simple normalization between top 10 intents using logits
        total_score_sum = torch.sum(intent_scores)
        simple_normalized_scores = intent_scores / total_score_sum if total_score_sum != 0 else torch.zeros_like(intent_scores)

        top_intents = []
        for score, softmax_score, norm_score, simple_norm_score, idx in zip(intent_scores[0], softmax_scores[0], normalized_scores[0], simple_normalized_scores[0], intent_indices[0]):
            top_intents.append({
                "label": self.intent_id2label[idx.item()],
                "logit_score": f"{score.item()}",
                "softmax_score": f"{softmax_score.item()}",
                "min_max_normalized_score": f"{norm_score.item()}",
                "simple_normalized_score": f"{simple_norm_score.item()}"
            })

        best_intent = top_intents[0]

        slot_pred = np.argmax(slot_prob.detach().cpu().numpy(), axis=2)[0]
        all_slot_scores = torch.max(nn.Softmax(dim=2)(torch.tensor(slot_prob)), axis=2)[0].detach()[0]

        word_ids = tokenized_inputs.word_ids()

        previous_word_id = None
        slot_labels = []
        slot_scores = []
        slot_texts = text.split()
        for i, word_id in enumerate(word_ids):  # Set the special tokens to 0.
            if word_id is None:  # Special tokens have a word id "None". We set the label to -100 so they are automatically ignored in the loss function.
                continue
            elif word_id == previous_word_id:  # We set the label for the first token of each word.
                continue
            else:  # For the other tokens in a word, we set the label to either the current label or -100, depending on the label_all_tokens flag.
                slot_labels.append(self.slot_id2label[slot_pred[i]])
                slot_scores.append(all_slot_scores[i].item())
            previous_word_id = word_id

        slot_output_dict = []
        slot_start = 0
        slot_starts = []
        slot_ends = []
        for word in slot_texts:
            slot_starts.append(slot_start)
            slot_end = slot_start + len(word)
            slot_ends.append(slot_end)
            slot_start = slot_end + 2

        # for correcting i wihout b
        for i, slot_label in enumerate(slot_labels):
            if i < len(slot_labels) - 1:
                if slot_label == 'o' and slot_labels[i + 1][:2] == 'i-':
                    slot_labels[i + 1] = 'b-' + slot_labels[i + 1][2:]
                if (slot_labels[i + 1] != 'o') and (slot_labels[i][2:] != slot_labels[i + 1][2:]) and (
                        slot_labels[i + 1][:2] == 'i-'):
                    slot_labels[i + 1] = 'b-' + slot_labels[i + 1][2:]
        print(slot_labels)

        # delete 'o' and combined b- & i-
        b_observed = False
        for slot_label, slot_score, slot_text, slot_start, slot_end in zip(slot_labels, slot_scores, slot_texts,
                                                                           slot_starts, slot_ends):
            if b_observed and slot_label[:2] != 'i-':
                slot_output_dict.append({"start": slot_start_b, "end": slot_end_i, "text": slot_text_b,
                                         "label": slot_label_b.replace("b-", "").replace("i-", ""),
                                         "score": f"{slot_score}"})
                b_observed = False
                slot_text_b = ''
                slot_label_b = ''

            if slot_label[:2] == 'b-':
                slot_start_b = slot_start
                b_observed = True
                slot_end_i = slot_end
                slot_text_b = slot_text
                slot_label_b = slot_label
                continue
            if b_observed and slot_label[:2] == 'i-':
                slot_end_i = slot_end
                slot_text_b = slot_text_b + ' ' + slot_text
                continue
            if slot_label == 'o':
                b_observed = False
                continue

        if b_observed:
            slot_output_dict.append({"start": slot_start_b, "end": slot_end_i, "text": slot_text_b,
                                     "label": slot_label_b.replace("b-", "").replace("i-", ""),
                                     "score": f"{slot_score}"})

        return {
            "intent": best_intent,
            "top_intents": top_intents,
            "slots": slot_output_dict
        }