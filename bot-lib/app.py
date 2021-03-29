import requests
import os
import boto3

from languageprocessing.chatbot import QuestionEmbeddings
from aux.dynamobd_handler import DynamodbHandler

#############################################
# Facebook controler
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

# csv file
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_QUESTIONS_KEY = os.getenv('S3_QUESTIONS_KEY')

# Chatbot settings
QUESTION_PATH = "/tmp/" + S3_QUESTIONS_KEY
GREETING = os.getenv('MESSAGE_GREETING')
NO_ANSWER = os.getenv('MESSAGE_NO_ANSWER')
EVALUATE = os.getenv('MESSAGE_EVALUATE')
THANK_YOU = os.getenv('MESSAGE_THANK_YOU')

# Database configuration
MESSAGE_TABLE = os.getenv('TABLE_MESSAGE')
RATING_TABLE = os.getenv('TABLE_RATING')

# alerts telegram
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
#############################################

s3client = boto3.client('s3')
s3client.download_file(S3_BUCKET_NAME, S3_QUESTIONS_KEY, '/tmp/' + S3_QUESTIONS_KEY)
bot = QuestionEmbeddings(QUESTION_PATH, NO_ANSWER)
dinamodb_handler = DynamodbHandler(MESSAGE_TABLE, RATING_TABLE)


def handle_response(sender, message, time):
    last_interaction, last_bot_response, last_time = dinamodb_handler.get_last_interaction(sender)

    if last_time is None:
        send_greeting = True
    else:
        if time - last_time > 300000:
            send_greeting = True
        else:
            send_greeting = False
    if send_greeting:
        send_message(sender, GREETING)
    # if message is a pure number - register as rating
    try:
        message = float(message.strip())
    except ValueError:
        message = str(message)

    if isinstance(message, float):
        dinamodb_handler.put_rating(sender, time, message, last_interaction, last_bot_response)
        send_message(sender, THANK_YOU)
    else:
        response, found_answer, is_greeting = bot.get_response(message)
        if is_greeting:
            print(message)
            send_message(sender, GREETING)
        if not found_answer:
            endpoint = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode={3}"
            ada_alert = "<i>Ada em apuros! Ajude-a respondendo a essa mensagem no Facebook:</i> {}".format(message)
            r = requests.get(endpoint.format(TELEGRAM_TOKEN, CHAT_ID, ada_alert, 'HTML'))
            send_message(sender, response)
        if found_answer and not(is_greeting): 
            send_message(sender, response)
            send_message(sender, EVALUATE)
        dinamodb_handler.put_message(sender, time, message, response)
        


def send_message(recipient_id, text):
    payload = {'messaging_type': 'RESPONSE', 'message': {'text': text}, 'recipient': {'id': recipient_id}}

    auth = {'access_token': PAGE_ACCESS_TOKEN}

    response = requests.post(FB_API_URL, params=auth, json=payload)

    return response.json()


def lambda_handler(event, context):
    print(event)
    sender, message, time = event['sender'], event['message'], event['time']
    handle_response(sender, message, time)
