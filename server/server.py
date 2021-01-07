from flask import Flask, request
import requests
from utils.languageprocessing import chatbot

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = ''# <paste your verify token here>
PAGE_ACCESS_TOKEN = ''# paste your page access token here>"


#Chatbot settings
QUESTION_PATH = "q_and_a.xlsx"
GREETING = "Olá! O Grupo Turing agradece o contato!\n"
NO_ANSWER = "Logo um membro entrará em contato para responder sua questão"
bot = chatbot.QuestionEmbeddings(QUESTION_PATH, GREETING, NO_ANSWER)

def get_bot_response(message):
    return bot.get_response(message)

def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


