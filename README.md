# Automated Threat Intelligence Pipeline: Python SOAR Utility

A custom Python-based Security Operations Center (SOC) automation tool designed to ingest, analyze, and report on suspicious IP addresses using the AbuseIPDB API.

### Objective

The objective of this project was to transform a manual security task—checking individual IP addresses for malicious activity—into a scalable, automated pipeline. This involved securely managing API credentials, querying a commercial threat intelligence database, parsing complex JSON responses, and generating actionable CSV reports for incident response teams.

### Tools & Technologies

* Language: Python 3
* Libraries: requests, json, csv, os, argparse, python-dotenv
* Threat Intel Source: AbuseIPDB API v2
* Environment: Visual Studio Code (VS Code), Windows CLI

### The Process

**Phase 1: Environment & Dependency Setup**
A dedicated development environment was established using Visual Studio Code. Python 3 was installed, and the built-in package manager (pip) was utilized to install the necessary external libraries, specifically requests for handling HTTP API calls and python-dotenv for local environment variable management.

**Phase 2: Secure Credential Management**
To adhere to secure coding best practices and prevent the accidental exposure of API keys, a .env file was created to act as a local credential vault. Concurrently, a .gitignore file was configured to ensure the .env file and other local caches would not be committed to public version control repositories.

*(Insert your first screenshot here showing the VS Code file explorer with the .env and .gitignore files)*

**Phase 3: API Integration & Data Parsing**
The core Python script was developed to authenticate with the AbuseIPDB API using the securely loaded API key. A custom function was written to pass an IP address to the API endpoint, receive the raw JSON response, and parse out only the most critical Indicators of Compromise (IOCs), such as the Abuse Confidence Score, ISP, and Total Reports.

**Phase 4: CLI Tool Development**
To ensure the tool was flexible for different SOC scenarios, Python's argparse library was implemented to build a Command Line Interface (CLI). This allowed the user to invoke the script with specific arguments, such as -i for scanning a single IP address or -f for ingesting a bulk text file of IPs.

**Phase 5: Automated Reporting**
For bulk analysis, the script was engineered to aggregate the parsed JSON data from multiple IP queries and automatically format the output into a structured CSV file. This enables analysts to easily hand off parsed threat intelligence to other teams or import it into a SIEM.

**Phase 6: Execution & Validation**
The fully functional utility was tested against a text file containing both benign and historically malicious IP addresses (e.g., known Tor Exit nodes). The script successfully iterated through the list, calculated the threat scores, and generated the final threat_report.csv artifact.

*(Insert your final screenshot here showing the terminal output and the Rainbow CSV color-coded spreadsheet)*

### Outcomes & Skills Applied

* Security Automation: Engineered a script to process hundreds of Indicators of Compromise (IOCs) in seconds, drastically reducing the time spent on initial triage.
* Secure Credential Management: Utilized environment variables (.env) and .gitignore files to securely separate secrets from source code.
* API Integration: Authenticated and interacted with a commercial REST API using Python's requests library to dynamically retrieve threat intelligence.
* Data Parsing & Formatting: Successfully parsed nested JSON responses and formatted the relevant data points into clean CSV reports for management review.

### Troubleshooting & Lessons Learned

**1. System Path Recognition for Package Managers**
* Issue: The VS Code terminal returned a "term 'pip' is not recognized" error when attempting to install the required Python libraries.
* Resolution: Identified that the Python executable path was missing from the Windows environment variables. Re-ran the Python installer, ensuring the "Add python.exe to PATH" directive was explicitly checked, which allowed the terminal to successfully locate and execute the pip package manager.

**2. Terminal Environment Refresh**
* Issue: After installing the Python extension in VS Code, the terminal required a refresh to properly color-code syntax and recognize the new environment settings.
* Resolution: Relaunched the integrated terminal session to apply the newly contributed shell integration scripts, establishing a stable and fully featured development environment.

**Key Lessons**
* Secrets Management: Hardcoding API keys into a script is a major security vulnerability; utilizing local .env files is a non-negotiable best practice for security engineering.
* System Variables: A strong understanding of how operating systems handle PATH variables is critical when deploying command-line tools and configuring development environments.