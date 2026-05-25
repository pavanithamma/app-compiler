from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time

from pipeline.stage1_intent import extract_intent
from pipeline.stage2_design import design_system
from pipeline.stage3_schema import generate_schema
from pipeline.stage4_validator import validate_and_repair

app = FastAPI(title="App Compiler")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/compile")
async def compile_app(req: PromptRequest):
    start = time.time()
    stages = {}

    intent = extract_intent(req.prompt)
    stages["intent"] = intent

    design = design_system(intent)
    stages["design"] = design

    schema = generate_schema(intent, design)
    stages["schema_raw"] = schema

    final_schema, errors = validate_and_repair(schema)
    stages["schema_final"] = final_schema

    return {
        "success": len(errors) == 0,
        "stages": stages,
        "validation_errors": errors,
        "assumptions": intent.get("assumptions", []),
        "latency_seconds": round(time.time() - start, 2)
    }

@app.get("/health")
def health():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")