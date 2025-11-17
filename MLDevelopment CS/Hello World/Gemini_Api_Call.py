from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

genai_key = os.getenv("GENAI_API_KEY")
if not genai_key:
    raise RuntimeError("GENAI_API_KEY is not set in the environment")

client = genai.Client(
    api_key=genai_key
)

response = client.models.generate_content(
    model = "gemini-2.5-flash",contents = "Explain how AI works in a few words"
)

print(response.text)  