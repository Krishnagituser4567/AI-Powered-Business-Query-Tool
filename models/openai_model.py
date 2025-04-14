import openai
import os

def query_openai(prompt, model="text-davinci-003"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()