import json
import time
import uuid
import boto3
import os
import orderMetadataManager

region = os.environ['REGION']
queue_url = os.environ['PENDING_ORDER_QUEUE']

sqs = boto3.client('sqs', region_name=region)

def hacerPedido(event, context):
    print('HacerPedido fue llamada')

    body = json.loads(event['body'])

    order = {
        'orderId': str(uuid.uuid1()),
        'name': body['name'],
        'address': body['address'],
        'pizzas': body['pizzas'],
        'timestamp': int(time.time() * 1000)
    }

    params = {
        'MessageBody': json.dumps(order),
        'QueueUrl': queue_url
    }

    try:
        response = sqs.send_message(**params)
        message = {
            'order': order,
            'messageId': response['MessageId']
        }
        return sendResponse(200, message)
    except Exception as e:
        return sendResponse(500, str(e))

def prepararPedido(event, context):
    print('Preparar pedido fue llamada')

    order = json.loads(event['Records'][0]['body'])

    try:
        orderMetadataManager.saveCompletedOrder(order)
        return {'statusCode': 200}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

def enviarPedido(event, context):
    print('enviarPedido fue llamada')

    record = event['Records'][0]
    if record['eventName'] == 'INSERT':
        print('deliverOrder')

        orderId = record['dynamodb']['Keys']['orderId']['S']

        try:
            orderMetadataManager.deliverOrder(orderId)
            return {'statusCode': 200}
        except Exception as e:
            return {'statusCode': 500, 'body': str(e)}
    else:
        print('is not a new record')
        return {'statusCode': 200}

def sendResponse(statusCode, message):
    return {
        'statusCode': statusCode,
        'body': json.dumps(message)
    }
