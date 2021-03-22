import requests
import os
import boto3
from multiprocessing import Process

from languageprocessing.chatbot import QuestionEmbeddings
from aux.dynamobd_handler import DynamodbHandler


FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')


# csv file
S3_FILENAME = 'q_and_a.csv'
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_QUESTIONS_KEY = os.getenv('S3_QUESTIONS_KEY')
s3client = boto3.client('s3')
s3client.download_file(S3_BUCKET_NAME, S3_QUESTIONS_KEY, '/tmp/' + S3_FILENAME)

# Chatbot settings
QUESTION_PATH = "/tmp/" + S3_FILENAME
GREETING = "Olá, eu sou a Ada, um bot em desenvolvimento pelo Grupo Turing! O Grupo Turing agradece o contato!\n"
NO_ANSWER = "Logo um membro entrará em contato para responder sua questão"
EVALUATE = "O quanto essa resposta te ajudou de 0 (nada) a 5 (respondeu minha questão)?"


bot = QuestionEmbeddings(QUESTION_PATH, NO_ANSWER)

# Database configuration
MESSAGE_TABLE = os.getenv('MESSAGE_TABLE')
RATING_TABLE = os.getenv('RATING_TABLE')

dinamodb_handler = DynamodbHandler(MESSAGE_TABLE, RATING_TABLE)


def verify_webhook(event):
    if keys_exist(event, ["params", "querystring", "hub.verify_token", "hub.challenge"]):
        v_token = str(find_item(event, 'hub.verify_token'))
        challenge = int(find_item(event, 'hub.challenge'))
        if VERIFY_TOKEN == v_token:
            return challenge


def handle_response(sender, message, time):
    last_interaction, last_bot_response, last_time = dinamodb_handler.get_last_interaction(sender)
    print("Time:", time)
    print("Last time:", last_time)
    print("Last message:", last_interaction)

    if last_time is None:
        send_greeting = True
    else:
        if last_time - time > 300000:
            send_greeting = True
        else:
            send_greeting = False
    if send_greeting:
        send_message(sender, GREETING)
    # if message is a pure number - register as greeting
    try:
        message = float(message.strip())
        dinamodb_handler.put_rating(sender, time, message, last_interaction, last_bot_response)
    except ValueError:
        response = bot.get_response(message)
        dinamodb_handler.put_message(sender, time, message, response)
        send_message(sender, response)
        send_message(sender, EVALUATE)


# recursively look/return for an item in dict given key
def find_item(obj, key):
    item = None
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = find_item(v, key)
            if item is not None:
                return item


# recursivley check for items in a dict given key
def keys_exist(obj, keys):
    for key in keys:
        if find_item(obj, key) is None:
            return False
    return True


def send_message(recipient_id, text):
    payload = {'messaging_type': 'RESPONSE', 'message': {'text': text}, 'recipient': {'id': recipient_id}}

    auth = {'access_token': PAGE_ACCESS_TOKEN}

    response = requests.post(FB_API_URL, params=auth, json=payload)

    return response.json()


def lambda_handler(event, context):
    # handle webhook challenge
    challenge = verify_webhook(event)
    if challenge is not None:
        return challenge

    # handle messaging events
    if keys_exist(event, ['body-json', 'entry']):
        event_entry0 = event['body-json']['entry'][0]
        time = event_entry0['time']
        if keys_exist(event_entry0, ['messaging']):
            messaging_event = event_entry0['messaging'][0]
            if keys_exist(messaging_event, ['message', 'sender']):
                message = messaging_event['message']
                if message.get('is_echo') is True:
                    return 0
                msg_txt = message['text']
                sender_id = messaging_event['sender']['id']
                handle_response(sender_id, msg_txt, time)
