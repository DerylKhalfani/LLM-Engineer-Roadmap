from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model = 'gpt-5-nano',
    instructions = 'Generate text with question and answer style based on the content provided, and answer within 100 words',
    input = 'How do i connect backend to frontend in fastapi?',
    reasoning = {'effort':'minimal'}
)

print(response.output[1].content[0].text)

def llm_generation(input: str) -> str:
    


