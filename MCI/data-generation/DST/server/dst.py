import random
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import uvicorn

data_dict = {}
questions = {}
app = FastAPI(title="DST Server")


class SlotItem(BaseModel):
    start: int
    end: int
    text: str
    label: str
    score: float


class IntentItem(BaseModel):
    label: str
    score: float


class UserRequest(BaseModel):
    intent: IntentItem
    slots: list[SlotItem]


def data_up():
    global data_dict
    global questions
    if len(questions) == 0 and len(data_dict) == 0:
        # print('Data Loading started...')
        # #################################################################################################
        # LOADING ONTHOLOGY
        # Load the Excel file into a DataFrame
        filename = 'onthology'
        excel_file_path_data = './' + filename + '.xlsx'
        dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

        for index, row in dfd.iterrows():

            intent = row['intent']
            slot1 = row['slot1']
            m1 = row['1-mandatory']
            slot2 = row['slot2']
            m2 = row['2-mandatory']
            slot3 = row['slot3']
            m3 = row['3-mandatory']
            slot4 = row['slot4']
            m4 = row['4-mandatory']
            if intent not in data_dict:
                data_dict[intent] = {'slots': []}

            if intent in data_dict:
                if m1 == 1:
                    data_dict[intent]['slots'].append(slot1)
                if m2 == 1:
                    data_dict[intent]['slots'].append(slot2)
                if m3 == 1:
                    data_dict[intent]['slots'].append(slot3)

        # # #################################################################################################
        # LOADING questions
        # Load the Excel file into a DataFrame
        filename = 'questions'
        excel_file_path_data = './' + filename + '.xlsx'
        dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

        for index, row in dfd.iterrows():
            question = row['question']
            slot = row['slot']
            if slot not in questions:
                questions[slot] = []
            questions[slot].append(question)


def dst(intent, slots_dict):
    global data_dict
    global questions
    data_up()
    # print('DST started...')
    # Initialize the status and context variables
    m = 0
    n = 0
    not_found = []
    belief_state = f'Belief State - {intent} :  '
    # Check if the intent is in data_dict before accessing its slots
    if intent in data_dict:
        m_slots = data_dict[intent]['slots']
        n = len(data_dict[intent]['slots'])
        for slot in m_slots:
            belief_state = belief_state + f'{slot} = '
            if slot in slots_dict:
                # print(f'{slot} is founded')
                belief_state = belief_state + f'{slots_dict[slot]}  '
                # print(belief_state)
                m = m + 1
            else:
                not_found.append(slot)
                # print(f'{slot} is not founded')
                belief_state = belief_state + f'not found   '
                # print(belief_state)

        # print(f'm={m} , n={n}')
    else:
        print(f"Intent '{intent}' not found in data_dict")
    # Update status and context if intent is not found
    context = ''
    status = ''
    if n == m:
        status = 'completed'
        context = ''
    else:
        status = 'not-completed'
        random_slot = random.choice(not_found)
        # print(f'not found : {not_found}')
        q = random.choice(questions[random_slot])
        # print(f'Choosen q: {q}')
        context = q

    print(belief_state)
    # Return the JSON object
    result = {'status': status, 'context': context}
    return result


def process_user_request(request: UserRequest):
    intent_label = request.intent.label.lower()
    slots_dict = {slot.label.lower(): slot.text for slot in request.slots}

    # Perform your processing logic here
    # print(f"Intent: {intent_label}")
    # print("Slots:")
    # for label, text in slots_dict.items():
    #     print(f"  {label}: {text}")
    response_data = dst(intent_label, slots_dict)
    return response_data


@app.post("/process_request")
async def process_request(request: UserRequest):
    return process_user_request(request)


if __name__ == "__main__":
    uvicorn.run("dst:app", host="localhost", port=8000, reload=True)
