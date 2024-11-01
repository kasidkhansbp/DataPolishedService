import boto3

def read_s3_bucket(bucket_name, file_key):
    # Specify the profile to use
    session = boto3.Session(profile_name="my-profile")
    s3_client = session.client('s3')
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        return file_content
    except Exception as e:
        print(f"Error reading the file from s3:{e}")


