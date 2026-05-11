from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from tools import research_tools
import os
from dotenv import load_dotenv

load_dotenv()

def create_research_agent():
    # 1. Khởi tạo LLM 
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
    
    # 2. Định nghĩa System Prompt để hướng dẫn cách Agent hoạt động
    system_prompt = """
    Bạn là một trợ lý nghiên cứu thị trường xuất sắc. Nhiệm vụ của bạn là:
    1. Dùng tool 'internet_search' để tìm kiếm thông tin.
    2. Dùng tool 'scrape_webpage' để đọc sâu vào các đường link quan trọng vừa tìm được.
    3. Đọc, tổng hợp thông tin, loại bỏ các tin rác.
    4. Nếu thấy thông tin chưa đủ, hãy tự động tìm kiếm với từ khóa khác.
    5. Cuối cùng, trình bày báo cáo bằng Markdown rõ ràng, chia đề mục chi tiết.
    """
    
    # 3. Kết hợp LLM và Tools vào LangGraph
    # create_react_agent tự động tạo ra một Graph gồm Node suy luận và Node thực thi Tool
    agent_executor = create_agent(
        model=llm,
        tools=research_tools,
        system_prompt=system_prompt
    )
    
    return agent_executor