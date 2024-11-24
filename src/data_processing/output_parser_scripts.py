from langchain.output_parsers import BaseOutputParser
import json

class DynamoDBOutputParser(BaseOutputParser):
    def __init__(self):
        # Define the schema with default values as null
        self.schema = {
            "Symptoms": {"L": [{"S": None}]},
            "History": {"M": {"hypertension": {"S": None}, "diabetes_mellitus": {"S": None}}},
            "Medications": {"L": [{"S": None}]},
            "Vitals": {"M": {"blood_pressure": {"S": None}, "heart_rate": {"N": None}}},
            "Observations": {"M": {"lungs": {"S": None}, "heart_sounds": {"S": None}, "ekg": {"S": None}}},
            "Recommendations": {"L": [{"S": None}]}
        }

    def parse(self, text: str):
        # Assume `text` is the unstructured doctor’s note or LLM output
        try:
            parsed_data = json.loads(text)  # You can adjust this parsing as per the LLM output structure
        except json.JSONDecodeError:
            parsed_data = {}

        # Apply schema and populate fields based on parsed data, filling missing data with `null`
        for key, value in self.schema.items():
            if key in parsed_data:
                if isinstance(value, dict):  # Handle map type
                    self.schema[key] = self._parse_map(key, value, parsed_data[key])
                elif isinstance(value, list):  # Handle list type
                    self.schema[key] = self._parse_list(key, parsed_data[key])
            else:
                # Fill missing fields with null values or default schema values
                self.schema[key] = value

        return self.schema

    def _parse_map(self, key, value, data):
        # Iterate over the expected schema keys and their nested structure
        for subkey, subvalue in value.items():
            if isinstance(subvalue, dict):  # Handle nested maps (e.g. "hypertension": {"S": "Yes"})
                # Check if subkey exists in the actual data and ensure it's populated correctly
                if subkey in data:
                    self.schema[key][subkey] = {"S": data[subkey]} if isinstance(data[subkey], str) else data[subkey]
                else:
                    # If the subkey is missing in data, set it to a default value (e.g. None or empty dict)
                    self.schema[key][subkey] = {"S": None}
            else:
                # For non-nested values (like strings or numbers)
                if subkey in data:
                    self.schema[key][subkey] = {"S": data[subkey]} if isinstance(data[subkey], str) else {
                        "N": data[subkey]}
                else:
                    self.schema[key][subkey] = {"S": None}  # Handle missing data
        return self.schema[key]

    def _parse_list(self, key, data):
        # Parse the list and fill missing values with null
        for idx, item in enumerate(data):
            self.schema[key][idx] = {"S": item} if item else {"S": None}
        return self.schema[key]