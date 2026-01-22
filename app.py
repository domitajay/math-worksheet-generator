import streamlit as st
import random
from fpdf import FPDF

# --- 1. ตรรกะคณิตศาสตร์แบบกำหนดหลัก (Dynamic Digits Logic) ---
def get_math_problem(op_type, digits):
    # กำหนดค่าต่ำสุดและสูงสุดตามจำนวนหลัก
    low = 10**(digits-1) if digits > 1 else 1
    high = (10**digits) - 1
    
    if op_type == "Addition (+)":
        a, b = random.randint(low, high), random.randint(low, high)
        return a, b, a + b, "+"
    elif op_type == "Subtraction (-)":
        a = random.randint(low, high)
        b = random.randint(low, a) # ป้องกันตัวลบมากกว่าตัวตั้ง
        return a, b, a - b, "-"
    elif op_type == "Multiplication (x)":
        # สำหรับคูณ ถ้าเลือกหลายหลัก ตัวคูณอาจจะปรับให้เล็กลงเพื่อความเหมาะสม
        a = random.randint(low, high)
        b = random.randint(2, 9) if digits > 2 else random.randint(2, high)
        return a, b, a * b, "x"
    else: # Division (÷) 
        # สร้างจากการคูณเพื่อให้ลงตัวเสมอ
        divisor = random.randint(2, 9) if digits > 2 else random.randint(2, 12)
        ans = random.randint(low, high)
        dividend = divisor * ans
        return dividend, divisor, ans, "÷"

# --- 2. ฟังก์ชันสร้าง PDF (Worksheet + Answer Key) ---
def create_full_worksheet(op_type, num_pages, probs_per_page, brand_name, digits):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    all_answers = []

    for p_num in range(num_pages):
        pdf.add_page()
        page_answers = []
        
        # หัวกระดาษ (Branding)
        pdf.set_font("Helvetica", 'B', 20)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"Practice: {op_type} ({digits} Digits) | Page: {p_num + 1}", ln=True, align='C')
        pdf.ln(15)

        # การจัดวาง Grid (ปรับระยะ X ตามจำนวนหลักที่เพิ่มขึ้น)
        col_width = 65 # เพิ่มความกว้างคอลัมน์เล็กน้อยสำหรับเลข 5 หลัก
        row_height = 55
        
        for i in range(probs_per_page):
            n1, n2, res, symbol = get_math_problem(op_type, digits)
            page_answers.append(res)
            
            col = i % 3
            row = i // 3
            x = 35 + (col * col_width)
            y = 60 + (row * row_height)

            # วาดเลขข้อ
            pdf.set_font("Helvetica", 'B', 14)
            pdf.text(x - 12, y - 8, f"{i+1}.") 

            # วาดโจทย์ (จัดชิดขวาเพื่อให้หลักเลขตรงกันเสมอ)
            pdf.set_font("Helvetica", '', 18)
            # ใช้ฟังก์ชัน drawRightString เพื่อให้หลักหน่วยตรงกันเป๊ะเหมือนมืออาชีพ
            pdf.text(x + 18, y, f"{n1:>{digits}}")      # ตัวตั้ง
            pdf.text(x - 2, y + 5, symbol)             # เครื่องหมาย
            pdf.text(x + 18, y + 8, f"{n2:>{digits}}")  # ตัวบวก/ลบ
            pdf.line(x + 8, y + 11, x + 30, y + 11)    # เส้นใต้โจทย์
        
        all_answers.append(page_answers)

    # --- ส่วนการสร้างหน้าเฉลย (Answer Key) ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, "ANSWER KEY", ln=True, align='C')
    pdf.line(20, 30, 190, 30)
    pdf.ln(10)

    for p_idx, p_ans in enumerate(all_answers):
        if pdf.get_y() > 250: pdf.add_page()
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, f"Page {p_idx + 1}", ln=True)
        pdf.set_font("Helvetica", '', 12)
        
        ans_text = ""
        for a_idx, ans in enumerate(p_ans):
            ans_text += f"{a_idx+1}) {ans:,}    " # ใส่คอมม่าให้ผลลัพธ์ที่เกินพัน
            if (a_idx + 1) % 4 == 0:
                pdf.cell(0, 8, ans_text, ln=True)
                ans_text = ""
        if ans_text: pdf.cell(0, 8, ans_text, ln=True)
        pdf.ln(2)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. หน้าตาเว็บไซต์ Streamlit ---
st.set_page_config(page_title="Math Generator Pro", layout="centered")
st.title("📚 Professional Math Worksheet Generator")

with st.sidebar:
    st.header("Customization")
    op = st.selectbox("1. Select Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (÷)"])
    # เพิ่มตัวเลือกจำนวนหลัก 1-5 หลัก
    num_digits = st.slider("2. Number of Digits", 1, 5, 2) 
    pages = st.slider("3. Number of Pages", 1, 100, 1) 
    probs = st.selectbox("4. Problems per Page", [12, 15, 18])
    brand = st.text_input("5. Brand Name", "My Learning Studio")

if st.button("Generate Mega Bundle"):
    with st.spinner(f'Creating {pages} pages ({num_digits} digits)...'):
        pdf_bytes = create_full_worksheet(op, pages, probs, brand, num_digits)
        st.success(f"Success! {pages} pages generated.")
        st.download_button(
            label="📥 Download PDF with Answer Key",
            data=pdf_bytes,
            file_name=f"math_{num_digits}digits_bundle.pdf",
            mime="application/pdf"
        )
