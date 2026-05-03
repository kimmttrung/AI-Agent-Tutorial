from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain.tools import tool
import requests

load_dotenv()

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given city."""
    return f"{location.capitalize()} 32°C"

#LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant"
)
#Agent
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="""
You are a weather assistant.

When the user asks about weather:
- You MUST call the get_weather tool
- Do NOT answer directly
- Do NOT say you don't know

Always use the tool.
"""
)

# run
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "what is the weather in hanoi"}
    ]
})

print(result["messages"][-1].content)


