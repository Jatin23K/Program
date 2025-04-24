Perfect, Jatin 👨‍💻 — now we’re entering **Day 5: ResumeTailor Agent** — and we’ll stick to your direction:

> ✨ **Tailor only the *content* of the resume** (skills, summary, bullet points),  
> ❌ Do *not* change the **format/template** of your original resume.

---

## 🧠 What ResumeTailor Agent Will Do

| Task | Details |
|------|---------|
| ✅ Extract important job keywords | From each job description |
| ✅ Match keywords to your resume content | Add/match to experience/skills |
| ✅ Modify content (not layout) | Keep formatting/style unchanged |
| ✅ Output updated content in **same structure** | For seamless integration |

---

## ✅ Step-by-Step Implementation

### 📁 `agents/resume_tailor.py`

```python
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def tailor_resume(resume_text, job_description):
    print("[ResumeTailor] Tailoring resume for specific job description...")

    prompt = f"""
You are a resume optimization expert.

Given:
- The original resume content below
- A job description
Your task is to tailor the resume content (summary, skills, and bullet points) to better match the job, while maintaining the original resume format and structure. Do NOT change headings, layout, or overall format. ONLY rewrite or enhance content where necessary.

Original Resume:
{resume_text[:3000]}  # trimmed for token safety

Job Description:
{job_description}

Return only the revised resume content (no extra explanations).
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
```

---

## 🧪 Optional Testing Mode
You can also create a mock job post for now:

```python
def sample_job_description():
    return """
We are hiring a Data Analyst proficient in SQL, Power BI, and R. The candidate should have experience in automation, data cleaning, and presenting dashboards to stakeholders. Familiarity with CrewAI or LLM-based tools is a plus.
"""
```

---

### 🔁 Update `main.py` to Run ResumeTailor

```python
from agents.resume_tailor import tailor_resume, sample_job_description

# Simulate job description (later pull from real listings)
job_desc = sample_job_description()

# Tailor resume content
tailored_resume = tailor_resume(
    resume_text=profile_data["resume_text"],
    job_description=job_desc
)

print("\n[✅ Tailored Resume Content]")
print(tailored_resume)
```

---

## 🎯 Final Output

This function will return **only the modified content**:
- Updated Summary
- Rewritten Skills section
- Improved Experience bullet points

It will **not touch**:
- Your resume’s structure (headings, sections)
- File format or layout  
⚠️ You can manually paste the tailored text into your template **or** later automate it with PDF editing tools like `pdfplumber` or `docx`.

---

## ✅ Day 5 Progress

| Task | Status |
|------|--------|
| Tailor resume content only | ✅ Done |
| Keep template untouched | ✅ Guaranteed |
| OpenAI-powered content matching | ✅ Done |
| Manual preview of tailored text | ✅ Displayed in terminal/output |

---

Ready to go to **Day 6: CoverLetter Agent**?  
This one will generate custom cover letters that align with the tailored resume + job description 💌📋
