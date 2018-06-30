import boto3  
import json
import requests
import os
from datetime import datetime

def handler(event, context):
    sqs = boto3.client('sqs')
    url = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
    response = requests.request("GET", url)
    print os.environ['QUEUE_URL']
    marketData = json.loads(response.text)['result']
    minutes = datetime.strptime(marketData[0]['TimeStamp'],"%Y-%m-%dT%H:%M:%S.%f").minute
    sqsData = {
        'action_type':  'one_minute_data',
        'payload': marketData
    }
    queueResponse = sqs.send_message(QueueUrl=os.environ['QUEUE_URL'],MessageBody=json.dumps(sqsData))
    if minutes%5 == 0:
        sqsData = {'action_type':  'five_minutes_data','payload': marketData}
        queueResponse = sqs.send_message(QueueUrl=os.environ['QUEUE_URL'],MessageBody=json.dumps(sqsData))
    if minutes%15 == 0:
        sqsData = {'action_type':  'fifteen_minutes_data','payload': marketData}
        queueResponse = sqs.send_message(QueueUrl=os.environ['QUEUE_URL'],MessageBody=json.dumps(sqsData))
    if minutes%30 == 0:
        sqsData = {'action_type':  'thirty_minutes_data','payload': marketData}
        queueResponse = sqs.send_message(QueueUrl=os.environ['QUEUE_URL'],MessageBody=json.dumps(sqsData))
    if minutes == 0:
        sqsData = {'action_type':  'sixty_minutes_data','payload': marketData}
        queueResponse = sqs.send_message(QueueUrl=os.environ['QUEUE_URL'],MessageBody=json.dumps(sqsData))
    