
from module.common_utilities import CommonUtilities

def main(event, context):
    CommonUtilities.process_sqs_batch_response(event)

if __name__ == "__main__":
    main()