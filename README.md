# Serverlessauth

Lambda Function Creation:
Created AWS Lambda functions for user authentication, including functions for creating, retrieving, updating, and deleting user records.

API Gateway Configuration:
Configured API Gateway endpoints to trigger the Lambda functions. Defined appropriate HTTP methods (GET, POST, PUT, DELETE) for interacting with the Lambda functions.

DynamoDB Table Setup:
Created a DynamoDB table named userauth to store user records. Defined attributes such as user_id, full_name, mob_num, and pan_num for each user.

Lambda Function Logic:
Implemented logic within the Lambda functions to handle requests from the API Gateway. Validated input data, performed CRUD operations on the DynamoDB table, and returned appropriate responses.

Testing with Postman: 
Tested the functionality of the API endpoints using Postman. Sent requests for creating, retrieving, updating, and deleting user records. Verified the responses and handled errors as needed.
