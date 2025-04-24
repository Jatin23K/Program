# 🎯 Purpose:
#Extract all text content from your resume (PDF) so the system can analyze your:
#Skills
#Work experience
#Projects
# Education
# Certification

# 🔧 How it works:
#Uses PyPDF2.PdfReader to read each page of your resume.
# Extracts raw text content from all pages.
# Returns it as a single string. */

def parse_resume(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# 🧠 Why it's important:
# The AI needs this plain text to analyze what kind of candidate you are. It’s like scanning your resume for keywords automatically.
