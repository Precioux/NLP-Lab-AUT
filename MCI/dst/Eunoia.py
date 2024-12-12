import pandas as pd
from DST.db.states.funcs import *
import requests
import json

# Define URLs for the servers
url_NLU = "http://localhost:8092/predict"
url_confirmation = "http://localhost:8000/check_intent/"
url_DST = "http://localhost:8080/process_request"


def send_NLU(data, turn):
    global url_NLU
    params = {'conversation': data, 'turn': turn}
    response = requests.get(url_NLU, params=params)
    return response


def send_confirmation(data):
    global url_confirmation
    response = requests.post(url_confirmation, json=data)
    return response


def send_DST(data):
    global url_DST
    response = requests.post(url_DST, json=data)
    return response


def conversation_ID_generator():
    print('generating ID')
    id = ''
    if is_table_empty('states'):
        id = '0000'
    else:
        vid = get_latest_conversation_id()
        n = int(vid)
        nid = n + 1
        if nid < 10:
            id = '000' + str(nid)
        elif nid < 100:
            id = '00' + str(nid)
        elif nid < 1000:
            id = '0' + str(nid)
        else:
            id = str(nid)

    return id


conversation_schedule1 = []
conversation_schedule2 = []


def data_up():
    # Load ontology
    filename_ontology = 'Ontology'
    excel_file_path_data_ontology = './' + filename_ontology + '.xlsx'
    dfo = pd.read_excel(excel_file_path_data_ontology, engine='openpyxl')
    data_dict = {}

    for index, row in dfo.iterrows():
        intent = row['intent']
        if intent not in data_dict:
            data_dict[intent] = {}
            data_dict[intent]['slots'] = {}
            data_dict[intent]['slots']['mandatory'] = []
            data_dict[intent]['slots']['optional'] = []
        slot1 = row['Slot 1']
        m1 = row['1-mandatory']
        def1 = row['1-default']
        slot2 = row['Slot 2']
        m2 = row['2-mandatory']
        def2 = row['2-default']
        slot3 = row['Slot 3']
        m3 = row['3-mandatory']
        def3 = row['3-default']
        slot4 = row['Slot 4']
        m4 = row['4-mandatory']
        def4 = row['4-default']
        if intent in data_dict:
            if m1 == 1:
                data_dict[intent]['slots']['mandatory'].append(slot1)
            elif slot1 != 0:
                data_dict[intent]['slots']['optional'].append(slot1)
            if m2 == 1:
                data_dict[intent]['slots']['mandatory'].append(slot2)
            elif slot2 != 0:
                data_dict[intent]['slots']['optional'].append(slot2)
            if m3 == 1:
                data_dict[intent]['slots']['mandatory'].append(slot3)
            elif slot3 != 0:
                data_dict[intent]['slots']['optional'].append(slot3)
            if m4 == 1:
                data_dict[intent]['slots']['mandatory'].append(slot4)
            elif slot4 != 0:
                data_dict[intent]['slots']['optional'].append(slot4)


def get_eunoia(text, cid):
    if cid == '0':
        cid = conversation_ID_generator()
    conversation_schedule1.append(text)
    conversation_schedule2.append(text)
    str_conversation_schedule1 = ' '.join(conversation_schedule1)
    str_conversation_schedule2 = ' '.join(conversation_schedule2)
    print(f'Sending to NLU:')
    print("------------------------------------------------------")
    print(f'schedule1: {str_conversation_schedule1}')
    result_NLU = send_NLU(str_conversation_schedule1, text)
    print("------------------------------------------------------")
    print('This is NLU Result')
    print("------------------------------------------------------")
    result_NLU_json = result_NLU.json()
    # print(json.dumps(result_NLU_json, indent=4, ensure_ascii=False))
    print(f'Slots: {result_NLU_json["conversation"]["slots"]}')
    result_confirmation = (send_confirmation(result_NLU_json)).json()
    print("=================================================================")
    print('This is confirmation result')
    print("------------------------------------------------------")
    print(result_confirmation)
    confirmed_intent = result_confirmation.get('intent1')
    confirmation_status = result_confirmation.get('status')
    # Add conversation_id to result_NLU_json
    result_NLU_json['conversation_id'] = cid
    dst_status = None
    dst_context = None
    dst_intent = None
    if confirmation_status == 'confirmed':
        result_DST = send_DST(result_NLU_json).json()
        print("=================================================================")
        print('This is DST')
        print(json.dumps(result_DST, indent=4, ensure_ascii=False))
        print("=================================================================")
        dst_status = result_DST.get('status')
        dst_context = result_DST.get('context')
        dst_intent = result_DST.get('intent')
        # if 'question' in dst_context:
        #     conversation_schedule2.append(dst_context['question'])
    return  dst_status,dst_context, cid


if __name__ == "__main__":
    data_up()
    flag = True
    print('Hi, This is Eunoia! How can I help you?   X for stop')
    while flag:
        user_input = input('Enter your request:')
        if user_input != 'X':
            status,answer,cid = get_eunoia(user_input, '0')
            print(status)
            print(answer)
            if status == 'not-completed':
                user_continue = input('Tell me: ')
                status, answer, cid = get_eunoia(user_continue, cid)
                print(answer)
            elif status == 'completed':
                conversation_schedule1.clear()
                conversation_schedule2.clear()
        else:
            print('See you next time!')
            flag = False



