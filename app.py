import streamlit as st
import openai
import docx
import os
import re
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --------------------------
#   API Key Configuration
# --------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# --------------------------
#   File Reading Function
# --------------------------
def read_docx(file):
    doc = docx.Document(file)
    full_text = [p.text for p in doc.paragraphs]
    return "\n".join(full_text)

# --------------------------
#  Anonymization for Privacy
# --------------------------
def anonymize_text(text):
    text = re.sub(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b', 'CandidateName', text)  # Names
    text = re.sub(r'\b[\w.-]+?@\w+?\.\w+?\b', 'candidate@email.com', text)      # Emails
    text = re.sub(r'(\+?\d[\d\s\-().]{8,}\d)', 'XXX-XXX-XXXX', text)            # Phones
    text = re.sub(r'https?://(www\.)?(linkedin|github)\.com/[^\s]+', 'https://profile.url', text)  # URLs
    return text

# --------------------------
#    Resume Matching Logic
# --------------------------
def get_match_score(resume_text, jd_text):
    resume_text_safe = anonymize_text(resume_text)
    jd_text_safe = anonymize_text(jd_text)

    prompt = f"""
    You are an expert technical recruiter. 
    Compare the following resume with the job description.

    Provide your output in this exact format:
    
    1. Match percentage: <number between 0 and 100>
    2. Strengths: <3-5 bullet points summarizing the candidate's strengths>
    3. Skill Gaps: <3-5 bullet points where the resume does not meet the JD>
    4. Suggestions: <3-5 bullet points on how the candidate can improve for this role>

    Resume:
    {resume_text_safe}

    Job Description:
    {jd_text_safe}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message["content"]

# --------------------------
#    PDF Report Generator
# --------------------------
def generate_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    for line in content.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
#      Streamlit UI
# --------------------------
st.title("📄 AI Resume Matcher")
st.caption("Upload your resume and job description to get an AI-powered compatibility report.")
st.markdown("---")

# --------------------------
#      Upload Widgets
# --------------------------
resume_file = st.file_uploader(" Upload Resume (.docx)", type=["docx"])
jd_text = st.text_area(" Paste the Job Description")

# --------------------------
#      Match & Report
# --------------------------
if st.button("Analyze") and resume_file and jd_text:
    resume_text = read_docx(resume_file)
    with st.spinner("Analyzing with AI..."):
        result = get_match_score(resume_text, jd_text)

    st.subheader("Match Result")
    st.write(result)

    pdf_buffer = generate_pdf(result)
    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name="resume_match_report.pdf",
        mime="application/pdf"
    )

# --------------------------
#  Footer with Privacy Note
# --------------------------
st.markdown("---")
st.caption("🔒 Your data is processed securely in-memory and never stored.")
