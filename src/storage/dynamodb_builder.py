import boto3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Usage
# DynamoDBBuilder()
#             .set_region("us-east-1")
#             .connect_to_dynamodb()
#             .find_table("YourTableName")
#             .insert_item(item_to_insert)
class DynamoDBBuilder:
    def __init__(self):
        self.region = None
        self.dynamodb = None
        self.table = None

    @classmethod
    def set_region(self, region):
        logging.info(f"Setting region: {region}")
        self.region = region
        return self

    @classmethod
    def connect_to_dynamodb(self):
        try:
            logging.info(f"Connecting to DynamoDB in region: {self.region}")
            self.dynamodb = boto3.resource("dynamodb",region_name=self.region)
        except Exception as e:
            logging.error(f"Error connecting to DynamoDB: {e}", exc_info=True)
            raise
        return self

    @classmethod
    def find_table(self, table_name):
        try:
            logging.info(f"Finding table: {table_name}")
            if not self.dynamodb:
                raise ValueError(f"DynamoDB connection not established. Call `connect_to_dynamodb` first")
            self.table = self.dynamodb.Table(table_name)
        except Exception as e:
            logging.error(f"Error finding table {table_name}: {e}", exc_info=True)
            raise
        return self

    @classmethod
    def insert_item(self, item):
        try:
            logging.info(f"Inserting item {item}")
            if not self.table:
                raise ValueError(f"Table not set. Call `find_table` first.")
            response = self.table.put_item(Item=item)
            logging.info(f"Item inserted successfully: {response}")
            return response
        except Exception as e:
            logging.error(f"Error inserting item into table: {e}", exc_info=True)
            raise
