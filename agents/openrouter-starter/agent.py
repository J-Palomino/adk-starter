from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import datetime
from zoneinfo import ZoneInfo

provider = "openrouter"
model = "mistral/ministral-8b"
agent_name = "openrouter_agent"
agent_instruction = f"You are a helpful assistant powered by {model}"
agent_description = "Agent to answer questions about the recipes for catering orders."

def get_current_time(city: str) -> dict:
   
    now = datetime.datetime.now()
    report = (
        f'The current time in Phoenix is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = LlmAgent(
    model=LiteLlm(model=f"{provider}/{model}", llm_provider=provider), # LiteLLM model string format
    name=agent_name,
    instruction=agent_instruction,
    description=agent_description,
    tools=[get_current_time],
)
