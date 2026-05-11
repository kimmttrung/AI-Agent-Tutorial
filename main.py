from agent import create_research_agent
import datetime

def main():
    print("Đang khởi tạo Agent Nghiên cứu...")
    agent = create_research_agent()
    
    # Chủ đề bạn muốn nghiên cứu
    topic = "Tổng hợp kiến thức về SQL injection ."
    print(f"Bắt đầu nghiên cứu chủ đề: {topic}\n")

      # Dùng stream để xem từng bước
    for step in agent.stream({"messages": [("user", topic)]}):
        print("=== STEP ===")
        print(step)
    
    # Ra lệnh cho Agent chạy
    response = agent.invoke({
        "messages": [("user", topic)]
    })
    
    # Trích xuất kết quả cuối cùng
    final_report = response["messages"][-1].content
    
    # Lưu kết quả ra file Markdown
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_report)
        
    print(f"Đã hoàn thành! Báo cáo được lưu tại file: {filename}")

if __name__ == "__main__":
    main()