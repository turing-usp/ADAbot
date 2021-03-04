import requests
import os
from languageprocessing.chatbot import QuestionEmbeddings


FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')


#Chatbot settings
QUESTION_PATH = "assets/q_and_a.csv"
GREETING = "Olá, eu sou a Ada, um bot em desenvolvimento pelo Grupo Turing! O Grupo Turing agradece o contato!\n"
NO_ANSWER = "Logo um membro entrará em contato para responder sua questão"

bot = QuestionEmbeddings(QUESTION_PATH, NO_ANSWER)

def get_bot_response(message):
    return bot.get_response(message)

def verify_webhook(event):
    if keys_exist(event, ["params","querystring","hub.verify_token","hub.challenge"]):
        v_token   = str(find_item(event,'hub.verify_token'))
        challenge = int(find_item(event,'hub.challenge'))
        if (VERIFY_TOKEN == v_token):
            return(challenge)

def respond(sender, message):
    response = get_bot_response(message)
    response = GREETING + response
    send_message(sender, response)

##recursively look/return for an item in dict given key
def find_item(obj, key):
    item = None
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = find_item(v, key)
            if item is not None:
                return item

##recursivley check for items in a dict given key
def keys_exist(obj, keys):
    for key in keys:
        if find_item(obj, key) is None:
            return(False)
    return(True)

def send_message(recipient_id, text):
    payload = {
        'messaging_type': 'RESPONSE',
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        }}

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def lambda_handler(event, context):
    #handle webhook challenge
    challenge = verify_webhook(event)
    if challenge != None:
        return challenge
            
    #handle messaging events
    if keys_exist(event, ['body-json','entry']):
        event_entry0 = event['body-json']['entry'][0]
        if keys_exist(event_entry0, ['messaging']):
            messaging_event = event_entry0['messaging'][0]
            msg_txt   = messaging_event['message']['text']
            sender_id = messaging_event['sender']['id']
            respond(sender_id, msg_txt)
