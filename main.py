from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import List
import shutil
import re

app = FastAPI()

AGENT_TEMPLATES_DIR = Path(__file__).parent.resolve()
OPENROUTER_STARTER_DIR = AGENT_TEMPLATES_DIR / "openrouter-starter"

@app.get("/")
def read_root():
    return {"message": "Welcome to the ADK Starter Server!"}

@app.get("/agent_templates", response_model=List[str])
def list_templates():
    files = [f.name for f in AGENT_TEMPLATES_DIR.glob("*.py") if f.is_file() and f.name != "main.py"]
    return files

@app.post("/new_agent/{agent_name}")
def new_agent(agent_name: str, model: str, instruction: str, description: str):
    new_agent_dir = AGENT_TEMPLATES_DIR / agent_name
    if new_agent_dir.exists():
        raise HTTPException(status_code=400, detail="Agent directory already exists")
    try:
        shutil.copytree(OPENROUTER_STARTER_DIR, new_agent_dir)
        update_agent_py(new_agent_dir, "openrouter", model, agent_name, instruction, description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")
    return {"status": "created", "agent_dir": str(new_agent_dir)}


def update_agent_py(agent_dir, provider, model, agent_name, agent_instruction, agent_description):
    agent_py = Path(agent_dir) / "agent.py"
    content = agent_py.read_text()
    replacements = {
        'provider = ': f'provider = "{provider}"',
        'model = ': f'model = "{model}"',
        'agent_name = ': f'agent_name = "{agent_name}"',
        'agent_instruction = ': f'agent_instruction = "{agent_instruction}"',
        'agent_description = ': f'agent_description = "{agent_description}"',
    }
    for key, value in replacements.items():
        content = re.sub(rf'{key}.*', value, content)
    agent_py.write_text(content)