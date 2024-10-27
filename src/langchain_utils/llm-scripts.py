import openai

def generate_structured_data(input_text):
    prompt = (f"Convert the following unstructured doctor’s notes into a structured format with the following categories: Symptoms, History, Medications, Vitals, Observations, and Recommendations. "
              f"Use complete sentences where necessary and organize the information logically under each category.Unstructured Notes: '{input_text}'. "
              f"Format: Symptoms, History, Medications, Vitals, Observations, Recommendation")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

structured_data = generate_structured_data("Pt c/o chest pain x3 days, worse on exertion, radiates to L arm. Hx of HTN and DM. Meds: metoprolol, insulin. BP 150/90, HR 88. Lungs clear, heart S1S2 with no murmurs. EKG shows mild ST elevation. Recommend cardiac consult and troponin levels q6h. Pt advised to avoid strenuous activity.")
print(structured_data)