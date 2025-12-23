import logging

import os

from data_processing.clean_scripts import clean_response
from openai import OpenAI

# Create client ONCE (module-level or app startup)
api_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_structured_data(input_text):
    try:
        # ---------- Validation ----------
        if not input_text or not input_text.strip():
            logging.error("Input text is empty.")
            raise ValueError("Input text cannot be empty")

        if not api_client.api_key:
            logging.error("API key not found. Please set OPENAI_API_KEY.")
            raise ValueError("OpenAI API key is required")

        logging.info("starting data generation...")

        # ---------- Prompt ----------
        prompt = (
            "Convert the following unstructured doctor’s notes into a structured JSON format with the following fields: "
            "Id, History, Medications, Vitals, Observations, Symptoms, and Recommendations. "
            "The format should be structured as: "
            "- History: A JSON object where each key is a condition "
            "- Medications: A list of strings representing medication names. "
            "- Observations: A JSON object where each key is an observation type (e.g., 'ekg') and its value is a string description. "
            "- Recommendations: A list of strings, each representing a recommendation. "
            "- Symptoms: A list of strings describing symptoms. "
            "- Vitals: A JSON object with keys for vitals (e.g., 'blood_pressure') and corresponding values. Numbers should be represented as integers where applicable. "
            "Include an 'Id' field at the root level with a unique identifier as a string. "
            "Ensure the output is human-readable and logically organized while maintaining simplicity. "
            "Do not, under any circumstance, make any assumptions regarding existing conditions"
            f"Unstructured Notes: '{input_text}'. "
            "Return the output in this exact structure and format."
        )

        # ---------- OpenAI Responses API ----------
        response = api_client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts information from unstructured notes and returns data in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_output_tokens=300,
            temperature=0
        )
        # ---------- Output handling ----------
        # Preferred: use output_text (safe for non-schema responses)
        output_text = response.output_text

        if not output_text:
            raise ValueError("Model returned empty response")
        return clean_response(output_text)

    except Exception as e:
        logging.error(f"Error during structured data generation: {e}")
        raise
