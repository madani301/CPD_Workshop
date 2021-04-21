#!/usr/local/bin/python3

"""

This script was made by Madani Napaul.

Please use this only as a reference while working on your Cloud Platform
Development Coursework. 

Most of the material here are from AWS Documentations. Go to AWS Documentations
for further information. 

Thank you!

"""

# Import the required libraries
import boto3

# Create the resource for dynamoDB
dynamodb = boto3.resource("dynamodb")

# Create the table by starting with the TableName
# KeySchema is the schema for the table, where KeyType 'HASH' is the partition key
# AttributeDefinitions is where you set the data type, for e.g, Strings, Numbers, Booleans, etc.
# ProvisionedThroughput is where you set the capacity for reading/writing to the dynamoDB table
table = dynamodb.create_table(
    TableName="dynamodb-cpd-2021",
    KeySchema=[{"AttributeName": "Image_Name", "KeyType": "HASH"}],
    AttributeDefinitions=[
        {"AttributeName": "Image_Name", "AttributeType": "S"},
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
)
