# GitHub User and Repository Scraper for London-Based Users with High Follower Counts

### Project Summary

- **Data scraping methodology:** The project used the GitHub API to fetch data on users in London with more than 500 followers and saved details to CSV files.
- **Key finding:** Most popular users with high follower counts were affiliated with well-known companies and frequently contributed to open-source projects.
- **Recommendation for developers:** Engage with open-source communities and maintain a public profile, as high-visibility repositories attract significant engagement.

---

## Project Description

This project uses the GitHub API to identify and retrieve information on all GitHub users based in London with over 500 followers. User details and the first 500 repositories for each user are stored in CSV files (`users.csv` and `repositories.csv`) for analysis.

### File Descriptions

1. **`users.csv`** contains user details, including login, name, company, location, email, hireable status, bio, number of public repositories, followers, following count, and creation date.
2. **`repositories.csv`** lists repositories associated with each user, showing the repository’s name, creation date, star count, watcher count, language, and other relevant metadata.
3. **`README.md`** provides an overview of the project, methodology, findings, and recommendations.

### Analysis Process

The data was gathered using a Python script that leveraged the GitHub API. Here’s a brief outline of the workflow:
1. **User Search**: Search for users in London with more than 500 followers.
2. **User Detail Fetching**: Retrieve detailed information on each user, including bio, company, and follower count.
3. **Repository Fetching**: For each user, retrieve up to 500 of their most recently updated repositories.
4. **Data Cleaning**: Ensure consistent formatting for fields like company names.
5. **CSV Export**: Save the processed data to CSV files for easy access and further analysis.

### Findings

Analysis revealed that:
- Many high-follower users work in notable technology companies or popular startups in London.
- Frequently updated repositories tend to attract more stars, highlighting the importance of regular contributions.
- Popular languages among these developers were Python, JavaScript, and TypeScript, aligning with current web development and data science trends.

### Recommendations

For developers seeking to grow their GitHub presence:
- **Be active in open-source projects** to increase visibility and follower count.
- **Maintain high-quality, regularly updated repositories**; these are more likely to attract watchers and stars.
- **Engage with other developers** and leverage networking opportunities in local tech hubs like London.

### Technical Notes

- **Rate Limiting**: The GitHub API imposes rate limits. The script handles this with time delays to avoid exceeding these limits.
- **Data Clean-Up**: Company names were cleaned by trimming spaces, removing any initial `@` symbols, and standardizing to uppercase for uniformity.

### Future Work

Further analysis could include visualizations of user activity trends, language popularity among high-follower developers, and the role of open-source contributions in building a strong GitHub profile. 
