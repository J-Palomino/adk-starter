import os
import re
import shutil
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException

app = FastAPI()

AGENT_TEMPLATES_DIR = Path(__file__).parent.resolve()
OPENROUTER_STARTER_DIR = AGENT_TEMPLATES_DIR / "agents"

@app.get("/")
def read_root():
    return {"message": "Welcome to the ADK Starter Server!"}

@app.get("/agent_templates", response_model=List[str])
def list_templates():
    # List all agent template directories in the agents directory
    agents_dir = AGENT_TEMPLATES_DIR / "agents"
    if not agents_dir.exists():
        return []
    templates = [f.name for f in agents_dir.iterdir() if f.is_dir() and not f.name.startswith('__')]
    return templates

@app.post("/new_agent/{agent_name}")
async def new_agent(agent_name: str, model: str, instruction: str, description: str):
    # Validate agent name
    if not re.match(r'^[a-zA-Z0-9_-]+$', agent_name):
        raise HTTPException(status_code=400, detail="Invalid agent name. Use only letters, numbers, underscores, or hyphens.")
    
    new_agent_dir = AGENT_TEMPLATES_DIR / agent_name
    
    # Debug: Check directory permissions
    try:
        if not os.access(AGENT_TEMPLATES_DIR, os.W_OK):
            raise HTTPException(
                status_code=500,
                detail=f"No write permission in directory: {AGENT_TEMPLATES_DIR}"
            )
            
        if new_agent_dir.exists():
            raise HTTPException(status_code=400, detail=f"Agent directory '{agent_name}' already exists")
            
        # Create the new agent directory
        os.makedirs(new_agent_dir, exist_ok=True)
        
        # Ensure the directory is writable
        if not os.access(new_agent_dir, os.W_OK):
            raise HTTPException(
                status_code=500,
                detail=f"Cannot write to directory: {new_agent_dir}"
            )
            
        # Copy template files
        shutil.copytree(OPENROUTER_STARTER_DIR, new_agent_dir, dirs_exist_ok=True)
        
        # Update agent configuration
        update_agent_py(new_agent_dir, "openrouter", model, agent_name, instruction, description)
        
        return {"status": "created", "agent_dir": str(new_agent_dir)}
        
    except HTTPException:
        raise
    except FileExistsError:
        raise HTTPException(status_code=400, detail=f"Agent directory '{agent_name}' already exists")
    except PermissionError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Permission denied when creating agent: {str(e)}"
        )
    except Exception as e:
        # Clean up partially created directory if something went wrong
        if new_agent_dir.exists():
            shutil.rmtree(new_agent_dir, ignore_errors=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create agent: {str(e)}"
        )


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