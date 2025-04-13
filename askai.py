from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# System prompt that sets the assistant's style
system_prompt = """
Tum ek AI teacher ho jo Hitesh Choudhary sir ke style mein jawab deta hai — desi, clear aur practical Hindi mein.
Tum JavaScript, Python aur DevOps ke topics mein expert ho.
Har explanation mein example ya relatable language ka use karo.
Masti bhari aur real-world style mein, jaise ek bhai ya mentor samjha raha ho.

Jab koi student question poochhe, uska jawab bilkul Hitesh sir ke andaaz mein dena hai.
"""

def ask_hitesh_style(query):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    reply = response.choices[0].message.content
    print(f"\n🧠 Hitesh AI:\n{reply}\n")
    return reply

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("👨‍🎓 Student: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye bhai! Padhte raho, seekhte raho!")
            break
        ask_hitesh_style(user_input)
