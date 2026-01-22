import streamlit as st
import random
from fpdf import FPDF

# --- 1. ตรรกะการคำนวณที่รองรับเฉลย ---
def get_math_logic(op_type):
    if op_type == "Addition (+)":
        a, b = random.randint(10, 99), random.randint(10, 99)
        return a, b, a + b, "+"
    elif op_type == "Subtraction (-)":
        a = random.randint(20, 99)
        b = random.randint(10, a)
        return a, b, a - b, "-"
    elif op_type == "Multiplication (x)":
        a, b = random.randint(2, 12), random.randint(2, 9)
        return a, b, a * b, "x"
    else: # Division (/)
        b = random.randint(2, 9)
        ans = random.randint(2, 12)
        a = b * ans
        return a, b, ans, "/"

# --- 2. ฟังก์ชันสร้าง PDF แบบหลายหน้า ---
def create_worksheet_pdf(op_type, num_pages, probs_per_page, brand_name):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for page in range(num_pages):
        pdf.add_page()
        # ส่วนหัวกระดาษ
        pdf.set_font("Helvetica", 'B', 20)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"Name: ______________________ Class: _______ Page: {page+1}", ln=True, align='C')
        pdf.ln(15)

        # การจัดวาง Grid (3 คอลัมน์)
        col_width = 60
        row_height = 45
        for i in range(probs_per_page):
            n1, n2, res, symbol = get_math_logic(op_type)
            
            # คำนวณตำแหน่ง X, Y
            col = i % 3
            row = i // 3
            x = 25 + (col * col_width)
            y = 45 + (row * row_height)

            # วาดตัวเลขและเครื่องหมาย (จัดให้เครื่องหมายอยู่กลาง)
            pdf.set_font("Helvetica", '', 18)
            pdf.text(x + 10, y, f"{n1:2}")      # ตัวตั้ง
            pdf.text(x - 2, y + 5, symbol)     # เครื่องหมายอยู่ระหว่างบรรทัด
            pdf.text(x + 10, y + 8, f"{n2:2}")  # ตัวลบ/บวก
            pdf.line(x + 8, y + 11, x + 25, y + 11) # เส้นใต้โจทย์
            pdf.line(x + 8, y + 20, x + 25, y + 20) # เส้นคำตอบ
            pdf.line(x + 8, y + 21, x + 25, y + 21)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. ส่วนแสดงผลบน Streamlit ---
st.title("🔢 Multi-Page Worksheet Generator")

with st.sidebar:
    st.header("Settings")
    op = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (/)"])
    pages = st.slider("Number of Pages", 1, 10, 1) # กำหนดจำนวนหน้า
    probs = st.selectbox("Problems per Page", [12, 15, 18, 21])
    brand = st.text_input("Brand Name", "CapyCap Math")

if st.button("Generate Worksheet PDF"):
    pdf_file = create_worksheet_pdf(op, pages, probs, brand)
    st.success(f"Success! Generated {pages} pages.")
    st.download_button(
        label="📥 Download PDF",
        data=pdf_file,
        file_name="worksheet_multi.pdf",
        mime="application/pdf"
    )
