import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import uuid


class DynamodbHandler:
    def __init__(self, MESSAGE_TABLE, RATING_TABLE):
        self.dynamodb = boto3.resource('dynamodb')
        self.messages_table = self.dynamodb.Table(MESSAGE_TABLE)
        self.rating_table = self.dynamodb.Table(RATING_TABLE)

    def put_message(self, user_id, time, message_txt, bot_given_response):
        response = self.messages_table.put_item(
            Item={
                'interaction_id': str(uuid.uuid4()),
                'user_id': user_id,
                'time': time,
                'message_txt': message_txt,
                'bot_given_response': bot_given_response,
            }
        )
        return response

    def put_rating(self, user_id, time, rating, message_user, bot_given_response):
        try:
            rating = int(rating)
            response = self.rating_table.put_item(
                Item={
                    'interaction_id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'time': time,
                    'message_user': message_user,
                    'bot_given_response': bot_given_response,
                    'rating': rating,
                }
            )
            return response
        except Exception as e:
            print(e)
            return None

    def get_last_interaction(self, user_id):
        try:
            response = self.messages_table.scan(FilterExpression=Attr('user_id').eq(user_id))
            items = response['Items']
            if len(items) < 1:
                return None, None, None
            last_time = -999
            last_interaction = ""
            last_bot_response = ""
            for item in items:
                if item['time'] > last_time:
                    last_time = item['time']
                    last_interaction = item['message_txt']
                    last_bot_response = item['bot_given_response']
            return last_interaction, last_bot_response, last_time

        except ClientError as e:
            print(e.response['Error']['Message'])
            return None, None, None
