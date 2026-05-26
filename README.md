# ⚡ App Compiler — AI Engineer Internship Submission

A multi-stage LLM pipeline that compiles natural language into validated, executable app configurations — inspired by how a compiler transforms source code into machine code.

## 🔗 Live Demo
**https://app-compiler-production.up.railway.app**

## 🧠 What It Does
Type a natural language description like *"Build a CRM with login, contacts, dashboard, role-based access for admin and user"* and the system produces a fully validated, cross-layer consistent app configuration ready for runtime execution.

## 🏗️ Architecture

Natural Language Prompt
↓
[Stage 1] Intent Extractor     → app_type, features, roles, assumptions
↓
[Stage 2] System Designer      → entities, flows, permissions
↓
[Stage 3] Schema Generator     → UI + API + DB + Auth JSON
↓
[Stage 4] Validator + Repairer → cross-layer checks + targeted repair
↓
Validated App Config (Ready for Runtime)

## 🔍 Key Design Decisions

### Multi-Stage Pipeline
Each stage is an isolated module with its own system prompt and schema contract. This mirrors compiler design — separation of concerns, clear interfaces between stages.

### Targeted Repair (Not Brute Retry)
When Stage 4 finds a validation error, it repairs **only the broken layer** — not the entire pipeline. For example, a missing DB table triggers a DB schema repair without re-running Stage 1 intent extraction. This is intelligent repair vs brute retry.

### Cross-Layer Consistency Rules
- Every API endpoint role must exist in `auth.roles`
- Every UI page role must match `auth.roles`
- Every API path must have a matching DB table

### Schema-First Design
All stage outputs are validated against strict JSON schemas before being passed to the next stage, ensuring type safety at every boundary.

## 📊 Evaluation Metrics
The system tracks per-request:
- Latency (seconds)
- Validation errors found
- Repair attempts made
- Runtime readiness status

## 🧪 Test Cases
20 test cases in `evaluation/test_cases.json`:
- 10 normal prompts (CRM, e-commerce, HR tool, etc.)
- 10 edge cases (vague inputs, conflicting requirements, incomplete prompts)

## 🛠️ Tech Stack
| Layer | Tool |
|-------|------|
| Backend | Python + FastAPI |
| LLM | Groq API (llama-3.3-70b-versatile) |
| Validation | Custom cross-layer rule engine |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Railway |

## 🚀 Setup

```bash
git clone https://github.com/pavanithamma/app-compiler
cd app-compiler
pip install -r requirements.txt
# Add GROQ_API_KEY to .env
uvicorn main:app --reload
```

## 📁 File Structure

app-compiler/
├── main.py                  # FastAPI app
├── pipeline/
│   ├── stage1_intent.py     # Intent extraction
│   ├── stage2_design.py     # System design
│   ├── stage3_schema.py     # Schema generation
│   └── stage4_validator.py  # Validation + repair
├── frontend/
│   └── index.html           # UI
├── evaluation/
│   └── test_cases.json      # 20 test cases
└── requirements.txt

## 💡 What Separates This System
Most approaches use a single prompt → JSON output. This system is modular with isolated stages, a dedicated validation layer, and proof that repair is targeted — **Stage 3 DB schema repair does not re-run Stage 1 intent extraction.**