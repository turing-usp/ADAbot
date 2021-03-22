import os
import json
import boto3


def lambda_handler(event, context):
    print(event)
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='turing-chatbot-nlp',
        InvocationType='Event',
        Payload=json.dumps(event)
    )