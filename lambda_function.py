import json
import boto3
import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('arn:aws:dynamodb:us-east-1:905418101464:table/Movies')

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYTI1YjBkMGY0ZDU0ZTA4OTRlYjk0YmMwYjZiZTRmNCIsInN1YiI6IjY2MDFlYTE1Yjg0Y2RkMDE2NGY1YjY4MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Tr2NmEqZ4Ws05q4FbS8NPf-RRqhhEvUvFYHXUtQ0SqU'

def search_movie(name):
    url = f'https://api.themoviedb.org/3/search/movie?query={name}&include_adult=false&language=en-US&page=1'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]  # Return the first search result
    return None

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def lambda_handler(event, context):
    name = event['name']
    
    # Search for the movie by name
    movie = search_movie(name)
    if not movie:
        return {
            'statusCode': 404,
            'body': json.dumps('Movie not found')
        }
    
    # Fetch movie details using the movie ID
    movie_id = movie['id']
    movie_details = get_movie_details(movie_id)
    if not movie_details:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to fetch movie details')
        }
    
    # Prepare the item to be added to DynamoDB
    item = {
        'id': movie_id,
        'name': movie['title'],
        'budget': movie_details.get('budget', 0),
        'revenue': movie_details.get('revenue', 0),
        'genres': [genre['name'] for genre in movie_details.get('genres', [])]
    }
    
    # Add item to DynamoDB
    table.put_item(Item=item)
    
    # Return the item
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

