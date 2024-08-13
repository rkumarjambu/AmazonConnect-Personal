import json
import boto3
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerInteractions')

def lambda_handler(event, context):
    try:
        #Ensure phone number is an integer and extract primary key from payload
        print(event)
        phone_number = int(event['Details']['ContactData']['CustomerEndpoint']['Address']) 
        #Extract intent of interaction dynamically from the flow for each contact
        interaction_category = event['Details']['ContactData']['Attributes']['Category'] 
        
        # Get current date and time
        current_time = datetime.utcnow().strftime('%Y-%m-%d')
        
        # Check if the phone number exists in the table
        response = table.get_item(
            Key={'PhoneNumber': phone_number}
        )
        
        if 'Item' in response:
            # Phone number exists, update the interaction data
            table.update_item(
                Key={'PhoneNumber': phone_number},
                UpdateExpression="SET LastInteractionCategory = :category, LastInteractionDate = :date",
                ExpressionAttributeValues={
                    ':category': interaction_category,
                    ':date': current_time
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps('Interaction updated successfully.')
            }
        else:
            # Phone number does not exist, create a new entry
            table.put_item(
                Item={
                    'PhoneNumber': phone_number,
                    'LastInteractionCategory': interaction_category,
                    'LastInteractionDate': current_time
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps('Interaction stored successfully.')
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred while processing the request.'})
        }