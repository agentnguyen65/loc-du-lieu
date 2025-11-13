# TẠO FILE app.py VÀ DÁN TOÀN BỘ NỘI DUNG SAU:
import gradio as gr
import re
import json

# --- START: API Logic (Được sao chép từ Bước 2) ---
def generate_response(content_source, search_keyword):
    # ... (Toàn bộ mã hàm generate_response và UI đã sinh ở Bước 3)
    # Vui lòng dán toàn bộ mã code đã tạo trong Bước 3 vào đây
    # ...
    # Sử dụng json.loads/dumps để Gradio JSON component hiển thị đẹp hơn
    return json.loads(json.dumps(result, indent=2, ensure_ascii=False))

# --- END: API Logic ---

# --- Bắt đầu Xây dựng UI Gradio ---
with gr.Blocks(title="Ứng Dụng Lọc Dữ Liệu SPG") as app:
    gr.Markdown("<h1>Ứng Dụng Lọc Dữ Liệu Chính Xác (SPG-Powered)</h1>")
    gr.Markdown("Chuyển đổi Quy trình Lọc Dữ Liệu SPG thành WebApp dùng được.")
    
    with gr.Row():
        content_source = gr.Textbox(lines=10, label="1. Nguồn Đầu Vào: Dán Đoạn Văn Bản")
        search_keyword = gr.Textbox(label="2. Từ Khóa Tra Cứu/Lọc")
        
    btn = gr.Button("🚀 Tạo Kết Quả Lọc Chính Xác (Bước 3: Thực Thi)")
    
    output_json = gr.JSON(
        label="✅ Kết Quả Chính Xác Tuyệt Đối (OUTPUT_SCHEMA)",
        value={"Tình trạng": "Chờ đầu vào và xử lý..."}
    )

    btn.click(
        fn=generate_response, 
        inputs=[content_source, search_keyword], 
        outputs=output_json
    )

app.launch() # Đảm bảo lệnh launch có mặt nếu chạy trực tiếp trên Spaces