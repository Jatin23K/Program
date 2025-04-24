# Install Required Packages
pip install crewai openai python-dotenv

# Required Libraries
import os
from crewai import Crew, Agent, Task
from dotenv import load_dotenv

# Load environment variables (OpenAI Key, etc.)
load_dotenv()

# Define All Agents
# Define Agents
info_collector = Agent(
    role='Information Collector',
    goal='Extract relevant profile info from resume, GitHub, and Notion',
    backstory='You are skilled at extracting structured data from unstructured documents and links.',
    verbose=True
)

overview_builder = Agent(
    role='Overview Builder',
    goal='Create a structured overview based on collected data',
    backstory='You summarize skills, experience, and project highlights.',
    verbose=True
)

job_searcher = Agent(
    role='Job Searcher',
    goal='Find relevant job listings based on profile overview',
    backstory='You specialize in identifying job opportunities online.',
    verbose=True
)

resume_tailor = Agent(
    role='Resume Tailor',
    goal='Customize resumes to align with job descriptions',
    backstory='You know how to highlight the most relevant points in a resume.',
    verbose=True
)

cover_letter_agent = Agent(
    role='Cover Letter Writer',
    goal='Write a cover letter that perfectly matches each job post',
    backstory='You write compelling cover letters tailored to specific companies.',
    verbose=True
)

auto_apply_agent = Agent(
    role='Auto Apply Agent',
    goal='Apply to job portals with the tailored resume and cover letter',
    backstory='You automate form submissions and login-based applications.',
    verbose=True
)

tracker_agent = Agent(
    role='Tracker Agent',
    goal='Track every application and update status logs',
    backstory='You maintain detailed logs of job applications for future reference.',
    verbose=True
)

# Define Tasks
tasks = [
    Task(description='Parse resume, GitHub, and Notion data', agent=info_collector),
    Task(description='Summarize profile into a structured overview', agent=overview_builder),
    Task(description='Search for 10 matching jobs based on profile', agent=job_searcher),
    Task(description='Tailor the resume to match each job found', agent=resume_tailor),
    Task(description='Generate personalized cover letters', agent=cover_letter_agent),
    Task(description='Submit applications via relevant platforms', agent=auto_apply_agent),
    Task(description='Log each application into Notion/CSV/GitHub', agent=tracker_agent)
]

# Create the Crew
jobcraft_crew = Crew(
    agents=[
        info_collector,
        overview_builder,
        job_searcher,
        resume_tailor,
        cover_letter_agent,
        auto_apply_agent,
        tracker_agent
    ],
    tasks=tasks,
    verbose=True
)

# Run the Crew
jobcraft_crew.run()






