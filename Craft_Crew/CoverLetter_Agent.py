
## 💌 CoverLetter Agent – Purpose

### 🎯 **Goal:**  
Automatically generate a **personalized, job-specific cover letter** using:
- The **tailored resume content**
- The **job description**
- Your **profile summary** and motivation

And just like before:
> ✅ The tone and content are customized,  
> ❌ But the format will follow a professional business letter template.

---

## ✅ Step-by-Step Implementation

### 📁 `agents/cover_letter_writer.py`

```python
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(tailored_resume, job_description, company_name="the company"):
    print("[CoverLetterAgent] Creating personalized cover letter...")

    prompt = f"""
You are a professional career assistant. Write a personalized, formal cover letter based on:
- The tailored resume content
- The job description
- A general interest in working at {company_name}

Make sure the letter:
- Starts with a greeting
- Clearly shows how the candidate fits the job
- Is 3–4 short paragraphs
- Ends with a polite thank you and call to action
- Follows a professional tone and structure

Tailored Resume:
{tailored_resume}

Job Description:
{job_description}

Only return the cover letter text (no extra notes).
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
```

---

### 🧪 Add Sample Use to `main.py`

```python
from agents.cover_letter_writer import generate_cover_letter

cover_letter = generate_cover_letter(
    tailored_resume=tailored_resume,
    job_description=job_desc,
    company_name="Tech Solutions Pvt Ltd"
)

print("\n[📄 Generated Cover Letter]")
print(cover_letter)
```

---

### 🧠 Sample Output:

```
Dear Hiring Manager,

I am writing to express my interest in the Data Analyst role at Tech Solutions Pvt Ltd. With hands-on experience in SQL, R, Power BI, and data automation tools, I am confident in my ability to contribute effectively to your data initiatives...

My recent work on automating data pipelines and building interactive dashboards aligns closely with the responsibilities outlined in your job post. I am particularly excited about the opportunity to leverage tools like CrewAI and OpenAI in real-world applications...

Thank you for considering my application. I would welcome the chance to discuss how I can support your team and bring value to your projects.

Sincerely,  
Jatin Kumar
```

---

## ✅ Day 6 Progress

| Task | Status |
|------|--------|
| Use tailored resume + job post | ✅ Done |
| Maintain business tone & format | ✅ Done |
| Fully automated generation | ✅ Done |
| CLI testing with sample job | ✅ Included |

---

Shall we head to **Day 7: AutoApply Agent** next?

We’ll stub login automation (real browser automation comes later) and simulate applying to jobs using the generated documents 🔁📤
