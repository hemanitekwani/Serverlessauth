import json
import boto3
import uuid
import re
from decimal import Decimal  

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userauth')

def lambda_handler(event, context):
    method = event['httpMethod']
    
    if method == 'POST':
        return create_user(event)
    elif method == 'GET':
        return get_users()
    elif method == 'DELETE':
        return delete_user(event)
    elif method == 'PUT':
        return update_user(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }

def validate_mobile_number(mob_num):
    return re.match(r'^\d{10}$', mob_num) is not None

def validate_pan_number(pan_num):
    return re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num) is not None

def create_user(event):
    data = json.loads(event['body'])
    
    full_name = data.get('full_name', '')
    mob_num = data.get('mob_num', '')
    pan_num = data.get('pan_num', '')
    
    if not full_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Full name must not be empty'})
        }
    
    if not validate_mobile_number(mob_num):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid mobile number'})
        }
    
    if not validate_pan_number(pan_num):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid PAN number'})
        }
    
    user_id = str(uuid.uuid4())
    
    table.put_item(
        Item={
            'user_id': user_id,
            'full_name': full_name,
            'mob_num': mob_num,
            'pan_num': pan_num
        }
    )
    
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'User created successfully', 'user_id': user_id})
    }

def get_users():
    response = table.scan()
    items = response.get('Items', [])
    
    if not items:
        return {
            'statusCode': 200,
            'body': json.dumps({'users': []})
        }
    
    users = []
    for item in items:
        
        user = {
            'user_id': str(item['user_id']),
            'full_name': item['full_name'],
            'mob_num': str(item['mob_num']),  
            'pan_num': str(item['pan_num'])   
        }
        users.append(user)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'users': users})
    }

def delete_user(event):
    data = json.loads(event['body'])
    user_id = data.get('user_id', '')
    
    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'User ID must be provided'})
        }
    
    response = table.delete_item(
        Key={'user_id': user_id}
    )
    
    if 'Attributes' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User deleted successfully'})
    }

def update_user(event):
    data = json.loads(event['body'])
    user_id = data.get('user_id', '')
    update_data = data.get('update_data', {})
    
    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'User ID must be provided'})
        }
    
    response = table.get_item(Key={'user_id': user_id})
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    
    item = response['Item']
    
    for key, value in update_data.items():
        if key == 'mob_num' and not validate_mobile_number(value):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid mobile number'})
            }
        if key == 'pan_num' and not validate_pan_number(value):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid PAN number'})
            }
        item[key] = value
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User updated successfully'})
    }



    
    