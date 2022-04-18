import json
import boto3
import re
from os import environ
null = None
none = None
false = False
true = True


def isTruncated(b):
    if 'truncated' in b['tweet_create_events'][0]:
        if b['tweet_create_events'][0]['truncated'] == true:
            return True
    return False


def isCreateEvent(b):
    if 'tweet_create_events' in b:
        return True
    return False


def hasMedia(b):
    try:
        if 'media_url_https' in b['tweet_create_events'][0]['entities']['media'][0]:
            return True
    except:
        return False


def hastco(t):
    if "https://t.co" in t:
        return True
    return False


def removetco(t):
    print("running removetco")
    return re.sub(r' https?:\/\/.*[\r\n]*', '', t)


def uploadToS3(tweet):
    bucketName = environ['BUCKETNAME']
    print("Output to S3: " + json.dumps(tweet))
    print("Uploading...")
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucketName, Key='tweet.json',
                         Body=str(json.dumps(tweet)), ContentType='text/plain; charset=utf-8')

def lambda_handler(event, context):
    print("vvv")
    print(json.dumps(event))
    print("^^^")
    body = json.loads(event['body'])
    print(json.dumps(body))
    tweet = {}
    if isCreateEvent(body):
        if isTruncated(body):
            tweet["fulltext"] = body["tweet_create_events"][0]["extended_tweet"]["full_text"]
        else:
            tweet["fulltext"] = body["tweet_create_events"][0]["text"]
        tweet["timestamp_ms"] = body["tweet_create_events"][0]["timestamp_ms"]
        tweet["created_at"] = body["tweet_create_events"][0]["created_at"]
        if hasMedia(body):
            tweet["media"] = body['tweet_create_events'][0]['entities']['media'][0]['media_url_https']+":small"
        if hastco(tweet["fulltext"]):
            tweet["fulltext"] = removetco(tweet["fulltext"])
        uploadToS3(tweet)

    return {
        'statusCode': 200,
        'body': json.dumps('Thank you, Mr. Twitter.')
    }
