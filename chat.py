from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        { "role": "user", "content": "What is greator? 9.8 or 9.11" } # Zero Shot Prompting
    ]
)

print(result.choices[0].message.content)
