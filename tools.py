import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Khởi tạo công cụ gốc
ddg_search = DuckDuckGoSearchRun()

# Gói nó lại vào một Tool tùy chỉnh có bọc try-except
@tool
def internet_search(query: str) -> str:
    """Sử dụng công cụ này để tìm kiếm thông tin mới nhất trên mạng. Cố gắng dùng từ khóa tiếng Anh nếu tiếng Việt không ra kết quả."""
    try:
        # Gọi tìm kiếm
        return ddg_search.invoke(query)
    except Exception as e:
        # Thay vì văng lỗi làm sập chương trình, trả về chuỗi text báo lỗi cho Agent biết
        return f"Hệ thống tìm kiếm đang quá tải hoặc lỗi mạng. Lỗi chi tiết: {str(e)}. Hãy thử lại bằng một từ khóa khác hoặc từ khóa tiếng Anh ngắn gọn hơn."

@tool
def scrape_webpage(url: str) -> str:
    """
    Sử dụng công cụ này để truy cập vào một URL cụ thể và đọc toàn bộ nội dung văn bản.
    """
    try:
        # Gia lập
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # requests để gọi HTTP
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # kiểm tra lỗi
        print(response)
        
        soup = BeautifulSoup(response.text, "html.parser") # Doc file html
        
        # Loại bổ phầm k cần thiết
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        return text[:2000] 
    except Exception as e:
        return f"Lỗi khi đọc trang web {url}: {str(e)}"

# Cập nhật mảng tools với tool internet_search mới
research_tools = [internet_search, scrape_webpage]