import os
import requests

CHAT_ID = os.getenv('CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

def send_telegram_alert(TELEGRAM_TOKEN,CHAT_ID, user_message):
    endpoint = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}"
    ada_alert = "Ada em apuros! Ajude-a respondendo a essa mensagem no Facebook: {}".format(user_message)
    r = requests.get(endpoint.format(TELEGRAM_TOKEN, CHAT_ID, ada_alert))
    return r.status_code

def lambda_handler(event, context):
    user_message = event["user_message"]
    auth = event["auth_token"]
    if auth == AUTH_TOKEN:
        send_telegram_alert(TELEGRAM_TOKEN, CHAT_ID, user_message)
