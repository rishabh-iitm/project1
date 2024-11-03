import requests
import csv
import time
from datetime import datetime

# GitHub API URL templates
USER_SEARCH_URL = "https://api.github.com/search/users"
USER_DETAIL_URL = "https://api.github.com/users/{username}"
USER_REPOS_URL = "https://api.github.com/users/{username}/repos"

# GitHub token for authentication to avoid rate limits
TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}"}

def fetch_users_in_barcelona(min_followers=500):
    """Fetch users in London with more than `min_followers` followers."""
    users = []
    page = 1
    while True:
        params = {
            "q": f"location:London followers:>{min_followers}",
            "per_page": 30,
            "page": page
        }
        response = requests.get(USER_SEARCH_URL, headers=HEADERS, params=params)
        data = response.json()
        
        if 'items' not in data:
            print("Error fetching users:", data)
            break
        
        users.extend(data['items'])
        
        # Stop if last page
        if len(data['items']) < 30:
            break
        page += 1
        time.sleep(1)  # to avoid rate limiting

    return users

def clean_company_name(company):
    """Clean the company name to follow requirements."""
    if company:
        company = company.strip()
        if company.startswith("@"):
            company = company[1:]
        return company.upper()
    return ""

def fetch_user_details(username):
    """Fetch detailed user information."""
    response = requests.get(USER_DETAIL_URL.format(username=username), headers=HEADERS)
    if response.status_code == 200:
        user_data = response.json()
        return {
            "login": user_data.get("login", ""),
            "name": user_data.get("name", ""),
            "company": clean_company_name(user_data.get("company", "")),
            "location": user_data.get("location", ""),
            "email": user_data.get("email", ""),
            "hireable": str(user_data.get("hireable", "")).lower(),
            "bio": user_data.get("bio", ""),
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "created_at": user_data.get("created_at", "")
        }
    return None

def fetch_user_repositories(username):
    """Fetch up to 500 repositories for a given user."""
    repos = []
    page = 1
    while len(repos) < 500:
        response = requests.get(USER_REPOS_URL.format(username=username), headers=HEADERS, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Failed to fetch repos for user {username}")
            break
        repo_data = response.json()
        if not repo_data:
            break
        for repo in repo_data:
            # Handle potential None value for license
            license_name = repo["license"]["key"] if repo.get("license") else ""
            repos.append({
                "login": username,
                "full_name": repo.get("full_name", ""),
                "created_at": repo.get("created_at", ""),
                "stargazers_count": repo.get("stargazers_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "language": repo.get("language", ""),
                "has_projects": str(repo.get("has_projects", "")).lower(),
                "has_wiki": str(repo.get("has_wiki", "")).lower(),
                "license_name": license_name
            })
        page += 1
        time.sleep(1)  # to avoid rate limiting

    return repos[:500]  # limit to 500 most recent repos


def save_to_csv(filename, data, fieldnames):
    """Save data to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    print("Starting data scraping...")
    users = fetch_users_in_barcelona()
    
    user_details = []
    user_repositories = []
    
    for user in users:
        username = user['login']
        details = fetch_user_details(username)
        
        if details:
            user_details.append(details)
            print(f"Fetched details for user: {username}")
            
            repos = fetch_user_repositories(username)
            user_repositories.extend(repos)
            print(f"Fetched {len(repos)} repos for user: {username}")

    # Save user data to users.csv
    user_fieldnames = ["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"]
    save_to_csv("users.csv", user_details, user_fieldnames)

    # Save repositories data to repositories.csv
    repo_fieldnames = ["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"]
    save_to_csv("repositories.csv", user_repositories, repo_fieldnames)
    
    print("Data scraping completed and saved to CSV files.")

if __name__ == "__main__":
    main()