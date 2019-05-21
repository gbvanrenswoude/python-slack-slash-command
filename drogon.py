import boto3
import json
import logging
import os

from base64 import b64decode
from urlparse import parse_qs


expected_token = "sometoken"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))

    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    if 'text' in params:
        command_text = params['text'][0]
    else:
        command_text = ''

    return respond(None, "%s invoked %s in %s and he burned the following line: :fire: :fire: :fire: :fire: %s :fire: :fire: :fire: :fire:" % (user, command, channel, command_text))
