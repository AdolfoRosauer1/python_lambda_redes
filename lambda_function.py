import json
import boto3
import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('arn:aws:dynamodb:us-east-1:905418101464:table/Movies')

def fetch_additional_data(user_id, name):
    # Fetch additional data from the external API
    # response = requests.get(f'https://api.example.com/data?id={user_id}&name={name}')
    # data = response.json()
    # return data.get('description')
    return 'mock data'

def lambda_handler(event, context):
    user_id = event['id']
    name = event['name']
    
    # Fetch additional data
    description = fetch_additional_data(user_id, name)
    
    # Add all data to DynamoDB
    item = {
        'id': user_id,
        'name': name,
        'description': description
    }
    table.put_item(Item=item)
    
    # Return the item
    return item
