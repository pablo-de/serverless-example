import os
import json
import uuid
import boto3

region = os.environ['REGION']
queue_url = os.environ['PENDING_ORDER_QUEUE']

sqs = boto3.client('sqs', region_name=region)

def hacer_pedido(event, context):
    print('hacer_pedido fue llamada')
    order_id = str(uuid.uuid1())

    params = {
        'MessageBody': json.dumps({'orderId': order_id}),
        'QueueUrl': queue_url
    }

    try:
        response = sqs.send_message(**params)
        message = {
            'orderId': order_id,
            'messageId': response['MessageId']
        }
        return send_response(200, message)
    except Exception as e:
        return send_response(500, str(e))

def send_response(status_code, message):
    response = {
        'statusCode': status_code,
        'body': json.dumps(message)
    }
    return response
