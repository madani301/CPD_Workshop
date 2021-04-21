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
import os

# This function iterates through the files in the given local path
# Each file in that directory is uploaded to the S3 bucket specified
# A similar approach can be used for the coursework by adding the 10s wait time
def upload_files(path):
    session = boto3.Session()
    s3 = session.resource("s3")
    bucket = s3.Bucket("s3-cpd-2021")

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, "rb") as data:
                bucket.put_object(Key=full_path[len(path) + 1 :], Body=data)


if __name__ == "__main__":
    upload_files("/Users/madani/Desktop/cpd_workshop/files")
