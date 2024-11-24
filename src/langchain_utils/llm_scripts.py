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
            "Convert the following unstructured doctor’s notes into a structured JSON format with the following fields: "
            "Id, History, Medications, Vitals, Observations, Symptoms, and Recommendations. "
            "The format should be structured as: "
            "- History: A JSON object where each key is a condition (e.g., 'diabetes_mellitus') and its value is a string (e.g., 'Yes'). "
            "- Medications: A list of strings representing medication names. "
            "- Observations: A JSON object where each key is an observation type (e.g., 'ekg') and its value is a string description. "
            "- Recommendations: A list of strings, each representing a recommendation. "
            "- Symptoms: A list of strings describing symptoms. "
            "- Vitals: A JSON object with keys for vitals (e.g., 'blood_pressure') and corresponding values. Numbers should be represented as integers where applicable. "
            "Include an 'Id' field at the root level with a unique identifier as a string. "
            "Ensure the output is human-readable and logically organized while maintaining simplicity. "
            f"Unstructured Notes: '{input_text}'. "
            "Return the output in this exact structure and format."
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
