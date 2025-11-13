# TẠO FILE app.py (Thay thế file cũ)
import streamlit as st
import re
import json

# --- API Logic (Được sao chép từ Bước 2) ---
# Hàm này được giữ nguyên, chỉ thay đổi cách nó nhận đầu vào từ Streamlit
def generate_response(content_source, search_keyword):
    """
    Hàm API bao bọc logic SPG 'Quy trình Lọc dữ liệu'.
    """
    content = content_source
    keyword = search_keyword

    if not content or not keyword:
        # Trả về lỗi nếu thiếu đầu vào
        return {
            "error": "Vui lòng cung cấp cả Nội dung nguồn và Từ khóa tra cứu."
        }

    # 1. Thực hiện Lọc và Đếm (Tương ứng với Bước 3 logic)
    lines = content.split('\n')
    total_count = 0
    occurrences_list = []
    
    # Chuẩn bị regex để tìm từ khóa chính xác (Mức Độ Chính Xác: Tuyệt đối)
    pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)

    for i, line in enumerate(lines):
        matches = list(pattern.finditer(line))
        count_in_line = len(matches)
        total_count += count_in_line

        if count_in_line > 0:
            # Tạo Diễn Giải (Placeholder cho AI lõi)
            explanation = f"Từ '{keyword}' xuất hiện trong đoạn/dòng thứ {i+1} của nội dung."
            
            occurrences_list.append({
                "line_number": i + 1,
                "context_snippet": line.strip()[:100] + ('...' if len(line.strip()) > 100 else ''),
                "explanation_placeholder": explanation
            })

    # 2. Tạo Đầu ra Chính Xác Tuyệt Đối (theo OUTPUT_SCHEMA)
    result = {
        "summary_title": f"TỔNG KẾT LỌC DỮ LIỆU CHO TỪ KHÓA '{keyword.upper()}'",
        "total_count": total_count,
        "occurrences_list": occurrences_list,
        "deploy_note": "Cần tích hợp mô hình AI lõi để tạo 'Diễn Giải Rõ Ràng Ý Nghĩa' thay thế cho placeholder."
    }
    
    # Ghi nhớ các tham số chính (INPUT 2) vào meta-data
    result["metadata_spg"] = {
        "Tieu_chi_Loc": "Tất cả các chữ số và kí tự đặc biệt.",
        "Muc_Do_Chinh_Xac": "Tuyệt đối.",
        "Toc_Do_Phan_Hoi": "Nhanh chóng."
    }
    
    return result

# --- Bắt đầu Xây dựng UI Streamlit ---

st.set_page_config(page_title="SPG Data Filter", layout="wide")
st.title("Ứng Dụng Lọc Dữ Liệu Chính Xác (SPG-Powered)")
st.markdown("Chuyển đổi Quy trình Lọc Dữ Liệu SPG thành WebApp dùng được trên Streamlit.")

# --- INPUT SECTION ---
with st.container():
    st.subheader("📥 Bước 1 & 2: Nhận Diện Đầu Vào & Từ khóa")
    
    # Column for input
    col1, col2 = st.columns([3, 1])

    with col1:
        content_source = st.text_area(
            "1. Nguồn Đầu Vào: Dán Đoạn Văn Bản Lớn",
            placeholder="Dán nội dung lớn cần lọc ở đây...",
            height=250
        )
    
    with col2:
        search_keyword = st.text_input(
            "2. Từ Khóa Tra Cứu/Lọc",
            placeholder="Ví dụ: content"
        )
        # Nút nhấn chỉ kích hoạt khi có đầu vào
        if st.button("🚀 Tạo Kết Quả Lọc Chính Xác"):
            if not content_source or not search_keyword:
                st.error("Vui lòng nhập đầy đủ cả Nội dung và Từ khóa.")
            else:
                # Kích hoạt API Logic
                st.session_state['result'] = generate_response(content_source, search_keyword)

# --- OUTPUT SECTION ---
st.markdown("---")
st.subheader("✅ Bước 3: Kết Quả Chính Xác Tuyệt Đối")

if 'result' in st.session_state:
    result = st.session_state['result']

    if "error" in result:
        st.error(f"Lỗi: {result['error']}")
    else:
        # Hiển thị tóm tắt và chi tiết
        st.success(result["summary_title"])
        st.metric(label="Tổng Số Lần Xuất Hiện", value=result["total_count"])
        
        # Hiển thị chi tiết các lần xuất hiện
        st.markdown("**Chi Tiết Vị Trí Xuất Hiện và Diễn Giải:**")
        
        for item in result["occurrences_list"]:
            with st.expander(f"Dòng/Đoạn {item['line_number']} (Số lần: 1)"):
                st.code(item['context_snippet'], language='text')
                st.info(f"Diễn Giải (Placeholder): {item['explanation_placeholder']}")
        
        # Hiển thị metadata cho người dùng nâng cao
        with st.expander("Metadata SPG (Tham số cốt lõi)"):
            st.json(result["metadata_spg"])
else:
    st.info("Nhấn nút 'Tạo Kết Quả Lọc Chính Xác' để xem kết quả.")
