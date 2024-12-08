import logging

class CommonUtilities:

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # code for init method with boto3 object initiation

    def getSQSBatchResponse(self, event, context):
        failed_messages = []
        for record in event['Records']:
            message_id = record['messageId']
            body = record['body']
            try:
                logging.info(f"Processing message ID: {message_id} with body: {body}")
                # Add message processing logic here
                # read record

            except Exception as e:
                logging.info(f"Failed to processing message ID: {message_id} Error: {str(e)}")
                # add the message ID to failure list
                failed_messages.append({"itemIdentifier": message_id})
        # Return the batch item failures (required for partial batch response). Enable partial batch response.
        return {"batchItemFailures": failed_messages}

    # Extract S3 file path
    def get_s3_filepath(self, body):
        return

    # read S3 file and return the clean text
    def get_s3_file(self, s3_filepath):
        return

    # send the cleaned data to LLM and store the response in DDB
    def process_sqs_record(self):
        return



