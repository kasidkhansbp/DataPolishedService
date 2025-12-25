from typing import Final
from .enums import ModelName

DOCTOR_NOTES_STRUCTURE_PROMPT: Final[str] = (
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
)

DOCTOR_NOTES_STRUCTURE_REPAIR_PROMPT: Final[str] = (
        "You are a helpful assistant that reviews JSON data extracted from unstructured doctor's notes. "
        "Your task is to identify and correct any formatting errors, missing fields, or inconsistencies in the JSON structure. "
        "Ensure that the final output adheres strictly to the required schema with fields: Id, History, Medications, Vitals, Observations, Symptoms, and Recommendations. "
        "Return only the corrected JSON without any additional commentary."
    )

class RepairConfig:
    model: Final[str] = ModelName.GPT4O_MINI.value
    max_output_tokens: Final[int] = 300
    temperature: Final[float] = 0.0