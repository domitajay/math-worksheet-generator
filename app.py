import streamlit as st
import random
from fpdf import FPDF

# --- 1. ตรรกะการคำนวณและสุ่มโจทย์ ---
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

# --- 2. ฟังก์ชันสร้าง PDF (โจทย์ + เฉลย) ---
def create_full_worksheet(op_type, num_pages, probs_per_page, brand_name):
    pdf = FPDF()
    all_answers = [] # เก็บเฉลยทั้งหมดแยกตามหน้า

    # --- ส่วนการสร้างหน้าโจทย์ ---
    for page_num in range(num_pages):
        pdf.add_page()
        page_answers = []
        
        # หัวกระดาษ
        pdf.set_font("Helvetica", 'B', 20)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"Practice: {op_type} | Page: {page_num + 1}", ln=True, align='C')
        pdf.ln(15)

        # จัดวางโจทย์แบบ Grid (3 คอลัมน์)
        for i in range(probs_per_page):
            n1, n2, res, symbol = get_math_logic(op_type)
            page_answers.append(res) # เก็บคำตอบไว้ทำเฉลย
            
            col = i % 3
            row = i // 3
            x = 35 + (col * 60)
            y = 50 + (row * 45)

            pdf.set_font("Helvetica", '', 18)
            pdf.text(x + 10, y, f"{n1:2}")      # ตัวตั้ง
            pdf.text(x - 2, y + 5, symbol)     # เครื่องหมายอยู่กึ่งกลาง
            pdf.text(x + 10, y + 8, f"{n2:2}")  # ตัวบวก/ลบ
            pdf.line(x + 8, y + 11, x + 25, y + 11) # เส้นใต้โจทย์
            pdf.text(x + 5, y - 2, f"{i+1})")  # เลขข้อ
        
        all_answers.append(page_answers)

    # --- ส่วนการสร้างหน้าเฉลย (Answer Key) ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, "ANSWER KEY", ln=True, align='C')
    pdf.line(20, 30, 190, 30)
    pdf.ln(10)

    pdf.set_font("Helvetica", '', 14)
    for p_idx, p_ans in enumerate(all_answers):
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, f"Page {p_idx + 1}", ln=True)
        pdf.set_font("Helvetica", '', 14)
        
        # แสดงเฉลยแบบบรรทัดละ 4 ข้อเพื่อให้ดูง่าย
        ans_text = ""
        for a_idx, ans in enumerate(p_ans):
            ans_text += f"({a_idx+1}) {ans}    "
            if (a_idx + 1) % 4 == 0:
                pdf.cell(0, 8, ans_text, ln=True)
                ans_text = ""
        if ans_text: pdf.cell(0, 8, ans_text, ln=True)
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. ส่วนหน้าตาเว็บไซต์ Streamlit ---
st.set_page_config(page_title="Math Worksheet Pro", layout="centered")
st.title("📚 Pro Math Worksheet Generator")
st.write("Generate high-quality worksheets with automated Answer Keys.")

with st.sidebar:
    st.header("Customization")
    op_choice = st.selectbox("1. Choose Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (/)"])
    page_count = st.slider("2. Number of Pages", 1, 10, 1)
    prob_count = st.selectbox("3. Problems per Page", [12, 15, 18, 21])
    brand = st.text_input("4. Header/Brand Name", "My Math Studio")

if st.button("Generate & Create Answer Key"):
    with st.spinner('Calculating and drawing PDF...'):
        pdf_data = create_full_worksheet(op_choice, page_count, prob_count, brand)
        st.success(f"Worksheet with {page_count} pages and Answer Key is ready!")
        st.download_button(
            label="📥 Download Full PDF (Worksheet + Answers)",
            data=pdf_data,
            file_name=f"math_bundle_{op_choice.split()[0].lower()}.pdf",
            mime="application/pdf"
        )
