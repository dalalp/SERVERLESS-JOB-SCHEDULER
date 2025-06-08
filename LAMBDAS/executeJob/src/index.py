import json
import boto3
import requests

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'JobScheduler'

def lambda_handler(event, context):
    try:
        job_id = event.get('jobId')
        if not job_id:
            raise ValueError("No jobId provided in event.")

        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={'jobId': job_id})
        job = response.get('Item')

        if not job:
            raise ValueError(f"Job with id {job_id} not found.")

        url = job['url']
        method = job.get('method', 'GET').upper()
        payload = job.get('payload', {})

        # Execute the HTTP request
        headers = {'Content-Type': 'application/json'}
        if method == 'POST':
            res = requests.post(url, data=json.dumps(payload), headers=headers)
        elif method == 'PUT':
            res = requests.put(url, data=json.dumps(payload), headers=headers)
        elif method == 'DELETE':
            res = requests.delete(url, headers=headers)
        else:
            res = requests.get(url, headers=headers)

        # Log result
        print(f"Executed job {job_id} with status {res.status_code}")
        print("Response:", res.text)

        return {
            'statusCode': res.status_code,
            'body': res.text
        }

    except Exception as e:
        print(f"Error executing job: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
