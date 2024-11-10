import logging
import os

import openai
import os

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
            f"Convert the following unstructured doctor’s notes into a structured JSON format with the following categories: "
            f"Symptoms, History, Medications, Vitals, Observations, and Recommendations. "
            f"Use complete sentences where necessary and organize the information logically under each category. "
            f"Unstructured Notes: '{input_text}'. "
            f"Return the output as JSON with fields: Symptoms, History, Medications, Vitals, Observations, Recommendations."
            )
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant that extracts information from unstructured notes and returns data in JSON format."},
                  {"role": "user", "content": prompt}],
            max_tokens=300
        )
        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        logging.error(f"Error during structured data generation: {e}")
        raise
