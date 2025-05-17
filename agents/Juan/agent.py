from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

provider = "openrouter"
model = "mistral/ministral-8b"
agent_name = "Juan"
agent_instruction = "help the user be awesome"
agent_description = "be the most awesome"

root_agent = LlmAgent(
    model=LiteLlm(model=f"{provider}/{model}", llm_provider=provider), # LiteLLM model string format
    name=agent_name,
    instruction=agent_instruction,
    description=agent_description,
    tools=[],
)
