import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'dependencies'))

import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AppointmentsMedical')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    body = json.loads(event.get('body', '{}'))

    if path == "/appointments" and http_method == "POST":
        return create_appointment(body)
    elif path.startswith("/appointments") and http_method == "GET":
        appointment_id = path.split("/")[-1]
        return get_appointment(appointment_id)
    elif path.startswith("/appointments") and http_method == "PUT":
        appointment_id = path.split("/")[-1]
        return update_appointment(appointment_id, body)
    elif path.startswith("/appointments") and http_method == "DELETE":
        appointment_id = path.split("/")[-1]
        return delete_appointment(appointment_id)
    else:
        return response(404, {"message": "Not Found"})

def create_appointment(data):
    item = {
        'id': data['id'],
        'patient_id': data['patient_id'],
        'doctor_id': data['doctor_id'],
        'appointment_time': data['appointment_time'],
        'sts': data['sts'],
        'reason': data['reason']
    }
    table.put_item(Item=item)
    return response(201, {"message": "Appointment created successfully"})

def get_appointment(appointment_id):
    try:
        result = table.get_item(Key={'id': appointment_id})
        return response(200, result['Item'])
    except Exception as e:
        return response(404, {"message": str(e)})

def update_appointment(appointment_id, data):
    update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in data.keys())
    expression_attribute_values = {f":{k}": v for k, v in data.items()}
    try:
        table.update_item(
            Key={'id': appointment_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response(200, {"message": "Appointment updated successfully"})
    except Exception as e:
        return response(404, {"message": str(e)})

def delete_appointment(appointment_id):
    try:
        table.delete_item(Key={'id': appointment_id})
        return response(200, {"message": "Appointment deleted successfully"})
    except Exception as e:
        return response(404, {"message": str(e)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body, default=default_decimal),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def default_decimal(o):
    if isinstance(o, Decimal):
        return float(o)
    raise TypeError