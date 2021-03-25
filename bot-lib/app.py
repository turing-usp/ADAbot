import requests
import os
import boto3
from multiprocessing import Process

from languageprocessing.chatbot import QuestionEmbeddings
from aux.dynamobd_handler import DynamodbHandler

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

# csv file
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_QUESTIONS_KEY = os.getenv('S3_QUESTIONS_KEY')
s3client = boto3.client('s3')
s3client.download_file(S3_BUCKET_NAME, S3_QUESTIONS_KEY, '/tmp/' + S3_QUESTIONS_KEY)

# Chatbot settings
QUESTION_PATH = "/tmp/" + S3_QUESTIONS_KEY
GREETING = os.getenv('MESSAGE_GREETING')
NO_ANSWER = os.getenv('MESSAGE_NO_ANSWER')
EVALUATE = os.getenv('MESSAGE_EVALUATE')


bot = QuestionEmbeddings(QUESTION_PATH, NO_ANSWER)

# Database configuration
MESSAGE_TABLE = os.getenv('TABLE_MESSAGE')
RATING_TABLE = os.getenv('TABLE_RATING')

dinamodb_handler = DynamodbHandler(MESSAGE_TABLE, RATING_TABLE)


def handle_response(sender, message, time):
    last_interaction, last_bot_response, last_time = dinamodb_handler.get_last_interaction(sender)
    print("Time:", time, type(time))
    print("Last time:", last_time, type(last_time))
    print("Last message:", last_interaction, type(last_interaction))

    if last_time is None:
        send_greeting = True
    else:
        if last_time - time > 300000:
            send_greeting = True
        else:
            send_greeting = False
    if send_greeting:
        send_message(sender, GREETING)
    # if message is a pure number - register as evaluation
    try:
        message = float(message.strip())
        dinamodb_handler.put_rating(sender, time, message, last_interaction, last_bot_response)
    except ValueError:
        response = bot.get_response(message)
        dinamodb_handler.put_message(sender, time, message, response)
        send_message(sender, response)
        send_message(sender, EVALUATE)


def send_message(recipient_id, text):
    payload = {'messaging_type': 'RESPONSE', 'message': {'text': text}, 'recipient': {'id': recipient_id}}

    auth = {'access_token': PAGE_ACCESS_TOKEN}

    response = requests.post(FB_API_URL, params=auth, json=payload)

    return response.json()


def lambda_handler(event, context):
    print(event)
    sender, message, time = event['sender'], event['message'], event['time']
    handle_response(sender, message, time)
