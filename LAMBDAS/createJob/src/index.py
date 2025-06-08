import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')
lambda_client = boto3.client('lambda')

TABLE_NAME = 'JobScheduler'
TARGET_LAMBDA_ARN = '<REPLACE_WITH_EXECUTEJOB_LAMBDA_ARN>'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        job_id = str(uuid.uuid4())

        # Extract fields
        url = body['url']
        method = body.get('method', 'GET').upper()
        cron_expr = body['cron']  # e.g., 'cron(0 12 * * ? *)'

        # Save to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'jobId': job_id,
            'url': url,
            'method': method,
            'cron': cron_expr,
            'status': 'scheduled'
        })

        # Create CloudWatch Rule
        rule_name = f"job_{job_id}"
        events.put_rule(
            Name=rule_name,
            ScheduleExpression=cron_expr,
            State='ENABLED'
        )

        # Add target
        events.put_targets(
            Rule=rule_name,
            Targets=[{
                'Id': '1',
                'Arn': TARGET_LAMBDA_ARN,
                'Input': json.dumps({'jobId': job_id})
            }]
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Job scheduled", "jobId": job_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
