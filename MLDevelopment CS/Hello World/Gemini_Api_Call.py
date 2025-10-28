from google import genai
import os

client = genai.Client(
    api_key ="AIzaSyByBKPJjlrIZFXkZatEMoMm9p1GTPoKE_c"
)

response = client.models.generate_content(
    model = "gemini-2.5-flash",contents = "Explain how AI works in a few words"
)

print(response.text)  