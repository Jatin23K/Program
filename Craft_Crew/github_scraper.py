
# 🎯 Purpose:
# Scrape project data from your public GitHub profile. It collects:
# Repository names
# Descriptions
# Number of stars
# Project URLs

# 🔧 How it works:
# Sends a GET request to GitHub’s public API: https://api.github.com/users/<username>/repos
# Loops through each repository and extracts relevant metadata.


def fetch_github_projects(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    repos = response.json()

    projects = []
    for repo in repos:
        projects.append({
            "name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"]
        })
    return projects

# 🧠 Why it's important:
# This shows the hiring manager (and JobCraft Crew) your technical portfolio, giving AI insight into your real-world coding work and contributions.




