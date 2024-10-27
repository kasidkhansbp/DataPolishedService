import re

def clean_text(text):
    # Remove punctuation and special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    # Convert to lowercase
    text = text.lower()

    cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'Figure \d+', '', cleaned_text)  # Remove figure references
    cleaned_text = re.sub(r'Image \d+', '', cleaned_text)  # Remove image references
    cleaned_text = cleaned_text.strip()  # Remove leading/trailing spaces
    return cleaned_text
