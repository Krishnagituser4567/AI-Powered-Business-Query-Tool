from google import genai
from google.genai import types
import os

def query_gemini(prompt, model="gemini-2.0-flash"):
    """
    Query the Gemini AI model with the given prompt and model name.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model=model,  # Use the model passed dynamically
        config=types.GenerateContentConfig(
            system_instruction="You are a data modeling expert and subject matter expert in SCM, HCM, Finance, Inventory Management. Based on the input metadata and sample data, suggest a dimensional model with fact and dimension tables."
        ),
        contents=prompt
    )
    return response.text