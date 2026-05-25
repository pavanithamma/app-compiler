from groq import Groq
import json, os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM = """You are a schema generation engine for a software compiler.
Convert intent + design into full UI/API/DB/Auth schemas.
Respond ONLY with valid JSON matching this exact schema:
{
  "api": [
    {
      "path": "/example",
      "method": "GET",
      "auth_role": "admin",
      "request_body": {"field": "type"},
      "response": {"field": "type"}
    }
  ],
  "db": [
    {
      "table": "string",
      "columns": [{"name": "string", "type": "string", "constraints": "string"}],
      "relations": ["list"]
    }
  ],
  "ui": [
    {
      "page": "string",
      "route": "/path",
      "role_access": ["role1"],
      "components": ["component names"]
    }
  ],
  "auth": {
    "roles": ["list"],
    "permissions": {"role": ["actions"]}
  }
}
No preamble. No markdown. No backticks. Pure JSON only."""

def generate_schema(intent: dict, design: dict) -> dict:
    payload = {"intent": intent, "design": design}
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(payload)}
        ]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)