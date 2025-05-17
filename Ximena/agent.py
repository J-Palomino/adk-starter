from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

provider = "openrouter"
model = "meta-llama/llama-3.3-8b-instruct:free"
agent_name = "Ximena"
agent_instruction = "You are a master business woman that supports others by validating their ideas"
agent_description = "business woman with MBA from U of I"

root_agent = LlmAgent(
    model=LiteLlm(model=f"{provider}/{model}", llm_provider=provider), # LiteLLM model string format
    name=agent_name,
    instruction=agent_instruction,
    description=agent_description,
    tools=[],
)
