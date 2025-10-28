#zero shot prompting - a technique where the model is given a task without any examples, relying solely on its pre-trained knowledge and the instruction provided in the prompt
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="AIzaSyByBKPJjlrIZFXkZatEMoMm9p1GTPoKE_c",
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