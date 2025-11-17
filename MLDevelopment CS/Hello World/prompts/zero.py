#zero shot prompting - a technique where the model is given a task without any examples, relying solely on its pre-trained knowledge and the instruction provided in the prompt
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

genai_key = os.getenv("GENAI_API_KEY")
if not genai_key:
    raise RuntimeError("GENAI_API_KEY is not set in the environment")

client = OpenAI(
    api_key=genai_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT = "you are an expert in Maths and only and only ans maths related questions. If any question comes that is not realated to math then just say sorry and do not answer the question !Your name is 'Alisha'"

response = client.chat.completions.create(
    model = "gemini-2.5-flash",
    messages=[
        {"role": "system", "content" : SYSTEM_PROMPT},
        {"role": "user","content": "Hey There, tell me a recipe please ?"}
    ]       
)

print(response.choices[0].message.content)