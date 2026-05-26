from groq import Groq
import json, os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM = """You are a system design engine for a software compiler.
Convert structured intent JSON into application architecture.
Respond ONLY with valid JSON matching this exact schema:
{
  "entities": [
    {
      "name": "string",
      "fields": [{"name": "string", "type": "string", "required": "true"}],
      "relations": ["related entity names"]
    }
  ],
  "flows": ["key business flows"],
  "roles": ["list of roles"],
  "permissions": {
    "role_name": ["list of allowed actions"]
  }
}
No preamble. No markdown. No backticks. Pure JSON only."""

def design_system(intent: dict) -> dict:
    response = client.chat.completions.create(
        model="llama3-70b-8192", max_tokens=4000,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(intent)}
        ]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)