import streamlit as st
import random
from fpdf import FPDF

# --- 1. เตรียมรายชื่อรูปสัตว์น่ารัก (URLs) ---
# ผมเตรียมลิงก์รูปสัตว์ที่โหลดง่ายและไฟล์ไม่หนักมาให้ครับ
ANIMAL_ICONS = [
    "https://cdn-icons-png.flaticon.com/128/1998/1998592.png", # ลิง
    "https://cdn-icons-png.flaticon.com/128/616/616408.png",   # แมว
    "https://cdn-icons-png.flaticon.com/128/235/235359.png",   # สุนัข
    "https://cdn-icons-png.flaticon.com/128/1998/1998610.png", # แพนด้า
    "https://cdn-icons-png.flaticon.com/128/1998/1998765.png", # กระต่าย
    "https://cdn-icons-png.flaticon.com/128/235/235368.png",   # สิงโต
    "https://cdn-icons-png.flaticon.com/128/1998/1998625.png"  # หมู
]

# --- 2. ตรรกะคณิตศาสตร์ ---
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
    else:
        divisor = random.randint(2, 9)
        ans = random.randint(low, high)
        dividend = divisor * ans
        return dividend, divisor, ans, "÷"

# --- 3. ฟังก์ชันสร้าง PDF พร้อมรูปสัตว์ ---
def create_animal_worksheet(op_type, num_pages, probs_per_page, brand_name, digits):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    all_answers = []

    for p_num in range(num_pages):
        pdf.add_page()
        page_answers = []
        
        # ส่วนหัวใบงาน
        pdf.set_font("Helvetica", 'B', 20)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 11)
        pdf.cell(0, 10, f"Name: __________________________  Class: ________  Date: ________", ln=True, align='C')
        pdf.ln(5)

        col_width = 60
        row_height = 55
        
        for i in range(probs_per_page):
            n1, n2, res, symbol = get_math_problem(op_type, digits)
            page_answers.append(res)
            
            col = i % 3
            row = i // 3
            x, y = 20 + (col * col_width), 55 + (row * row_height)

            # --- วาดกรอบสี่เหลี่ยมมุมมน ---
            pdf.set_draw_color(0, 102, 204)
            pdf.round_rect(x, y, 50, 45, 5) 

            # --- ใส่รูปสัตว์ (สุ่มรูปและวางที่มุมขวาบนของกรอบ) ---
            animal_url = random.choice(ANIMAL_ICONS)
            try:
                # วางรูปขนาด 12x12 mm ที่มุมขวาบน
                pdf.image(animal_url, x + 35, y + 2, 12, 12)
            except:
                pass # ถ้าโหลดรูปไม่ได้ ให้รันต่อโดยข้ามรูปไป

            # --- วาดเลขข้อ ---
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_text_color(100, 100, 100)
            pdf.text(x + 3, y + 6, f"{i+1}.") 

            # --- วาดโจทย์คณิตศาสตร์ ---
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", '', 18)
            pdf.text(x + 25, y + 18, f"{n1:>{digits}}")
            pdf.text(x + 8, y + 25, symbol)
            pdf.text(x + 25, y + 30, f"{n2:>{digits}}")
            pdf.line(x + 12, y + 34, x + 42, y + 34)
        
        all_answers.append(page_answers)

    # --- หน้าเฉลย ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, "ANSWER KEY", ln=True, align='C')
    for p_idx, p_ans in enumerate(all_answers):
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, f"Page {p_idx + 1}", ln=True)
        pdf.set_font("Helvetica", '', 12)
        ans_text = "  ".join([f"{a_idx+1}) {ans:,}" for a_idx, ans in enumerate(p_ans)])
        pdf.multi_cell(0, 8, ans_text)

    return pdf.output(dest='S').encode('latin-1')

# --- 4. UI Streamlit ---
st.set_page_config(page_title="Animal Math Studio")
st.title("🦁 Animal Math Worksheet Studio")

with st.sidebar:
    st.header("Settings")
    op = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (÷)"])
    num_digits = st.slider("Digits", 1, 5, 2)
    pages = st.slider("Pages", 1, 50, 1)
    probs = st.selectbox("Problems per Page", [12, 15])
    brand = st.text_input("Brand Name", "CapyCap Studio") #

if st.button("Generate Animal Worksheets"):
    with st.spinner('Loading cute animals...'):
        pdf_bytes = create_animal_worksheet(op, pages, probs, brand, num_digits)
        st.download_button(label="📥 Download PDF", data=pdf_bytes, file_name="animal_math.pdf")
