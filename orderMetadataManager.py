import os
import boto3

# Inicializa el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['COMPLETED_ORDER_TABLE']
table = dynamodb.Table(table_name)

def saveCompletedOrder(order):
    print('Guardar un pedido fue llamado')

    # Establece el estado de entrega como 'READY_FOR_DELIVERY'
    order['delivery_status'] = 'READY_FOR_DELIVERY'

    # Define los parámetros para la operación de put
    params = {
        'TableName': table_name,
        'Item': order
    }

    # Realiza la operación de put en la tabla de DynamoDB
    try:
        response = table.put_item(**params)
        return response
    except Exception as e:
        # Maneja cualquier excepción que pueda ocurrir durante la operación de put
        print("Error al guardar el pedido completado:", e)
        raise

def deliverOrder(orderId):
    print('Enviar una orden fue llamado')

    try:
        response = table.update_item(
            Key={'orderId': orderId},
            ConditionExpression='attribute_exists(orderId)',
            UpdateExpression='set delivery_status = :v',
            ExpressionAttributeValues={':v': 'DELIVERED'},
            ReturnValues='ALL_NEW'
        )
        print('order delivered')
        return response['Attributes']
    except Exception as e:
        print("Error al entregar el pedido:", e)
        raise

def getOrder(orderId):
    print('El metodo obtener una orden fue llamado')

    try:
        response = table.get_item(
            Key={
                'orderId': orderId
            }
        )
        return response.get('Item')
    except Exception as e:
        print("Error al obtener el pedido:", e)
        raise
