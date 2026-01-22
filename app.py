import streamlit as st
import random
from fpdf import FPDF

# --- 1. ตรรกะคณิตศาสตร์ระดับมือโปร (Professional Math Logic) ---
def get_math_problem(op_type):
    if op_type == "Addition (+)":
        a, b = random.randint(10, 99), random.randint(10, 99)
        return a, b, a + b, "+"
    elif op_type == "Subtraction (-)":
        a = random.randint(20, 99)
        b = random.randint(10, a) # ตัวตั้งมากกว่าตัวลบเสมอ
        return a, b, a - b, "-"
    elif op_type == "Multiplication (x)":
        a, b = random.randint(2, 12), random.randint(2, 9)
        return a, b, a * b, "x"
    else: # Division (÷) 
        divisor = random.randint(2, 9)
        ans = random.randint(2, 12)
        dividend = divisor * ans # สร้างโจทย์จากการคูณเพื่อให้หารลงตัว 100%
        return dividend, divisor, ans, "÷"

# --- 2. ฟังก์ชันสร้าง PDF (Worksheet + Answer Key) ---
def create_full_worksheet(op_type, num_pages, probs_per_page, brand_name):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    all_answers = [] # สำหรับเก็บข้อมูลเฉลย

    # --- ส่วนการสร้างหน้าโจทย์ ---
    for p_num in range(num_pages):
        pdf.add_page()
        page_answers = []
        
        # หัวกระดาษ (Branding)
        pdf.set_font("Helvetica", 'B', 20)
        pdf.cell(0, 10, brand_name, ln=True, align='C')
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"Practice: {op_type} | Page: {p_num + 1}", ln=True, align='C')
        pdf.ln(15)

        # การจัดวาง Grid (3 คอลัมน์)
        col_width = 60
        row_height = 45
        for i in range(probs_per_page):
            n1, n2, res, symbol = get_math_problem(op_type)
            page_answers.append(res)
            
            col = i % 3
            row = i // 3
            x = 35 + (col * col_width)
            y = 50 + (row * row_height)

            # วาดตัวเลขและเครื่องหมาย (จัดกึ่งกลาง)
            pdf.set_font("Helvetica", '', 18)
            pdf.text(x + 10, y, f"{n1:2}")      # ตัวตั้ง
            pdf.text(x - 2, y + 5, symbol)     # เครื่องหมายอยู่ระหว่างบรรทัด
            pdf.text(x + 10, y + 8, f"{n2:2}")  # ตัวลบ/บวก
            pdf.line(x + 8, y + 11, x + 25, y + 11) # เส้นใต้โจทย์
            pdf.text(x + 4, y - 2, f"{i+1}.")  # เลขข้อ
        
        all_answers.append(page_answers)

    # --- ส่วนการสร้างหน้าเฉลย (Answer Key) ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, "ANSWER KEY", ln=True, align='C')
    pdf.line(20, 30, 190, 30)
    pdf.ln(10)

    for p_idx, p_ans in enumerate(all_answers):
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, f"Page {p_idx + 1}", ln=True)
        pdf.set_font("Helvetica", '', 14)
        
        ans_text = ""
        for a_idx, ans in enumerate(p_ans):
            ans_text += f"{a_idx+1}) {ans}    "
            if (a_idx + 1) % 4 == 0:
                pdf.cell(0, 10, ans_text, ln=True)
                ans_text = ""
        if ans_text: pdf.cell(0, 10, ans_text, ln=True)
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1')

# --- 3. ส่วนหน้าตาเว็บไซต์ Streamlit ---
st.set_page_config(page_title="Pro Math Generator", layout="centered")
st.title("📚 Professional Math Worksheet Generator")
st.write("Create high-quality practice sheets for TPT, Etsy, or Classroom use.")

with st.sidebar:
    st.header("Customization Settings")
    op = st.selectbox("1. Select Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (÷)"])
    pages = st.slider("2. Number of Pages", 1, 10, 1)
    probs = st.selectbox("3. Problems per Page", [12, 15, 18, 21])
    brand = st.text_input("4. Brand/Header Name", "My Learning Studio")

if st.button("Generate Worksheet Bundle"):
    with st.spinner('Generating PDF with Answer Key...'):
        pdf_bytes = create_full_worksheet(op, pages, probs, brand)
        st.success(f"Worksheet bundle with {pages} pages is ready!")
        st.download_button(
            label="📥 Download PDF (Worksheet + Answer Key)",
            data=pdf_bytes,
            file_name=f"math_practice_bundle.pdf",
            mime="application/pdf"
        )
