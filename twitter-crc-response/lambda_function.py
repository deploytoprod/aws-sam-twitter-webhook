import boto3
import json
from os import environ
null = None
none = None
false = False
true = True

def crc(event, context):
    print(json.dumps(event))
    """ Returns a CRC (Challenge Response Check) to keep this webhook
    secure. https://goo.gl/kFdJgV for more details. """
    # Short circuit ping from CloudWatch Events
    if event.get('source', None) == 'aws.events':
        print('ping')
        return

    import base64
    import hmac
    import hashlib
    print('Calculating CRC')
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameters(
            Names=[
                environ['TWITTERAPISECRET']
            ],
            WithDecryption=True
        )
    except ClientError as error:
        print('Problem getting keys from SSM: {}'.format(error))
        return {
            'statusCode': 501,
            'body': 'Problem getting Twitter API Key Secret'
        }
    else:
        params = response['Parameters']
        crc = event['queryStringParameters']['crc_token']
        sha256_hash_digest = hmac.new(
            params[0]['Value'].encode('utf-8'), msg=crc.encode('utf-8'),
            digestmod=hashlib.sha256).digest()
        body = json.dumps({'response_token': 'sha256=' +
                           base64.b64encode(sha256_hash_digest).decode('utf-8')})
        print('Body response: {}'.format(body))
        response = {
            'statusCode': 200,
            'body': body
        }
        return response
