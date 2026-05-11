from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from dotenv import load_dotenv


# ---------------------------
# LLM
# ---------------------------
def get_llm(model_name="llama-3.1-8b-instant"):
    """Initializes the LLM instance."""
    return ChatGroq(model=model_name, temperature=0.5)


# ---------------------------
# Research Agent
# ---------------------------
def create_researcher(llm):
    """
    Creates a Tool-calling Agent for news gathering.
    In v1.0, 'system_prompt' is the correct keyword for instructions.
    """
    search_tool = TavilySearch(max_results=3)

    return create_agent(
        model=llm,
        tools=[search_tool],
        system_prompt=(
            "You are a senior news researcher. "
            "Find the most relevant facts on the topic provided."
        )
    )


# ---------------------------
# Writer Agent
# ---------------------------
def create_writer(llm):
    """
    Creates a creative Agent for blog writing.
    Even without tools, using create_agent keeps the I/O format consistent.
    """
    return create_agent(
        model=llm,
        tools=[],
        system_prompt=(
            "You are a professional tech blogger. "
            "Transform raw research into a viral blog post."
        )
    )


# ---------------------------
# Pipeline
# ---------------------------
def run_blog_pipeline(topic: str):
    # Make sure API keys are loaded
    load_dotenv()

    # Initialize agents
    llm = get_llm()
    researcher = create_researcher(llm)
    writer = create_writer(llm)

    # ---- Phase 1: Research ----
    print(f"🚀 Phase 1: Researching '{topic}'...")
    research_output = researcher.invoke({
        "messages": [
            HumanMessage(content=f"Research the latest news on: {topic}")
        ]
    })

    research_data = research_output["messages"][-1].content

    # ---- Phase 2: Writing ----
    print("📝 Phase 2: Generating Blog Post...")
    final_output = writer.invoke({
        "messages": [
            HumanMessage(
                content=f"Based on this research, write a blog post:\n\n{research_data}"
            )
        ]
    })

    return final_output["messages"][-1].content


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    target_topic = "Research on the state of AI Agents in 2026"

    blog_post = run_blog_pipeline(target_topic)

    print("\n" + "=" * 50)
    print("FINAL BLOG POST")
    print("=" * 50 + "\n")
    print(blog_post)