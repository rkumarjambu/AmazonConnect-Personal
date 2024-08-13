import json
from datetime import datetime

def lambda_handler(event, context):
    try:
        # Timestamp at invocation
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        print("Current date:", current_date)
        
        # HashMap of holidays
        holidays = {
            "2024-01-01": "New Year’s Day",
            "2024-01-15": "Martin Luther King Jr. Day",
            "2024-02-19": "Presidents’ Day",
            "2024-04-01": "Cesar Chavez Day (Observed)",
            "2024-05-27": "Memorial Day",
            "2024-07-04": "Independence Day",
            "2024-09-02": "Labor Day",
            "2024-11-11": "Veterans Day",
            "2024-11-28": "Thanksgiving Day",
            "2024-11-29": "Day after Thanksgiving",
            "2024-12-25": "Christmas Day"
        }
        
        # Check if the date is a holiday
        if current_date in holidays:
            print("Holiday detected:", holidays[current_date])
            response = {
                'statusCode': 200,
                'isHoliday': "True"
            }
        else:
            print("Not a holiday")
            response = {
                'statusCode': 200,
                'isHoliday': "False"
            }
            
        # Return the response
        print("Returning response:", response)
        return response

    except Exception as e:
        # Log the error and return a failure response
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred while processing the request.'})
        }