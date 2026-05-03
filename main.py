from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")


agent = create_agent(
    model=model,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
    tools=[]
)

response = agent.invoke({
    "messages": [
        ("user", "What is the capital of Viet Nam")
    ]
})

print(response)
print(response["messages"][-1].content)