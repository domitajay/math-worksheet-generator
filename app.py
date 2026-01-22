import streamlit as st
import random
from fpdf import FPDF
import base64

# --- ตรรกะการสร้างโจทย์ (Logic) ---
def get_problem(op):
    if op == "Addition (+)":
        a, b = random.randint(10, 99), random.randint(10, 99)
        return a, b, a + b, "+"
    elif op == "Subtraction (-)":
        a = random.randint(20, 99)
        b = random.randint(10, a) # ป้องกันเลขติดลบ
        return a, b, a - b, "-"
    elif op == "Multiplication (x)":
        a, b = random.randint(2, 12), random.randint(2, 9)
        return a, b, a * b, "x"
    else: # Division (/) - หารลงตัวเสมอ
        b = random.randint(2, 9)
        ans = random.randint(2, 12)
        a = b * ans
        return a, b, ans, "/"

# --- ฟังก์ชันสร้าง PDF ---
def create_pdf(problems, brand_name):
    pdf = FPDF()
    pdf.add_page()
    # ใช้ Helvetica เป็นฟอนต์มาตรฐานเพื่อป้องกัน Error
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, txt=f"Math Worksheet: {brand_name}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=14)
    # จัดวางโจทย์เป็น 3 คอลัมน์ 4 แถว
    for i in range(0, len(problems), 3):
        chunk = problems[i:i+3]
        y_start = pdf.get_y()
        for idx, p in enumerate(chunk):
            x_pos = 20 + (idx * 60)
            pdf.text(x_pos, y_start, f"{i+idx+1})")
            pdf.text(x_pos + 10, y_start + 5, f"{p[0]}")
            pdf.text(x_pos + 6, y_start + 12, f"{p[3]} {p[1]}")
            pdf.line(x_pos + 5, y_start + 14, x_pos + 25, y_start + 14)
        pdf.ln(35)
    
    return pdf.output(dest='S').encode('latin-1')

# --- หน้าตาเว็บไซต์ (UI) ---
st.set_page_config(page_title="Math Worksheet Pro", layout="centered")
st.title("🎨 Math Worksheet Generator")

with st.sidebar:
    st.header("Settings")
    op_choice = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (x)", "Division (/)"])
    num_problems = st.slider("Problems per page", 6, 24, 12)
    brand = st.text_input("Brand Name", "My Studio")

if st.button("Generate Worksheet"):
    st.session_state.problems = [get_problem(op_choice) for _ in range(num_problems)]
    st.success("Worksheet Generated! Check preview below.")

if 'problems' in st.session_state:
    st.write("---")
    st.write("### Preview")
    cols = st.columns(3)
    for i, p in enumerate(st.session_state.problems):
        cols[i%3].write(f"**{i+1})** {p[0]} {p[3]} {p[1]} = ?")
    
    pdf_bytes = create_pdf(st.session_state.problems, brand)
    st.download_button(label="📥 Download PDF", data=pdf_bytes, file_name="math_worksheet.pdf", mime="application/pdf")
