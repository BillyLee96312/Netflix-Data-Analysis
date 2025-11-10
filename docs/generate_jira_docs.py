import requests
import os
import json

# ---------- Configuration ----------
# <JIRA_BASE_URL>
# What it is: Your Jira site URL.
# Where to find it:
# Open your Jira in a browser.
# The URL in the address bar is your <JIRA_BASE_URL>.
# Example:
#text
# https://yourcompany.atlassian.net
# Replace <JIRA_BASE_URL> with https://yourcompany.atlassian.net.
#
# 2. <JIRA_USERNAME>
# What it is: Your Jira login email.
# Where to find it:
# In Jira, go to your profile:
<<<<<<< HEAD
# Click your avatar in the top right ?†’ Profile.
=======
# Click your avatar in the top right ¡æ Profile.
>>>>>>> 19ca840 (Resolve merge conflicts before pushing)
# The email displayed here is your <JIRA_USERNAME>.
# Replace <JIRA_USERNAME> with your email, e.g.,
# text
# Copy
# yourname@example.com
# 3. <JIRA_API_TOKEN>
# What it is: A personal access token to authenticate API calls.
# How to generate:
# Log into your Jira account.
<<<<<<< HEAD
# Click your avatar ?†’ Account Settings.
# Navigate to Security ?†’ Create API token.
=======
# Click your avatar ¡æ Account Settings.
# Navigate to Security ¡æ Create API token.
>>>>>>> 19ca840 (Resolve merge conflicts before pushing)
# Enter a label (e.g., "Scripts Access").
# Click Create.
# Copy and save the generated token securely.
# Use:
# In your script, use this token as the password for API authentication.
# Example:
# text
# Copy
# JIRA_API_TOKEN = "Abcdef12345..."
# 4. <JIRA_PROJECT_KEY>
# What it is: Your Jira project key, a short code.
# Where to find it:
# Open your Jira project.
# Look at the project sidebar or header, usually at the top left.
# The project key is usually a short acronym or code.
# Example:
# If the project name is Netflix Data Analysis, the key might be ABC.
# You can also verify in the project URL, e.g.,
# text

# https://yourcompany.atlassian.net/browse/ABC
# Replace <JIRA_PROJECT_KEY> with your project key.
# 5. <GITHUB_REPO_PATH>
# What it is: Path to your local clone or directory for the GitHub repo.
#Where to find it:

# If you cloned the repo locally:
# bash cd path/to/your/local/repo
# In your file explorer, locate where the repo is saved.
#Alternatively, if you plan to run scripts on CI/CD pipelines, the repo path is predefined (e.g., working directory).
#Example: /home/user/Netflix-Data-Analysis
# Note:  For scripting, this path must point to where your files are stored locally or in the build environment.
  


JIRA_BASE_URL = 'https://billylee96312.atlassian.net'
JIRA_USERNAME = 'billylee96312@gmail.com'
JIRA_API_TOKEN = 'ATATT3xFfGF0WkmZqfzMIuUJyx7G5F09W7z9fKkaQq7UloZAAQZNJZA2Ocfqb3L3oC62YgOmmG4mZzQBcGEPei1zitYNy3BiNZpKSb63sPVzFFK5ColHyKhG0Kt7ktpdiwkbjwE7q_VodWGmz1O_liw5lyl8kYejjUznFDSp6TRASoibgLVkor0=92AAD907' # Until Nov 10, 2026
JIRA_PROJECT_KEY = 'PSFDAODPT-22'  # e.g., 'ABC'
GITHUB_REPO_PATH = 'D:\Project\Python & SQL on Databricks for Data Analytics - Pro Track\source codes\Netflix-Data-Analysis\Netflix-Data-Analysis\docs'  # local folder for docs

# Basic Auth for Jira API
auth = (JIRA_USERNAME, JIRA_API_TOKEN)

# Jira API endpoint for issues in a project (expand as needed)
JIRA_API_URL = f"{JIRA_BASE_URL}/rest/api/3/search"

# JQL query to fetch all issues in project (including epics, stories, subtasks) 
JQL = f"project={JIRA_PROJECT_KEY}"

# Fetch issues from Jira
def fetch_issues():
    issues = []
    start = 0
    max_results = 50
    while True:
        params = {
            'jql': JQL,
            'startAt': start,
            'maxResults': max_results,
            'fields': 'summary,description,issuetype,epic,subtasks,customfield_10011'  # add custom fields as needed
        }
        response = requests.get(JIRA_API_URL, params=params, auth=auth)
        data = response.json()
        issues.extend(data['issues'])
        if data['total'] <= start + max_results:
            break
        start += max_results
    return issues

# Generate Markdown file for an issue
def create_markdown(issue):
    issue_key = issue['key']
    fields = issue['fields']
    summary = fields['summary']
    description = fields.get('description', {}).get('content', [])
    issue_type = fields['issuetype']['name']
    epic_link = fields.get('epic', {}).get('name', '') if fields.get('epic') else ''
    subtasks = fields.get('subtasks', [])
    custom_fields = fields.get('customfield_10011', '')  # replace or add as needed

    # Basic Markdown content
    md_content = f"# Issue {issue_key}: {summary}\n\n"
    md_content += f"**Type:** {issue_type}\n\n"
    md_content += f"**Epic:** {epic_link}\n\n"
    md_content += f"## Description\n"
    # (add code to extract description text)
    if description:
        for content in description:
            for item in content.get('content', []):
                if item['type'] == 'text':
                    md_content += item['text'] + '\n'
    else:
        md_content += 'No description provided.\n'
    md_content += "\n## Subtasks & Related Issues\n"
    for sub in subtasks:
        sub_key = sub['key']
        md_content += f"- {sub_key}\n"
    md_content += "\n## Custom Fields\n"
    md_content += f"Additional info: {custom_fields}\n"

    # Write to file
    filename = os.path.join(GITHUB_REPO_PATH, f"{issue_key}.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)

# Main execution
def main():
    issues = fetch_issues()
    for issue in issues:
        create_markdown(issue)
        print(f"Generated {issue['key']}.md")

if __name__ == "__main__":
    main()
