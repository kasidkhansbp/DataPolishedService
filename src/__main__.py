
from data_processing.clean_scripts import clean_text
from langchain_utils.llm_scripts import generate_structured_data
from storage.dynamodb_builder import DynamoDBBuilder
from storage.s3_scripts import read_s3_bucket

def main():
    text = read_s3_bucket("mybucket-qwertyui","unstructuredData.txt")
    text = clean_text(text)
    response = generate_structured_data(text)
    DynamoDBBuilder.set_region('us-west-2').connect_to_dynamodb().find_table("dynamodb-test").insert_item(response)

if __name__ == "__main__":
    main()