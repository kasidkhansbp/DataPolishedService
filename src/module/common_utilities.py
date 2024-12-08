import logging
import json

import boto3
import botocore.exceptions

from data_processing.clean_scripts import clean_text
from langchain_utils.llm_scripts import generate_structured_data
from storage.dynamodb_builder import DynamoDBBuilder


class CommonUtilities:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    def __init__(self):
        self.s3_client = boto3.client('s3')

    # code for init method with boto3 object initiation

    def process_sqs_batch_response(self, event, context):
        failed_messages = []
        for record in event['Records']:
            message_id = record['messageId']
            body = record['body']
            try:
                logging.info(f"Processing message ID: {message_id} with body: {body}")
                # Add message processing logic here
                # Read the S3 file in chunks and return clean data.
                file_contents = self.return_clean_s3_data(body)
                logging.info(f"File contents fetched successfully.")
                # Process the file contents
                self.process_sqs_record(file_contents)
            except Exception as e:
                logging.info(f"Failed to processing message ID: {message_id} Error: {str(e)}")
                # add the message ID to failure list
                failed_messages.append({"itemIdentifier": message_id})
        # Return the batch item failures (required for partial batch response). Enable partial batch response.
        return {"batchItemFailures": failed_messages}

    # Extract S3 file path
    def get_s3_filepath(self, body):
        """
            Extract the S3 bucket name and object key from the SQS message body.
            Assumes the body is JSON with an embedded S3 event structure.
        """
        body_data = json.loads(body)
        s3_event = body_data['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']
        return {"bucket_name": bucket_name, "object_key": object_key}

    # read S3 file and return the clean text
    def read_s3_file(self, body):
        s3_filepath = self.get_s3_filepath(body)
        bucket_name = s3_filepath['bucket_name']
        file_path = s3_filepath['object_key']
        logging.info(f"Fetching file from S3 bucket name: {bucket_name}, file_path: {file_path}")
        try:
            response = self.s3_client.get_paginator(Bucket=bucket_name, Key=file_path)
            file_stream = response['Body']
            # stream the file in chunks
            file_contents = ""
            for chunk in file_stream.iter_lines():
                file_contents += chunk.decode('utf-8') + "\n"
            return file_contents

        except botocore.exceptions.ClientError as e:
            logging.error(f"Error fetching file from S3. Error: {str(e)}")
            raise
        except Exception as e:
            logging.info(f"Unexpected error while reading the file. Error: {str(e)}")
            raise

    # clean the content file for punctuation, multiple spaces or special characters
    def return_clean_s3_data(self, body):
        return clean_text(self.read_s3_file(body))

    # send the cleaned data to LLM and store the response in DDB
    def process_sqs_record(self, text):
        response = generate_structured_data(text)
        return DynamoDBBuilder.set_region('us-west-2').connect_to_dynamodb().find_table("dynamodb-test").insert_item(
            response)
