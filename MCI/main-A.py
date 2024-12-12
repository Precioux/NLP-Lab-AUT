import requests
import json
import psycopg2
from typing import Optional

# Database connection parameters
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "dst_database"
DB_USER = "postgres"

# Connect to the database
conn = psycopg2.connect(
    dbname=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER
)
conn.autocommit = True


# Define the send_NLU function as provided
def send_NLU(data, turn):
    global url_NLU
    params = {'conversation': data, 'turn': turn}
    try:
        response = requests.get(url_NLU, params=params)
        print(f"Request made to: {url_NLU} with params: {params}")
        return response
    except Exception as e:
        print(f"Error while making request: {str(e)}")
        raise


# Set up the URL for the NLU service
url_NLU = "http://localhost:8089/predict"


# Define the send_DST function
def send_DST(data):
    global url_DST
    response = requests.post(url_DST, json=data)
    return response


# Set up the URL for the DST service
url_DST = "http://localhost:8093/process_request"


# Define the send_confirmation function
def send_confirmation(data):
    global url_confirmation
    response = requests.post(url_confirmation, json=data)
    return response


# Set up the URL for the confirmation service
url_confirmation = "http://localhost:8000/check_intent/"


# Function to check if the table is empty
def is_table_empty(table_name: str) -> bool:
    cursor = conn.cursor()
    #print(f'Checking if table {table_name} is empty')
    select_query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(select_query)
    result = cursor.fetchone()
    is_empty = result[0] == 0
    #print(f'Table {table_name} is empty: {is_empty}')
    cursor.close()
    return is_empty


# Function to get the conversation_id of the latest added row
def get_latest_conversation_id() -> Optional[str]:
    # print('Getting conversation_id of the latest added row')
    cursor = conn.cursor()
    select_query = "SELECT conversation_id FROM states ORDER BY id DESC LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
    #print(f'Latest conversation_id: {result[0]}' if result else 'No rows found')
    cursor.close()
    return result[0] if result else None


# Define the conversation ID generator function
def conversation_ID_generator():
    #print('Generating conversation ID')
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


def chatbot():
    print("Hello! I am your chatbot. You can start chatting with me now.")
    conversation_data = []
    cid = conversation_ID_generator()  # Generate a conversation ID at the start of the chat
    print(f"Conversation ID: {cid}")
    turn = 0

    while True:
        # Get user input
        user_input = input("You: ")

        # If user wants to exit the chat
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Have a great day!")
            break

        # Store the user's message in conversation data
        conversation_data.append(user_input+' ')
        turn += 1  # Increment turn

        # Send the conversation to the NLU function
        try:
            print('Sending to NLU:')
            print("------------------------------------------------------")
            response = send_NLU(" ".join(conversation_data), user_input)
            print("------------------------------------------------------")
            if response.status_code == 200:
                # Handle the response from the NLU server
                nlu_result = response.json()
                print('Sending to Confirmation:')
                print("------------------------------------------------------")
                result_confirmation = send_confirmation(nlu_result).json()
                print(f"NLU Response: {json.dumps(nlu_result, indent=4, ensure_ascii=False)}")
                print("------------------------------------------------------")
                print(f"Confirmation Response: {json.dumps(result_confirmation, indent=4, ensure_ascii=False)}")
                print("------------------------------------------------------")
                confirmed_intent = result_confirmation.get('intent1')
                confirmation_status = result_confirmation.get('status')

                # Add conversation_id to result_NLU_json
                nlu_result['conversation_id'] = cid

                dst_status = None
                dst_context = None
                dst_intent = None

                if confirmation_status == 'confirmed':
                    result_DST = send_DST(nlu_result).json()
                    print("=================================================================")
                    print('This is DST')
                    print(json.dumps(result_DST, indent=4, ensure_ascii=False))
                    print("=================================================================")
                    dst_status = result_DST.get('status')
                    dst_context = result_DST.get('context')
                    dst_intent = result_DST.get('intent')

                    # If DST status is not completed, use context question for chatbot reply
                    if dst_status == 'not-completed' and dst_context:
                        bot_reply = dst_context.get('question', "I didn't quite get that. Can you please elaborate?")
                        conversation_data.append('BOT_START ' + bot_reply + ' BOT_END ')
                    elif dst_status == 'completed':
                        print('-----------Completed-----------')
                        bot_reply = nlu_result.get("conversation", {}).get("intent", {}).get("label",
                                                                                             "I didn't quite get that. Can you please elaborate?")
                        conversation_data.clear()
                    else:
                        bot_reply = nlu_result.get("conversation", {}).get("intent", {}).get("label",
                                                                                             "I didn't quite get that. Can you please elaborate?")
                else:
                    bot_reply = nlu_result.get("conversation", {}).get("intent", {}).get("label",
                                                                                         "I didn't quite get that. Can you please elaborate?")

                print(f"Chatbot: {bot_reply}")
                
            else:
                print(f"Chatbot: Sorry, I had an issue understanding you. (Error Code: {response.status_code})")
                print(f"Response content: {response.text}")
        except Exception as e:
            print(f"Chatbot: Oops! Something went wrong. Error: {str(e)}")


# Run the chatbot
if __name__ == "__main__":
    chatbot()
