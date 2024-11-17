import re
import logging
import json
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')
def clean_text(text):
    if text is None:
        logging.error("Input text is None. Please provide a valid string.")
        raise ValueError("Input text is None. Please provide a valid string")

    logging.info("cleaning text...")
    # Remove punctuation and special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    # Convert to lowercase
    text = text.lower()

    cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'Figure \d+', '', cleaned_text)  # Remove figure references
    cleaned_text = re.sub(r'Image \d+', '', cleaned_text)  # Remove image references
    cleaned_text = cleaned_text.strip()  # Remove leading/trailing spaces
    logging.info("Text cleaning completed.")
    return cleaned_text

def clean_response(text):
    # Remove code block markers (` ```json ` and trailing backticks)
    if text.startswith("```json"):
        text = text[7:].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    if text.endswith(",,,"):  # Remove trailing `,,,`
        text = text[:-3].strip()
    data = json.loads(text)
    # DynamoDB expect Id as a partition key
    data["Id"] = str(uuid.uuid4())
    return data


