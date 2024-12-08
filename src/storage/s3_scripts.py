import boto3
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')

def read_s3_bucket(bucket_name, file_key):
    try:
        logging.info(f"Attempting to read file {file_key} from bucket {file_key}")

        # Specify the profile to use
        session = boto3.Session(profile_name="my-profile")
        s3_client = session.client('s3')

        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        logging.info("File read successfully.")
        return file_content

    except NoCredentialsError:
        logging.error("AWS credentials are missing or invalid.")
        raise
    except PartialCredentialsError:
        logging.error("Incomplete AWS credential")
        raise
    except Exception as e:
        logging.error(f"Error reading the file from s3:{e}")
        raise



