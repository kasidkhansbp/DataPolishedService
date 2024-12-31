
from module.common_utilities import CommonUtilities

def lambda_handler(event, context):
    util = CommonUtilities()
    util.process_sqs_batch_response(event, context)

if __name__ == "__main__":
    lambda_handler()