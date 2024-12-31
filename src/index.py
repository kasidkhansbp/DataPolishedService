
from module.common_utilities import CommonUtilities

def lambda_handler():
    util = CommonUtilities()
    util.process_local_file("C:\\Users\\kasid\\Downloads\\unstructuredData.txt")
    #CommonUtilities.process_sqs_batch_response(event)

if __name__ == "__main__":
    lambda_handler()