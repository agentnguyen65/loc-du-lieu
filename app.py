# TẠO FILE app.py (Cập nhật với File Uploader)
import streamlit as st
import re
import json
import io

# --- API Logic CẬP NHẬT (Hỗ trợ xử lý file) ---
def process_content(uploaded_file, text_input):
    """Xử lý đầu vào: Ưu tiên file, nếu không có file thì dùng text_input."""
    content = ""
    if uploaded_file is not None:
        # Giả định file là văn bản (txt, csv)
        try:
            # Đọc file nhị phân và decode thành string
            string_data = uploaded_file.getvalue().decode("utf-8")
            content = string_data
        except UnicodeDecodeError:
            st.error("Lỗi: Không thể đọc file. Vui lòng đảm bảo đó là file văn bản (UTF-8).")
            return ""
    elif text_input:
        content = text_input
    
    return content

def generate_response(content_source, search_keyword):
    # API Logic core được giữ nguyên
    content = content_source
    keyword = search_keyword
    
    # ... (Phần còn lại của hàm generate_response từ Bước 2/3) ...
    # (Đoạn mã này không thay đổi)
    
    # Chuẩn bị regex để tìm từ khóa chính xác (Mức Độ Chính Xác: Tuyệt đối)
    lines = content.split('\n')
    total_count = 0
    occurrences_list = []
    pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)

    for i, line in enumerate(lines):
        matches = list(pattern.finditer(line))
        count_in_line = len(matches)
        total_count += count_in_line
        
        # ... (Phần tạo occurrences_list và result) ...
        if count_in_line > 0:
            explanation = f"Từ '{keyword}' xuất hiện trong đoạn/dòng thứ {i+1} của nội dung."
            occurrences_list.append({
                "line_number": i + 1,
                "context_snippet": line.strip()[:100] + ('...' if len(line.strip()) > 100 else ''),
                "explanation_placeholder": explanation
            })
            
    result = {
        "summary_title": f"TỔNG KẾT LỌC DỮ LIỆU CHO TỪ KHÓA '{keyword.upper()}'",
        "total_count": total_count,
        "occurrences_list": occurrences_list,
        "deploy_note": "Cần tích hợp mô hình AI lõi để tạo 'Diễn Giải Rõ Ràng Ý Nghĩa' thay thế cho placeholder."
    }
    result["metadata_spg"] = {
        "Tieu_chi_Loc": "Tất cả các chữ số và kí tự đặc biệt.",
        "Muc_Do_Chinh_Xac": "Tuyệt đối.",
        "Toc_Do_Phan_Hoi": "Nhanh chóng."
    }
    
    return result

# --- Bắt đầu Xây dựng UI Streamlit CẬP NHẬT ---
st.set_page_config(page_title="SPG Data Filter", layout="wide")
st.title("Ứng Dụng Lọc Dữ Liệu Chính Xác (SPG-Powered)")

# --- INPUT SECTION ---
with st.container():
    st.subheader("📥 Bước 1 & 2: Nguồn Đầu Vào & Từ khóa")
    
    col1, col2 = st.columns([3, 1])

    with col1:
        # THAY THẾ TEXT AREA BẰNG FILE UPLOADER & TEXT AREA
        uploaded_file = st.file_uploader(
            "1a. Tải file văn bản (TXT, CSV)",
            type=['txt', 'csv'],
            help="Ưu tiên dùng file này nếu được tải lên."
        )
        
        text_input = st.text_area(
            "1b. Hoặc: Dán Đoạn Văn Bản Lớn",
            placeholder="Dán nội dung lớn cần lọc ở đây...",
            height=150
        )
    
    with col2:
        search_keyword = st.text_input(
            "2. Từ Khóa Tra Cứu/Lọc",
            placeholder="Ví dụ: content"
        )
        
        # Kích hoạt API Logic khi nhấn nút
        if st.button("🚀 Tạo Kết Quả Lọc Chính Xác"):
            processed_content = process_content(uploaded_file, text_input)
            
            if not processed_content or not search_keyword:
                st.error("Vui lòng cung cấp Nguồn nội dung (File hoặc Text) và Từ khóa.")
            else:
                # Lưu trữ kết quả vào session state
                st.session_state['result'] = generate_response(processed_content, search_keyword)

# --- OUTPUT SECTION (Không thay đổi) ---
st.markdown("---")
st.subheader("✅ Bước 3: Kết Quả Chính Xác Tuyệt Đối")

if 'result' in st.session_state:
    result = st.session_state['result']

    if "error" in result:
        st.error(f"Lỗi: {result['error']}")
    else:
        st.success(result["summary_title"])
        st.metric(label="Tổng Số Lần Xuất Hiện", value=result["total_count"])
        
        st.markdown("**Chi Tiết Vị Trí Xuất Hiện và Diễn Giải:**")
        
        for item in result["occurrences_list"]:
            with st.expander(f"Dòng/Đoạn {item['line_number']} (Số lần: 1)"):
                st.code(item['context_snippet'], language='text')
                st.info(f"Diễn Giải (Placeholder): {item['explanation_placeholder']}")
        
        with st.expander("Metadata SPG (Tham số cốt lõi)"):
            st.json(result["metadata_spg"])
else:
    st.info("Nhấn nút 'Tạo Kết Quả Lọc Chính Xác' để xem kết quả.")
