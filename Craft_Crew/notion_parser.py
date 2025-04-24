# 🎯 Purpose:
# Pull a summary of your portfolio/projects from a Notion page (portfolio or case study hub).

# 🔧 How it works:
# For now, it returns a dummy string.

# In future updates, it will use the Notion API to:
# Access blocks
# Extract rich content like project details, images, and links


def parse_notion(notion_url):
    return f"Parsed content from Notion page: {notion_url}"

# 🧠 Why it's important:
# Your Notion page contains personal branding, featured work, and key highlights that enhance your professional story.

# 📦 Combined Output (Profile Dictionary)
# After running all 3 parsers, we get a unified profile_data like:


{
    "resume_text": "Jatin Kumar is a Data Analyst skilled in SQL, R, Power BI...",
    "github_projects": [
        {"name": "MetaMinds", "description": "AI-powered data analysis tool", "stars": 12, "url": "..."},
        ...
    ],
    "notion_summary": "Parsed content from Notion page: https://notion.so/jatin/portfolio"
}
# This profile_data will now be passed to the OverviewBuilder Agent next.
