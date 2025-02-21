import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 
import re
import os

#Email validation function
def email_validation(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
        
    #Phone number validation function
def phone_validation(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None
    
#Function to generate PDF
def generate_pdf(name, email, phone, summary, education, experience, skills, linkedin=None, github=None, certifications=None, languages=None):
    pdf_file = f"{name}_resume.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Name at the top with larger font
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, height - 72, name)
    
    # Contact info in separate lines
    c.setFont("Helvetica", 10)
    y_contact = height - 95
    
    # Email and phone on first line
    contact_line = f"Email: {email} | Phone: {phone}"
    c.drawString(72, y_contact, contact_line)
    
    # Social profiles on second line
    if linkedin or github:
        y_contact -= 15
        social_parts = []
        if linkedin:
            social_parts.append(f"LinkedIn: {linkedin}")
        if github:
            social_parts.append(f"GitHub: {github}")
        social_line = " | ".join(social_parts)
        c.drawString(72, y_contact, social_line)
        y_position = y_contact - 35
    else:
        y_position = y_contact - 35

    y_position = height - 130

    # Summary section
    if summary and summary != "A brief description about yourself...":
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, "PROFESSIONAL SUMMARY")
        c.setFont("Helvetica", 11)
        # Draw horizontal line
        c.line(72, y_position - 5, width - 72, y_position - 5)
        
        # Wrap and draw summary text
        text = c.beginText(72, y_position - 25)
        text.setFont("Helvetica", 11)
        wrapped_lines = [line.strip() for line in summary.split('\n')]
        for line in wrapped_lines:
            text.textLine(line)
        c.drawText(text)
        y_position -= (25 + len(wrapped_lines) * 15)

    # Education section
    if education:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, "EDUCATION")
        c.line(72, y_position - 5, width - 72, y_position - 5)
        c.setFont("Helvetica", 11)
        
        text = c.beginText(72, y_position - 25)
        wrapped_lines = [line.strip() for line in education.split('\n')]
        for line in wrapped_lines:
            text.textLine(line)
        c.drawText(text)
        y_position -= (25 + len(wrapped_lines) * 15)

    # Experience section
    if experience:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, "PROFESSIONAL EXPERIENCE")
        c.line(72, y_position - 5, width - 72, y_position - 5)
        c.setFont("Helvetica", 11)
        
        text = c.beginText(72, y_position - 25)
        wrapped_lines = [line.strip() for line in experience.split('\n')]
        for line in wrapped_lines:
            text.textLine(line)
        c.drawText(text)
        y_position -= (25 + len(wrapped_lines) * 15)

    # Skills section
    if skills:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, "SKILLS")
        c.line(72, y_position - 5, width - 72, y_position - 5)
        c.setFont("Helvetica", 11)
        
        text = c.beginText(72, y_position - 25)
        skill_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
        for skill in skill_list:
            text.textLine(f"• {skill}")
        c.drawText(text)
        y_position -= (25 + len(skill_list) * 15)

    # Certifications section
    if certifications:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, "CERTIFICATIONS")
        c.line(72, y_position - 5, width - 72, y_position - 5)
        c.setFont("Helvetica", 11)
        
        text = c.beginText(72, y_position - 25)
        cert_list = [cert.strip() for cert in certifications.split('\n') if cert.strip()]
        for cert in cert_list:
            text.textLine(f"• {cert}")
        c.drawText(text)
        y_position -= (25 + len(cert_list) * 15)

    # Languages section
    if languages:
        y_position -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, "LANGUAGES")
        c.line(72, y_position - 5, width - 72, y_position - 5)
        c.setFont("Helvetica", 11)
        
        text = c.beginText(72, y_position - 25)
        lang_list = [lang.strip() for lang in languages.split('\n') if lang.strip()]
        for lang in lang_list:
            text.textLine(f"• {lang}")
        c.drawText(text)

    c.save()
    return pdf_file


#Streamlit UI
st.title("Resume Builder")

#Input fields
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
linkedin = st.text_input("LinkedIn (Optional)")
github = st.text_input("GitHub (Optional)")
summary = st.text_area("Professional Summary")
education = st.text_area("Education")
experience = st.text_area("Professional Experience")
skills = st.text_area("Skills")
certifications = st.text_area("Certifications (Optional)")
languages = st.text_area("Languages (Optional)")

#RealTime Preview
st.subheader("Resume Preview")
st.markdown("---")

#Header Section With Personal Info
st.markdown(f"## {name}")
if email or phone:
    contact_info = []
    if email:
        contact_info.append(f"📧 {email}")
    if phone:
        contact_info.append(f"📱 {phone}")
    st.markdown(" | ".join(contact_info))

if linkedin or github:
    profiles = []
    if linkedin:
        profiles.append(f"[LinkedIn]({linkedin})")
    if github:
        profiles.append(f"[GitHub]({github})")
    st.markdown(" | ".join(profiles))

#Summary Section
if summary and summary != "A brief description about yourself...":
    st.markdown("### 📝 Professional Summary")
    st.write(summary)

# Education section
if education:
    st.markdown("### 🎓 Education")
    st.markdown(education)
    st.markdown("---")

# Experience section
if experience:
    st.markdown("### 💼 Professional Experience")
    st.markdown(experience)
    st.markdown("---")

# Skills section
if skills:
    st.markdown("### 🛠️ Skills")
    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
    for skill in skills_list:
        st.markdown(f"- {skill}")
    st.markdown("---")

# Certifications section
if certifications:
    st.markdown("### 📜 Certifications")
    cert_list = certifications.split("\n")
    for cert in cert_list:
        if cert.strip():  # Only show non-empty certifications
            st.markdown(f"- {cert.strip()}")
    st.markdown("---")

# Languages section
if languages:
    st.markdown("### 🌐 Languages")
    lang_list = languages.split("\n")
    for lang in lang_list:
        if lang.strip():  # Only show non-empty languages
            st.markdown(f"- {lang.strip()}")
    st.markdown("---")

#Button to generate PDF
if st.button("Generate PDF"):
    if name and email and phone:
        pdf_file = generate_pdf(name, email, phone, summary, education, experience, skills, linkedin, github, certifications, languages)

        with open(pdf_file, "rb") as f:
            st.download_button("Download Resume", f, file_name="resume.pdf", mime="application/pdf")
    else:
        st.error("Please fill in the required fields (Name, Email, Phone) to generate the resume.")