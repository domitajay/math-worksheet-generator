import streamlit as st
import random
from fpdf import FPDF  # fpdf2 จะใช้ชื่อ import นี้เช่นกัน

# รายชื่อลิงก์รูปสัตว์น่ารัก (Icons)
ANIMAL_ICONS = [
    "https://cdn-icons-png.flaticon.com/128/1998/1998592.png",
    "https://cdn-icons-png.flaticon.com/128/616/616408.png",
    "https://cdn-icons-png.flaticon.com/128/235/235359.png",
    "https://cdn-icons-png.flaticon.com/128/1998/1998610.png",
    "https://cdn-icons-png.flaticon.com/128/1998/1998765.png"
]

def get_math_problem(op_type, digits):
    low, high = 10**(digits-1) if digits > 1 else 1, (10**digits) - 1
    a, b = random.randint(low, high), random.randint(low, high)
    if op_type == "Addition (+)": return a, b, a + b, "+"
    elif op_type == "Subtraction (-)":
        a, b = max(a, b), min(a, b)
        return a, b, a - b, "-"
    return a, b, a * b, "x"

def create_animal_worksheet(op_type, num_pages, probs_per_page, brand_name, digits):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for p_num in range(num_pages):
        pdf.add_page()
        # ส่วนหัวใบงาน
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 10)
        pdf.cell(0, 8, "Name: __________________________  Class: ________  Date: ________", ln=True, align='C')
        pdf.ln(5)

        col_width, row_height = 60, 50
        for i in range(probs_per_page):
            n1, n2, _, symbol = get_math_problem(op_type, digits)
            col, row = i % 3, i // 3
            x, y = 20 + (col * col_width), 45 + (row * row_height)

            # วาดกรอบสี่เหลี่ยมมุมมน (ต้องใช้ fpdf2 เท่านั้น)
            pdf.set_draw_color(0, 102, 204)
            pdf.set_line_width(0.5)
            pdf.round_rect(x, y, 50, 42, 5) 

            # สุ่มใส่รูปสัตว์มุมขวาบน
            try: pdf.image(random.choice(ANIMAL_ICONS), x + 35, y + 2, 10, 10)
            except: pass

            # เลขข้อ
            pdf.set_font("Helvetica", 'B', 10)
            pdf.set_text_color(120)
            pdf.text(x + 3, y + 6, f"{i+1}.") 

            # โจทย์คณิตศาสตร์ (จัดชิดขวาเพื่อให้หลักตรงกัน)
            pdf.set_text_color(0)
            pdf.set_font("Helvetica", '', 18)
            pdf.text(x + 25, y + 15, f"{n1:>{digits}}")
            pdf.text(x + 8, y + 22, symbol)
            pdf.text(x + 25, y + 28, f"{n2:>{digits}}")
            pdf.line(x + 12, y + 31, x + 42, y + 31)

    return pdf.output(dest='S').encode('latin-1')

st.title("🦁 Animal Math Studio")
with st.sidebar:
    op = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)"])
    digits = st.slider("Digits", 1, 3, 2)
    brand = st.text_input("Brand Name", "CapyCap Studio")

if st.button("Generate Animal Worksheets"):
    pdf_bytes = create_animal_worksheet(op, 1, 12, brand, digits)
    st.download_button("📥 Download PDF", pdf_bytes, "animal_math.pdf")
