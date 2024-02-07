import json
import uuid
import boto3
import os

region = os.environ['REGION']
queue_url = os.environ['PENDING_ORDER_QUEUE']

sqs = boto3.client('sqs', region_name=region)

def hacerPedido(event, context, callback):
    print('HacerPedido fue llamada')
    order_id = str(uuid.uuid1())

    params = {
        'MessageBody': json.dumps({'orderId': order_id}),
        'QueueUrl': queue_url
    }

    sqs.send_message(**params, Callback=send_response(callback))

def prepararPedido(event, context, callback):
    print('Preparar pedido fue llamada')
    print(event)
    callback()

def sendResponse(callback):
    def wrapper(status_code, message):
        response = {
            'statusCode': status_code,
            'body': json.dumps(message)
        }
        callback(None, response)
    return wrapper
