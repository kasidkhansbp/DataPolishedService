import re
import logging

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
