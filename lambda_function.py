#!/usr/local/bin/python3

"""

This script was made by Madani Napaul. 

This script is the Lambda function which:

        - Extracts relevant details from the SQS messages 
        - Uses image names extracted to call AWS Rekognition PPE Detection to analyze
          the images with exact names in the S3 Bucket 
        - Manipulate the response and prepare the data to store it in the DynamoDB Table 
        - Stores the responses in the DynamoDB Table 'PPE_Detection'
        - Sends an SMS to a specified phone number with the Body Parts detected

"""
# Import the required libraries
import json
import boto3


def lambda_handler(event, context):

    # Create the required resources
    ppe_client = boto3.client("rekognition")
    sns_client = boto3.client("sns")

    # Load the messages from the SQS Queue into JSON Objects
    for msg in event["Records"]:
        msg_payload = json.loads(msg["body"])

        # If there are 'Records' in the messages; the messages are not empty
        # Extract the bucket name and the image name
        # Request AWS Rekognition PPE Detection to analyze images in the S3 Bucket with the extracted image names
        # Set the Required Equipment Types to 'FACE_COVER' and 'HEAD_COVER'
        # Set the Minimum Confidence
        if "Records" in msg_payload:
            bucket = msg_payload["Records"][0]["s3"]["bucket"]["name"]
            image = msg_payload["Records"][0]["s3"]["object"]["key"].replace("+", " ")
            response = ppe_client.detect_protective_equipment(
                Image={"S3Object": {"Bucket": bucket, "Name": image}},
                SummarizationAttributes={
                    "MinConfidence": 75,
                    "RequiredEquipmentTypes": ["FACE_COVER", "HEAD_COVER"],
                },
            )

            # Access the body parts of all persons detected from AWS Rekognition PPE Detection
            # Create a dictionary 'result' where the data will be constantly appended
            for person in response["Persons"]:
                body_parts = person["BodyParts"]
                result = {"Content": []}

                # Access the Equipment Detected of the response
                for equip_details in body_parts:
                    name = equip_details["Name"]
                    ppe = equip_details["EquipmentDetections"]

                    # We prepare the data we read from above to output to a file or store in a database
                    data = {"Body Part": name, "Equipment": str(ppe)}

                    # From the empty result dictionary above, we append the data we prepared from the step before
                    # Now the data is ready to be stored in the database in the format we specified
                    result["Body"].append(data)

                    # Create the resource for dynamodb and set the table in which we want to store the data
                    # Image_Name here is the primary key we declared whilst creating the table, and it's required
                    # 'Body' contains the content which belongs to that primary key
                    table = boto3.resource("dynamodb").Table("dynamodb-cpd-2021")
                    table.put_item(Item={"Image_Name": image, "Body": result})

                    # Ensure you have attached 'AWSLambdaBasicExecutionRole' & 'SNS: Publish'
                    # If you exceed your $1 limit, contact AWS Support Team and request for an upgrade (Check SNS)
                    # We will be sending only the file name here, for demonstration purposes
                    number = "+ZZ- ZZZZZZZ"
                    message = image
                    sns_client.publish(PhoneNumber=number, Message=str(message))

    return {"statusCode": 200}
