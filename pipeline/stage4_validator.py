from groq import Groq
import json, os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def validate(schema: dict) -> list[str]:
    errors = []
    api = schema.get("api", [])
    db = schema.get("db", [])
    ui = schema.get("ui", [])
    auth = schema.get("auth", {})

    db_tables = {t["table"].lower() for t in db}
    auth_roles = set(auth.get("roles", []))

    for endpoint in api:
        role = endpoint.get("auth_role", "")
        if role and role != "public" and role not in auth_roles:
            errors.append(f"API role '{role}' at {endpoint['path']} not in auth.roles")

    for page in ui:
        for role in page.get("role_access", []):
            if role != "public" and role not in auth_roles:
                errors.append(f"UI page '{page['page']}' has unknown role '{role}'")

    for endpoint in api:
        path_part = endpoint["path"].strip("/").split("/")[0].lower()
        if path_part and path_part not in db_tables and path_part != "auth":
            errors.append(f"API '{endpoint['path']}' has no matching DB table '{path_part}'")

    return errors

REPAIR_SYSTEM = """You are a schema repair engine for a software compiler.
Fix ONLY the broken parts based on the errors listed.
Return the corrected full schema as valid JSON.
No preamble. No markdown. No backticks. Pure JSON only."""

def repair(schema: dict, errors: list[str]) -> dict:
    payload = {"schema": schema, "errors": errors}
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": REPAIR_SYSTEM},
            {"role": "user", "content": json.dumps(payload)}
        ]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def validate_and_repair(schema: dict, max_retries: int = 3) -> tuple[dict, list[str]]:
    for attempt in range(max_retries):
        errors = validate(schema)
        if not errors:
            return schema, []
        schema = repair(schema, errors)
    final_errors = validate(schema)
    return schema, final_errors