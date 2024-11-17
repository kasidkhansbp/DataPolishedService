import logging
import os

import openai
import os

from data_processing.clean_scripts import clean_response


def generate_structured_data(input_text):
    try:
        if not input_text:
            logging.error("Input text is empty.")
            raise ValueError("Input text cannot be empty")

        logging.info("starting data generation...")
        openai.api_key = os.getenv('OPENAI_API_KEY')

        if not openai.api_key:
            logging.error("API key not found. Please set the OPENAI_API_KEY environment variable")
            raise ValueError("OpenAI API key is required")

        prompt = (
            "Convert the following unstructured doctor’s notes into a structured JSON format with the following categories: "
            "Symptoms, History, Medications, Vitals, Observations, and Recommendations. "
            "Each field should be formatted as per DynamoDB's data types, where: "
            "- Strings are represented as {'S': 'value'}, "
            "- Numbers as {'N': 'value'}, "
            "- Lists as {'L': [{'S': 'value1'}, {'S': 'value2'}]}, "
            "- Nested objects as {'M': {'field1': {'S': 'value1'}, 'field2': {'N': 'value2'}}}. "
            "Ensure all information is logically organized and use complete sentences where necessary. "
            f"Unstructured Notes: '{input_text}'. "
            "Return the output as DynamoDB-compatible JSON with fields: Symptoms, History, Medications, Vitals, Observations, Recommendations."
        )

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant that extracts information from unstructured notes and returns data in JSON format."},
                  {"role": "user", "content": prompt}],
            max_tokens=300
        )
        result = clean_response(response.choices[0].message.content.strip())
        return result

    except Exception as e:
        logging.error(f"Error during structured data generation: {e}")
        raise
