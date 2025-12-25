import logging

import os

from data_processing.clean_scripts import clean_response
from openai import OpenAI
import logging
from pydantic import ValidationError
from src.models.model import DoctorNotes
from src.module.enums import V
from src.module.prompts import DOCTOR_NOTES_STRUCTURE_REPAIR_PROMPT, DOCTOR_NOTES_STRUCTURE_PROMPT

REPAIR_MODEL = "gpt-4o-mini"
# Create client ONCE (module-level or app startup)
api_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_structured_data_validated(input_text):
    """
    Validate the cleaned JSON produced by generate_structured_data using Pydantic.
    On ValidationError, ask the model to repair the JSON up to MAX_RETRIES, then
    persist failures for human review.
    Returns a dict (validated and coerced) on success or raises on terminal failure.
    """
    # initial call to existing function that prepares the JSON string
    current_json = generate_structured_data(input_text)

    for attempt in range(1, V.MAX_RETRIES + 1):
        try:
            # Validate and parse the JSON using Pydantic
            validated_data = DoctorNotes.model_validate(current_json)
            return validated_data.model_dump()  # Return as dict on success
        except ValidationError as ve:
            logging.warning(f"Validation error on attempt {attempt}: {ve}")
            if attempt == V.MAX_RETRIES:
                logging.error("Max retries reached. Persisting invalid JSON for review.")
                with open("invalid_jsons.log", "a") as f:
                    f.write(current_json + "\n")
                raise

            # Call the model to repair the JSON
            response = api_client.responses.create(
                model= REPAIR_MODEL,
                input=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that repairs JSON data to conform to a specified schema."
                    },
                    {
                        "role": "user",
                        "content": DOCTOR_NOTES_STRUCTURE_REPAIR_PROMPT
                    }
                ],
                max_output_tokens=300,
                temperature=0
            )
            current_json = response.output_text  # Update current_json for the next iteration

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
                    "content": DOCTOR_NOTES_STRUCTURE_PROMPT
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
