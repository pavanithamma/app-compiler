from groq import Groq
import json, os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM = """You are an intent extraction engine for a software compiler.
Extract structured intent from user prompts.
Respond ONLY with valid JSON matching this exact schema:
{
  "app_type": "string",
  "features": ["list of features"],
  "roles": ["list of user roles"],
  "auth_required": true,
  "payment_required": false,
  "assumptions": ["list of assumptions made for vague inputs"]
}
No preamble. No markdown. No backticks. Pure JSON only."""

def extract_intent(user_prompt: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", max_tokens=4000,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt}
        ]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)