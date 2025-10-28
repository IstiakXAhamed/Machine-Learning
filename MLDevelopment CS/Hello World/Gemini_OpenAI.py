from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="AIzaSyByBKPJjlrIZFXkZatEMoMm9p1GTPoKE_c",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model = "gemini-2.5-flash",
    messages=[
        {"role": "system", "content" : "you are an expert in Maths and only and only ans maths related questions. If any question comes that is not realated to math then just say sorry and do not answer the question ! "},
        {"role": "user","content": "Hey There, tell me a recipe please ?"}
    ]
)

print(response.choices[0].message.content)