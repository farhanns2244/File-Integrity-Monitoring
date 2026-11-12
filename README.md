# File Integrity Monitoring (FIM) System

## Project Overview

The File Integrity Monitoring (FIM) System is a Python-based cybersecurity project designed to monitor files and detect unauthorized changes.

The system uses the SHA-256 cryptographic hashing algorithm to identify file modifications by comparing current file hashes against previously stored baseline hashes.

When a change is detected, the system records the event, generates an alert, sends an email notification, and creates a Jira ticket for incident tracking.

## Objectives

- Monitor files for unauthorized modifications.
- Detect file creation, modification, and deletion.
- Maintain file integrity using SHA-256 hashing.
- Generate logs and JSON records of detected changes.
- Automate security notifications through email.
- Integrate with Jira for incident tracking.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| hashlib | SHA-256 hash calculation |
| JSON | Baseline and change storage |
| Requests | Jira API communication |
| SMTP | Email notifications |
| python-dotenv | Secure environment variable management |
| Jira REST API | Automated ticket creation |

## Key Features

### 1. SHA-256 Hashing
Calculates SHA-256 hashes for monitored files to identify changes in file contents.

### 2. Baseline Management
Creates and maintains a baseline containing the original file hashes in `baseline.json`.

### 3. File Integrity Detection
Identifies three types of file changes:

- ADDED – Detects newly created files.
- MODIFIED – Detects changes in existing files.
- DELETED – Detects removed files.

### 4. Change Logging
Records detected file changes, including timestamps and old and new hash values, in `log.txt`.

### 5. JSON Reporting
Stores detected changes in `changes.json` for structured recordkeeping.

### 6. Email Notifications
Sends email alerts through Gmail SMTP whenever a file integrity change is detected.

### 7. Jira Integration
Automatically creates Jira tickets when file changes are identified, helping track and manage security events.

### 8. Periodic Monitoring
Continuously checks the monitored directory at 10-second intervals.

## Project Structure

```text
File-Integrity-Monitoring/
│
├── monitor.py
├── baseline.json
├── changes.json
├── log.txt
├── test_folder/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

| File/Directory | Description |
|---|---|
| monitor.py | Main FIM monitoring script |
| baseline.json | Stores baseline file hashes |
| changes.json | Stores detected file changes |
| log.txt | Maintains change logs |
| test_folder | Directory being monitored |
| .env | Stores configuration and credentials |
| .gitignore | Prevents sensitive files from being uploaded |
| requirements.txt | Lists Python dependencies |

## How It Works

1. The system checks whether the monitoring directory exists.
2. It calculates SHA-256 hashes for files inside the directory.
3. It compares current hashes against the stored baseline.
4. It identifies newly added, modified, and deleted files.
5. It generates alerts when changes are detected.
6. It records events in the log and JSON files.
7. It sends email notifications.
8. It creates Jira tickets for detected changes.
9. It updates the baseline with the latest file hashes.
10. The monitoring process repeats every 10 seconds.

## Installation and Setup

### Prerequisites

- Python 3
- pip
- Git
- Jira account (for Jira integration)
- Gmail account with an app password (for email notifications)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/File-Integrity-Monitoring.git
```

### 2. Navigate to the Project Directory

```bash
cd File-Integrity-Monitoring
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project directory.

Add the following configuration:

```env
JIRA_URL=https://your-domain.atlassian.net/rest/api/3/issue
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
PROJECT_KEY=YOUR_PROJECT_KEY

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=recipient@example.com
```

Replace the example values with your own credentials and configuration.

**Security Note:** Never upload your `.env` file or expose API tokens and email passwords on GitHub.

### 6. Run the Project

```bash
python3 monitor.py
```

The system will start monitoring the `test_folder` directory.

## Testing

The system can be tested by performing the following operations inside `test_folder`:

| Test | Action | Expected Result |
|---|---|---|
| File Creation | Create a new file | ADDED alert |
| File Modification | Edit an existing file | MODIFIED alert |
| File Deletion | Delete an existing file | DELETED alert |

When a change is detected, the system records the event and attempts to send an email notification and create a Jira ticket.

## Security Considerations

- Uses SHA-256 hashing for file integrity verification.
- Keeps credentials in environment variables.
- Uses `.gitignore` to prevent accidental exposure of `.env`.
- Integrates automated alerts for detected changes.

**Note:** SHA-256 hashing detects content changes but does not independently prevent unauthorized modifications.

## Future Improvements

- Real-time monitoring using Python Watchdog.
- Monitoring multiple directories.
- Improved alert management.
- Detection of file permission changes.
- Integration with SIEM platforms such as Wazuh.
- Enhanced reporting and monitoring dashboard.
- More robust error handling and configuration validation.

## Learning Outcomes

Through this project, I gained practical experience in:

- Python scripting for cybersecurity.
- Cryptographic hashing using SHA-256.
- File integrity monitoring techniques.
- API integration and automation.
- Email-based security notifications.
- Security event logging and incident tracking.
- Environment variable management.

---

**Project:** File Integrity Monitoring System  
**Category:** Cybersecurity / Python Automation
