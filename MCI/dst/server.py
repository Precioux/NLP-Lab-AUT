from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn
import random
import langid
from typing import List
import jdatetime
from translate import *

app = FastAPI(title="DST Server")


# Define Pydantic models
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
    slots: List[SlotItem]


# Global data structures
data_dict = {}
questions = {}
defaults = {}
single_slot = []
multi_slot = []

# Definitions:
# #################################################################################################
shamsi = {"فروردین": '1', "اردیبهشت": '2', "خرداد": "3", "تیر": "4", "مرداد": '5', "شهریور": '6', "مهر": '7',
          "آبان": '8', "آذر": '9', "دی": '10', "بهمن": '11', "اسفند": '12'}
miladi_fa = {"ژانویه": '1', "فوریه": '2', "مارچ": "3", "آپریل": "4", "می": '5', "جون": '6', "جولای": '7', "اوت": '8',
             "سپتامبر": '9', "اکتبر": '10', "نوامبر": '11', "دسامبر": '12'}
miladi_eng = {"January": '1', "February": '2', "March": "3", "April": "4", "May": '5', "June": '6', "July": '7',
              "August": '8', "September": '9', "October": '10', "November": '11', "December": '12'}
ghamari = {"محرم": '1', "صفر": '2', "ربیع الاول": "3", "ربیع الثانی": "4", "جمادی الاول": '5', "جمادی الثانیه": '6',
           "رجب": '7', "شعبان": '8', "رمضان": '9', "شوال": '10', "ذیقعده": '11', "ذیحجه": '12'}
# #################################################################################################
oprand = {'plus', 'minus', 'multiply', 'divide', 'radical', 'power'}
source_unit = {'unit_volume1', 'unit_length1', 'unit_surface1', 'unit_mass1'}
dest_unit = {'unit_volume2', 'unit_length2', 'unit_surface2', 'unit_mass2'}
date_names = {'امروز', 'دیروز', 'فردا', 'پس فردا', 'پریروز', 'روز', 'فعلی', 'الان', 'صبحی', 'بروز'}
alphabet = {'الف': 'ا', 'جیم': 'ج', 'دال': 'د', 'ذال': 'ذ', 'سین': 'س', 'شین': 'ش', 'صاد': 'ص', 'ضاد': 'ض', 'عین': 'ع',
            'غین': 'غ', 'قاف': 'ق', 'کاف': 'ک', 'گاف': 'گ', 'لام': 'ل', 'میم': 'م', 'نون': 'ن', 'واو': 'و'}


# Load data from files
def data_up():
    global data_dict
    global questions
    if len(questions) == 0 and len(data_dict) == 0:
        # Load ontology
        filename = 'Onthology'
        excel_file_path_data = './' + filename + '.xlsx'
        dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

        for index, row in dfd.iterrows():
            intent = row['intent']
            n = row['num']
            if n > 1:
                multi_slot.append(intent)
            else:
                single_slot.append(intent)

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
                else:
                    data_dict[intent]['slots']['optional'].append(slot1)
                    defaults[slot1] = def1
                if m2 == 1:
                    data_dict[intent]['slots']['mandatory'].append(slot2)
                else:
                    data_dict[intent]['slots']['optional'].append(slot2)
                    defaults[slot2] = def2
                if m3 == 1:
                    data_dict[intent]['slots']['mandatory'].append(slot3)
                else:
                    data_dict[intent]['slots']['optional'].append(slot3)
                    defaults[slot3] = def3
                if m4 == 1:
                    data_dict[intent]['slots']['mandatory'].append(slot4)
                else:
                    data_dict[intent]['slots']['optional'].append(slot4)
                    defaults[slot4] = def4

        # Load questions
        filename = 'questions'
        excel_file_path_data = './' + filename + '.xlsx'
        dfd = pd.read_excel(excel_file_path_data, engine='openpyxl')

        for index, row in dfd.iterrows():
            question = row['question']
            slot = row['slot']
            if slot not in questions:
                questions[slot] = []
            questions[slot].append(question)


# text to number
def persian_text_to_int(text):
    # Create a dictionary to map Persian text numbers to their integer values
    numbers = {
        'صفر': 0,
        'یک': 1,
        'دو': 2,
        'سه': 3,
        'چهار': 4,
        'پنج': 5,
        'شش': 6,
        'هفت': 7,
        'هشت': 8,
        'نه': 9,
        'ده': 10,
        'یازده': 11,
        'دوازده': 12,
        'سیزده': 13,
        'چهارده': 14,
        'پانزده': 15,
        'شانزده': 16,
        'هفده': 17,
        'هجده': 18,
        'نوزده': 19,
        'بیست': 20,
        'سی': 30,
        'چهل': 40,
        'پنجاه': 50,
        'شصت': 60,
        'هفتاد': 70,
        'هشتاد': 80,
        'نود': 90,
        'صد': 100,
        'هزار': 1000
    }

    # Split the text into individual Persian numbers
    tokens = text.split()

    # Convert each Persian number to its integer value
    result = 0
    current_number = 0
    for token in tokens:
        if token in numbers:
            current_number += numbers[token]
        elif token == 'و':
            continue
        else:
            result += current_number * numbers['هزار']
            current_number = 0

    result += current_number
    return result


# translator
def translate_text(text, src='fa', dest='en'):
    translator = Translator(to_lang=dest, from_lang=src)
    translation = translator.translate(text)
    return translation


# convert text to date
def convert_relative_date(relative_date_text):
    today = jdatetime.date.today()
    if relative_date_text == 'امروز' or relative_date_text == 'بروز' or relative_date_text == 'روز' or relative_date_text == 'صبحی' or relative_date_text == 'الان' or relative_date_text == 'فعلی':
        return today
    elif relative_date_text == 'دیروز':
        return today - jdatetime.timedelta(days=1)
    elif relative_date_text == 'پریروز':
        return today - jdatetime.timedelta(days=2)
    elif relative_date_text == 'فردا':
        return today + jdatetime.timedelta(days=1)
    elif relative_date_text == 'پس فردا':
        return today + jdatetime.timedelta(days=2)
    else:
        return None  # Handle unrecognized relative date texts


# Language detection functions
def detect_language(text):
    lang, confidence = langid.classify(text)
    return lang


def is_persian(text):
    language = detect_language(text)
    # print(f'{text} => {language}')
    return language == 'fa'


def is_english(text):
    language = detect_language(text)
    return language == 'en'


# DST function
def dst(intent, slots_dict):
    global data_dict
    global questions
    data_up()
    m = 0
    n = 0
    not_found = []
    belief_state = f'Belief State - {intent} :  '
    if intent in data_dict:
        print('DST')
        print(f'Intent varified : {intent}')
        m_slots = data_dict[intent]['slots']['mandatory']
        n = len(data_dict[intent]['slots']['mandatory'])
        print(f'required slots: {n} {m_slots}')
        for slot in m_slots:
            print(f'checking for {slot}')
            belief_state = belief_state + f'{slot} = '
            if slot in slots_dict:
                print(f'founded! {slots_dict[slot]}')
                belief_state = belief_state + f'{slots_dict[slot]}  '
                m = m + 1
            elif slot == 'oprand':
                for s in slots_dict:
                    if s in oprand:
                        print(f'oprand founded : {s}')
                        belief_state = belief_state + f'{s}'
                        m = m + 1
            elif slot == 'source_unit':
                for s in slots_dict:
                    if s in source_unit:
                        print(f'source unit founded : {s}')
                        belief_state = belief_state + f'{s}     '
                        m = m + 1
            elif slot == 'dest_unit':
                for s in slots_dict:
                    if s in dest_unit:
                        print(f'dest unit founded : {s}')
                        belief_state = belief_state + f'{s}'
                        m = m + 1
            else:
                print(f'not founded')
                not_found.append(slot)
                belief_state = belief_state + f'not found   '

    else:
        print(f"Intent '{intent}' not found in data_dict")

    context = ''
    status = ''
    if n == m:
        status = 'completed'
        context = ''
        print(belief_state)
    else:
        status = 'not-completed'
        print(f'Asking question for {not_found[0]}')
        q = random.choice(questions[not_found[0]])
        context = q
        print(belief_state)
    # Checking intents
    # Ask for restaurant

    # Calender Convert
    # Todo 1403 year cannot be empty
    if intent == 'calender_convert':
        print('This is calender convert')
        # print(f'{slots_dict}')
        # converting source
        ans = {'source_calender': '', 'dest_calender': '', 'date': ''}
        dd = 0
        mm = 0
        yy = 0
        if slots_dict['dest_calender'] != '' and slots_dict['source_calender'] != '' and slots_dict['date'] != '':
            date = slots_dict['date'].split()
            print(date)
            if slots_dict['source_calender'] == 'شمسی' or slots_dict['source_calender'] == 'shamsi':
                print('shamsi')
                ans['source_calender'] = 'shamsi'
                for d in date:
                    if d in shamsi.keys():
                        print(f'month recognized : {shamsi[d]}')
                        mm = shamsi[d]
                        # date.remove(d)
                        # print(date)
                    else:
                        d_int = int(d)
                        print(type(d_int))
                        if 1 <= d_int <= 31 and dd == 0:
                            dd = d_int
                            print(f'day recognized : {d_int}')
                            # date.remove(d)
                            # print(date)
                        else:
                            # adding century
                            if d_int < 100:
                                yy = d_int + 1300
                            else:
                                yy = d_int
                            print(f'year recognized : {d_int}')
                            # date.remove(d)
                            # print(date)
                    print(f'{yy}-{mm}-{dd}')
                    ans['date'] = f'{yy}-{mm}-{dd}'
            if slots_dict['source_calender'] == 'میلادی' or slots_dict['source_calender'] == 'miladi':
                print('miladi')
                ans['source_calender'] = 'miladi'
                for d in date:
                    if type(d) == str and is_english(d):
                        d = d.capitalize()
                        print(d)
                    if d in miladi_fa.keys():
                        print(f'month recognized : {miladi_fa[d]}')
                        mm = miladi_fa[d]
                        # date.remove(d)
                        # print(date)
                    elif d in miladi_eng.keys():
                        print(f'month recognized : {miladi_eng[d]}')
                        mm = miladi_eng[d]
                        # date.remove(d)
                        # print(date)
                    else:
                        d_int = int(d)
                        print(type(d_int))
                        if 1 <= d_int <= 31 and dd == 0:
                            dd = d_int
                            print(f'day recognized : {d_int}')
                            # date.remove(d)
                            # print(date)
                        else:
                            # # adding century
                            # if d_int < 100:
                            #     yy = d_int + 1300
                            # else:
                            yy = d_int
                            print(f'year recognized : {d_int}')
                            # date.remove(d)
                            # print(date)
                    print(f'{yy}-{mm}-{dd}')
                    ans['date'] = f'{yy}-{mm}-{dd}'
            if slots_dict['source_calender'] == 'قمری' or slots_dict['source_calender'] == 'ghamari':
                print('ghamari')
                ans['source_calender'] = 'ghamari'
                for d in date:
                    if d in ghamari.keys():
                        print(f'month recognized : {ghamari[d]}')
                        mm = ghamari[d]
                        # date.remove(d)
                        # print(date)
                    else:
                        d_int = int(d)
                        print(type(d_int))
                        if 1 <= d_int <= 31 and dd == 0:
                            dd = d_int
                            print(f'day recognized : {d_int}')
                            # date.remove(d)
                            # print(date)
                        else:
                            yy = d_int
                            print(f'year recognized : {d_int}')
                            # date.remove(d)
                            # print(date)
                    print(f'{yy}-{mm}-{dd}')
                    ans['date'] = f'{yy}-{mm}-{dd}'
            if slots_dict['dest_calender'] == 'قمری' or slots_dict['dest_calender'] == 'ghamari':
                ans['dest_calender'] = 'ghamari'
            if slots_dict['dest_calender'] == 'شمسی' or slots_dict['dest_calender'] == 'shamsi':
                ans['dest_calender'] = 'shamsi'
            if slots_dict['dest_calender'] == 'میلادی' or slots_dict['dest_calender'] == 'miladi':
                ans['dest_calender'] = 'miladi'
            context = str(ans)

######### TIMEEEEE
    if intent == 'ask_azan':
        ans = {'city': slots_dict['city'], 'prayer_time': '', 'timestamp': str(jdatetime.date.today())}
        print(f'This is ask azan')
        if slots_dict['prayer_time'] == 'اذان صبح' or 'سحر':
            ans['prayer_time'] = 'azan_sobh'
        elif slots_dict['prayer_time'] == 'طلوع آفتاب':
            ans['prayer_time'] = 'toloe_aftab'
        elif slots_dict['prayer_time'] == 'اذان ظهر':
            ans['prayer_time'] = 'azan_zohre'
        elif slots_dict['prayer_time'] == 'غروب آفتاب':
            ans['prayer_time'] = 'ghorob_aftab'
        elif slots_dict['prayer_time'] == 'اذان مغرب' or 'افطار':
            ans['prayer_time'] = 'azan_maghreb'
        elif slots_dict['prayer_time'] == 'نیمه شب شرعی':
            ans['prayer_time'] = 'nime_shabe_sharie'
        elif slots_dict['prayer_time'] == 'اوقات شرعی':
            ans['prayer_time'] = ''

        context = str(ans)

    if intent == 'translate_it':
        print('This is Translate it')
        if slots_dict['sentence'] != '':
            ans = {'source_language': '', 'dest_language': '', 'sentence': slots_dict['sentence']}
        if is_persian(slots_dict['sentence']):
            ans['source_language'] += 'fa'
            ans['dest_language'] += 'en'
        elif is_english(slots_dict['sentence']):
            ans['source_language'] += 'en'
            ans['dest_language'] += 'fa'
        print(ans)
        context = str(ans)

    if intent == 'ask_math':
        print(f'This is ask math')
        if 'power' in slots_dict and slots_dict['num1'] != '' and slots_dict['num2'] != '':
            context = {'operand': 'power', 'num1': persian_text_to_int(slots_dict['num1']),
                       'num2': persian_text_to_int(slots_dict['num2'])}
        if 'plus' in slots_dict and slots_dict['num1'] != '' and slots_dict['num2'] != '':
            context = {'operand': 'plus', 'num1': persian_text_to_int(slots_dict['num1']),
                       'num2': persian_text_to_int(slots_dict['num2'])}
        if 'minus' in slots_dict and slots_dict['num1'] != '' and slots_dict['num2'] != '':
            context = {'operand': 'minus', 'num1': persian_text_to_int(slots_dict['num1']),
                       'num2': persian_text_to_int(slots_dict['num2'])}
        if 'divide' in slots_dict and slots_dict['num1'] != '' and slots_dict['num2'] != '':
            context = {'operand': 'divide', 'num1': persian_text_to_int(slots_dict['num1']),
                       'num2': persian_text_to_int(slots_dict['num2'])}
        if 'multiply' in slots_dict and slots_dict['num1'] != '' and slots_dict['num2'] != '':
            context = {'operand': 'multiply', 'num1': persian_text_to_int(slots_dict['num1']),
                       'num2': persian_text_to_int(slots_dict['num2'])}
        if 'radical' in slots_dict and slots_dict['num1'] != '':
            context = {'operand': 'radical', 'num1': persian_text_to_int(slots_dict['num1'])}

    if intent == 'unit_convert':
        print('This is unit convert')
        if status == 'completed':
            if 'unit_volume1' in slots_dict and 'unit_volume2' in slots_dict:
                context = {'source_unit': slots_dict['unit_volume1'], 'dest_unit': slots_dict['unit_volume2']}
            elif 'unit_length1' in slots_dict and 'unit_length2' in slots_dict:
                context = {'source_unit': slots_dict['unit_length1'], 'dest_unit': slots_dict['unit_length2']}
            elif 'unit_mass1' in slots_dict and 'unit_mass2' in slots_dict:
                context = {'source_unit': slots_dict['unit_mass1'], 'dest_unit': slots_dict['unit_mass2']}
            elif 'unit_surface1' in slots_dict and 'unit_surface2' in slots_dict:
                context = {'source_unit': slots_dict['unit_surface1'], 'dest_unit': slots_dict['unit_surface2']}
            else:
                status = 'unacceptable'

    # Todo Change date to month, week , today
    if intent == 'ask_weather':
        print('This is ask_weather')
        if status == 'completed':
            ans = {'city': slots_dict['city'], 'date': ''}
            if 'date' in slots_dict:
                if slots_dict['date'] in date_names:
                    ans['date'] = str(convert_relative_date(slots_dict['date']))
                    print(ans['date'])
                else:
                    yy = 0
                    mm = 0
                    dd = 0
                    date = slots_dict['date'].split()
                    for d in date:
                        if d in shamsi.keys():
                            print(f'month recognized : {shamsi[d]}')
                            mm = shamsi[d]
                        else:
                            d_int = int(d)
                            if 1 <= d_int <= 31 and dd == 0:
                                dd = d_int
                                print(f'day recognized : {d_int}')
                            else:
                                # adding century
                                if d_int < 100:
                                    yy = d_int + 1300
                                else:
                                    yy = d_int
                                print(f'year recognized : {d_int}')
                    ans['date'] = f'{yy}-{mm}-{dd}'
            else:
                ans['date'] = jdatetime.date.today()
        context = ans

    # Todo آ
    if intent == 'esm_famil':
        if status == 'completed':
            ans = {'subject': slots_dict['esm_famil_subject'], 'alphabet': ''}
            if slots_dict['alphabet'] in alphabet:
                ans['alphabet'] = alphabet[slots_dict['alphabet']]
            else:
                ans['alphabet'] = slots_dict['alphabet']
            context = ans

    if intent == 'tasadofi':
        print('This is tasadofi')
        if status == 'completed':
            ans = {'starting_point': '', 'ending_point': ''}
            print(slots_dict['starting_point'])
            print(is_persian(slots_dict['starting_point']))
            if detect_language(slots_dict['starting_point']) == 'fa' or detect_language(
                    slots_dict['starting_point']) == 'ar':
                ans['starting_point'] = persian_text_to_int(slots_dict['starting_point'])
            else:
                ans['starting_point'] = int(slots_dict['starting_point'])

            if detect_language(slots_dict['ending_point']) == 'fa' or detect_language(
                    slots_dict['ending_point']) == 'ar':
                ans['ending_point'] = persian_text_to_int(slots_dict['ending_point'])
            else:
                ans['ending_point'] = int(slots_dict['ending_point'])
            # should we check for << >>?
            context = ans

    if intent == 'president' or intent == 'ask_capital':
        if status == 'completed':
            if slots_dict['country'] == 'کشور خودمون' or slots_dict['country'] == 'کشورمون' or slots_dict[
                'country'] == 'کشور ما':
                context = 'Iran'
            else:
                context = slots_dict['country']

    if intent == 'moshaere':
        if status == 'completed':
            if slots_dict['alphabet'] in alphabet:
                context = alphabet[slots_dict['alphabet']]
            else:
                context = slots_dict['alphabet']

    if intent == 'birth_things':
        print('This is birth things')
        if status == 'completed':
            for m in shamsi:
                print(f'checking {m}')
                i = slots_dict['month'].find(m)
                print(i)
                if i != -1:
                    context = shamsi[m]

    if intent == 'price_gold':
        print('This is price gold')
        if 'gold_type' in slots_dict:
            context = 'gold'
        elif 'coin_type' in slots_dict:
            context = 'coin'
        else:
            context = 'defualt'

    if intent == 'create_password':
        print('This is Password')
        if status == 'completed':
            if detect_language(slots_dict['length']) == 'fa' or detect_language(slots_dict['length']) == 'ar':
                context = persian_text_to_int(slots_dict['length'])
            else:
                context = int(slots_dict['length'])

    # Todo farsi
    if intent == 'movie_score' or intent == 'movie_info':
        if status == 'completed':
            context = translate_text(slots_dict['movie'])
    # Todo Find_cinema

    # Todo Persian
    if intent == 'book_info':
        if status == 'completed':
            context = translate_text(slots_dict['book_name'])

    if context == '':
        context = str(slots_dict)

    result = {'status': status, 'context': context, 'intent': intent}
    print(result)
    return result


# Request processing function
def process_user_request(request: UserRequest):
    intent_label = request.intent.label.lower()
    print(f'Intent : {intent_label}')
    slots_dict = {slot.label.lower(): slot.text for slot in request.slots}
    print(f'slots: {slots_dict}')
    response_data = dst(intent_label, slots_dict)
    return response_data


# Endpoint for processing requests
@app.post("/process_request")
async def process_request(request: UserRequest):
    try:
        result = process_user_request(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("dst:app", host="localhost", port=8080, reload=True)
