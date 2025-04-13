from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyAGxd4MK7ZiMLO61jKA7QJnNnmDdFRKnw0')

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)