📁 jobcraft_crew/
Main project folder — contains all your agents, utilities, workflows, and logs.

📄 .env
Purpose: Store sensitive environment variables securely.

Contains:

ini
Copy
Edit
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp-xxxxxxxxxxxxxxxxxxxxx
NOTION_API_KEY=secret_xxxxxxxx
NAUKRI_EMAIL=your.email@example.com
NAUKRI_PASSWORD=secure_password
🔒 This is never committed to GitHub (add to .gitignore)
🔐 Loaded via load_dotenv() to access keys inside your scripts

📄 main.py
Purpose: Main entry point of the Crew workflow.

Contains:

All agent declarations (Agent())

All task assignments (Task())

Crew initialization (Crew())

crew.run() execution line

👨‍💻 This is the script you run to activate the whole JobCraft Crew!

📁 agents/
Purpose: Holds separate agent logic files for modular code.

Files inside:

info_collector.py
Parses resume, GitHub, Notion — returns structured profile data

overview_builder.py
Uses structured data to generate a summary overview (skills, experience, goals)

job_searcher.py
Searches for jobs using scraped data, APIs, or OpenAI-based queries

resume_tailor.py
Modifies the resume based on job descriptions using LLM

cover_letter_writer.py
Generates custom cover letters per job description

auto_apply_agent.py
Simulates login and applies using tailored documents (or stubs if automation blocked)

tracker_agent.py
Maintains application history, updates CSV or Notion/GitHub

🧠 Each file defines a helper class or function for its specific task.

📁 utils/
Purpose: Contains all helper scripts and low-level functions.

Files inside:

resume_parser.py

Extracts text from PDF/docx

Extracts skills, experience, education using NLP

github_scraper.py

Uses GitHub API to fetch public repos, stars, readmes

Summarizes most popular projects

notion_parser.py

Uses Notion API to extract structured info from the portfolio page

job_portal_scraper.py

Searches jobs from Naukri/LinkedIn/Indeed

Returns list of roles, links, companies

🛠 These are used by the agents as tools to complete their tasks.

📁 logs/
Purpose: Stores output files and logs of your crew's work.

Files inside:

applications.csv

Contains all job applications with status tracking

Columns like: Job Title, Company, Link, Status, Date, Resume Used, Cover Letter Used

📘 You can later upload this to Notion or GitHub for visibility.
