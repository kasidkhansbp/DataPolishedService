import os

import openai
import os

def generate_structured_data(input_text):
    print("inside generate_structured_data ")
    openai.api_key = os.getenv('OPENAI_API_KEY')

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
    return response.choices[0].message.content.strip()

#structured_data = generate_structured_data("Pt c/o chest pain x3 days, worse on exertion, radiates to L arm. Hx of HTN and DM. Meds: metoprolol, insulin. BP 150/90, HR 88. Lungs clear, heart S1S2 with no murmurs. EKG shows mild ST elevation. Recommend cardiac consult and troponin levels q6h. Pt advised to avoid strenuous activity.")
#print(structured_data)