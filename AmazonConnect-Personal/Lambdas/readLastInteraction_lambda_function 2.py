import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerInteractions')

def lambda_handler(event, context):
    try:
        # Ensure phone number is an integer & extracts primary key for look-up in table
        print(event)
        phone_number = int(event['Details']['ContactData']['CustomerEndpoint']['Address'])
        # Check if the phone number exists in the table
        response = table.get_item(
            Key={'PhoneNumber': phone_number}
        )
        
        if 'Item' in response:
            # Phone number exists, return the last interaction data
            last_interaction = response['Item']
            return {
                'statusCode': 200,
                'LastInteractionCategory': last_interaction['LastInteractionCategory'],
                'LastInteractionDate': last_interaction['LastInteractionDate']
            }
        else:
            # Phone number does not exist, return a message indicating no previous interaction
            return {
                'statusCode': 200,
                'LastInteractionCategory': "Null",
                'LastInteractionDate': "Null"
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred while processing the request.'})
        }