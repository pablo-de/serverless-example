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
