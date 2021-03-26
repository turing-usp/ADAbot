import os
import json
import boto3

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
FUNCTION_NAME = os.getenv('FUNCTION_NAME')


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


# recursively check for items in a dict given key
def keys_exist(obj, keys):
    for key in keys:
        if find_item(obj, key) is None:
            return False
    return True


def verify_webhook(event):
    if keys_exist(event, ["hub.verify_token", "hub.challenge"]):
        v_token = str(find_item(event, 'hub.verify_token'))
        challenge = int(find_item(event, 'hub.challenge'))
        if VERIFY_TOKEN == v_token:
            return challenge


def lambda_handler(event, context):
    client = boto3.client('lambda')

    challenge = verify_webhook(event)
    if challenge is not None:
        return challenge

    if keys_exist(event, ['body']):
        event_entry0 = json.loads(event['body'])['entry'][0]
        time = event_entry0['time']
        if keys_exist(event_entry0, ['messaging']):
            messaging_event = event_entry0['messaging'][0]
            if keys_exist(messaging_event, ['message', 'sender']):
                message = messaging_event['message']
                if message.get('is_echo') is True:
                    return 0
                msg_txt = message['text']
                sender_id = messaging_event['sender']['id']
                params = {'message': msg_txt, 'sender': sender_id, 'time': time}
                print(params)
                client.invoke(FunctionName=FUNCTION_NAME, InvocationType='Event', Payload=json.dumps(params))

    return {'statusCode': 202}
