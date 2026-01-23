import streamlit as st
import random
from fpdf import FPDF

# --- 1. ตรรกะคณิตศาสตร์ (Dynamic Digits) ---
def get_math_problem(op_type, digits):
    low = 10**(digits-1) if digits > 1 else 1
    high = (10**digits) - 1
    
    if op_type == "Addition (+)":
        a, b = random.randint(low, high), random.randint(low, high)
        return a, b, a + b, "+"
    elif op_type == "Subtraction (-)":
        a = random.randint(low, high)
        b = random.randint(low, a)
        return a, b, a - b, "-"
    elif op_type == "Multiplication (x)":
        a = random.randint(low, high)
        b = random.randint(2, 9) if digits > 2 else random.randint(2, high)
        return a, b, a * b, "x"
    else: # Division (÷)
        divisor = random.randint(2, 9)
        ans = random.randint(low, high)
        dividend = divisor * ans
        return dividend, divisor, ans, "÷"

# --- 2. ฟังก์ชันสร้าง PDF พร้อมกรอบ (Framed Layout) ---
def create_framed_worksheet(op_type, num_pages, probs_per_page, brand_name, digits):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    all_answers = []

    for p_num in range(num_pages):
        pdf.add_page()
        page_answers = []
        
        # ส่วนหัว: ชื่อแบรนด์ และ ข้อมูลนักเรียน (Name/Class/Date)
        pdf.set_font("Helvetica", 'B', 20)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 11)
        pdf.cell(0, 10, f"Name: __________________________  Class: ________  Date: ________", ln=True, align='C')
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, f"Practice: {op_type} ({digits} Digits) | Page: {p_num + 1}", ln=True, align='C')
        pdf.ln(5)

        # การจัดวาง Grid 
        # ปรับระยะห่างเพื่อให้ใส่กรอบได้สวยงาม
        col_width = 60
        row_height = 55
        
        for i in range(probs_per_page):
            n1, n2, res, symbol = get_math_problem(op_type, digits)
            page_answers.append(res)
            
            col = i % 3
            row = i // 3
            # จุดเริ่ม X, Y ของแต่ละข้อ
            x = 20 + (col * col_width)
            y = 55 + (row * row_height)

            # --- วาดกรอบสี่เหลี่ยมมุมมน (Rounded Box) ---
            pdf.set_draw_color(0, 102, 204) # สีน้ำเงินตามภาพตัวอย่าง
            pdf.set_line_width(0.6)
            # พารามิเตอร์: x, y, width, height, radius
            pdf.round_rect(x, y, 50, 45, 5) 

            # --- วาดเลขข้อ (มุมซ้ายบนของกรอบ) ---
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_text_color(100, 100, 100)
            pdf.text(x + 3, y + 6, f"{i+1}.") 

            # --- วาดโจทย์คณิตศาสตร์ (จัดหลักเลขให้ตรงกัน) ---
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", '', 18)
            # ใช้ช่องว่าง (padding) เพื่อให้ตัวเลขชิดขวา
            pdf.text(x + 25, y + 15, f"{n1:>{digits}}")     # ตัวตั้ง
            pdf.text(x + 8, y + 22, symbol)                 # เครื่องหมาย
            pdf.text(x + 25, y + 27, f"{n2:>{digits}}")     # ตัวบวก/ลบ
            pdf.line(x + 12, y + 31, x + 42, y + 31)        # เส้นใต้โจทย์
        
        all_answers.append(page_answers)

    # --- หน้าเฉลย (Answer Key) ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, "ANSWER KEY", ln=True, align='C')
    pdf.ln(10)
    for p_idx, p_ans in enumerate(all_answers):
        if pdf.get_y() > 250: pdf.add_page()
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, f"Page {p_idx + 1}", ln=True)
        pdf.set_font("Helvetica", '', 12)
        ans_text = "  ".join([f"{a_idx+1}) {ans:,}" for a_idx, ans in enumerate(p_ans)])
        pdf.multi_cell(0, 8, ans_text)
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. UI ส่วนหน้าเว็บ (Streamlit) ---
st.set_page_config(page_title="Math Generator Pro", layout="centered")
st.title("📚 Professional Math Worksheet Generator")

with st.sidebar:
    st.header("Settings")
    op = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (÷)"])
    num_digits = st.slider("Digits (1-5)", 1, 5, 2)
    pages = st.slider("Total Pages", 1, 100, 1)
    probs = st.selectbox("Problems per Page", [12, 15, 18])
    brand = st.text_input("Brand Name", "My Learning Studio")

if st.button("Generate Mega Bundle with Frames"):
    with st.spinner('Building your worksheets...'):
        pdf_bytes = create_framed_worksheet(op, pages, probs, brand, num_digits)
        st.success(f"Successfully generated {pages} pages!")
        st.download_button(
            label="📥 Download Framed PDF",
            data=pdf_bytes,
            file_name=f"math_bundle_framed.pdf",
            mime="application/pdf"
        )
