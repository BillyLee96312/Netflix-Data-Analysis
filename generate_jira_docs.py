import requests
import os
import json


JIRA_BASE_URL = 'https://billylee96312.atlassian.net'
JIRA_USERNAME = 'billylee96312@gmail.com'
JIRA_API_TOKEN = 'ATATT3xFfGF0WkmZqfzMIuUJyx7G5F09W7z9fKkaQq7UloZAAQZNJZA2Ocfqb3L3oC62YgOmmG4mZzQBcGEPei1zitYNy3BiNZpKSb63sPVzFFK5ColHyKhG0Kt7ktpdiwkbjwE7q_VodWGmz1O_liw5lyl8kYejjUznFDSp6TRASoibgLVkor0=92AAD907' # Until Nov 10, 2026
JIRA_PROJECT_KEY = 'PSFDAODPT-22'  # e.g., 'ABC'
GITHUB_REPO_PATH = r'D:\Project\Python & SQL on Databricks for Data Analytics - Pro Track\source codes\Netflix-Data-Analysis\Netflix-Data-Analysis\docs'  # local folder for docs

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
            'fields': 'summary,description,issuetype,epic,subtasks',  # add custom fields as needed
            'maxResults': 50
        }
        response = requests.get(JIRA_API_URL, params=params, auth=auth)
        if response.status_code != 200:
            print(f"Error fetching issues: {response.status_code}")
            print("Response:", response.text)
            return []

        data = response.json()
        if 'issues' not in data:
            print("No 'issues' key in response. Check your Jira API query.")
            return []
        # Debugging output
        print("Fetched issues:")

        print(json.dumps(data, indent=4))
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
