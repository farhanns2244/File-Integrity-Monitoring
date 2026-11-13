
import os
from dotenv import load_dotenv

load_dotenv()
import hashlib
import json
import datetime
import time
import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

 
# CONFIGURATION SECTION
 

FOLDER_TO_MONITOR = "test_folder"
BASELINE_FILE = "baseline.json"
LOG_FILE = "log.txt"
CHANGES_FILE = "changes.json"


JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")



 
# HASH FUNCTION
 

def calculate_hash(filepath):
    """Calculate SHA256 hash of a file"""

    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None


 
# CREATE BASELINE
 

def create_baseline():

    baseline = {}

    for file in os.listdir(FOLDER_TO_MONITOR):

        path = os.path.join(FOLDER_TO_MONITOR, file)

        if os.path.isfile(path):

            file_hash = calculate_hash(path)

            if file_hash:
                baseline[file] = file_hash

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("Baseline created successfully.")


 
# LOAD BASELINE
 

def load_baseline():

    if not os.path.exists(BASELINE_FILE):

        print("Baseline not found. Creating baseline...")

        create_baseline()

    with open(BASELINE_FILE, "r") as f:
        return json.load(f)


 
# ALERT FUNCTION
 

def trigger_alert(message):

    print("\n ALERT:", message)


 
# LOG FUNCTION
 

def log_change(change_type, file_name, old_hash, new_hash):

    timestamp = datetime.datetime.now()

    log_entry = f"""
Time: {timestamp}
Change Type: {change_type}
File: {file_name}
Old Hash: {old_hash}
New Hash: {new_hash}
"""

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)


 
# STORE JSON RESULTS
 

def store_change_json(change):

    if not os.path.exists(CHANGES_FILE):
        changes = []

    else:
        with open(CHANGES_FILE, "r") as f:
            changes = json.load(f)

    changes.append(change)

    with open(CHANGES_FILE, "w") as f:
        json.dump(changes, f, indent=4)

#SEND EMAIL

def send_email_alert(file_name, change_type, old_hash, new_hash):

    subject = f"FIM Alert: {file_name} {change_type}"

    body = f"""
File Integrity Change Detected

File: {file_name}
Change Type: {change_type}

Old Hash: {old_hash}
New Hash: {new_hash}
"""

    msg = MIMEMultipart()

    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("Email alert sent successfully!")

    except Exception as e:
        print("Email sending failed:", e)
 


# SEND DATA TO JIRA
 

def create_jira_ticket(file_name, change_type, old_hash, new_hash):

    timestamp = str(datetime.datetime.now())

    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": f"FIM Alert: {file_name} {change_type}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text":
                                f"File Integrity Change Detected\n\n"
                                f"File: {file_name}\n"
                                f"Change Type: {change_type}\n"
                                f"Old Hash: {old_hash}\n"
                                f"New Hash: {new_hash}\n"
                                f"Timestamp: {timestamp}"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }

    try:

        response = requests.post(
            JIRA_URL,
            json=payload,
            headers=headers,
            auth=auth
        )

        if response.status_code == 201:

            print("Jira ticket created successfully.")

        else:

            print("Failed to create Jira ticket.")
            print("Response:", response.text)

    except Exception as e:

        print("Error connecting to Jira:", e)


 
# CHECK FILE INTEGRITY
 

def check_integrity():

    baseline = load_baseline()

    current_files = {}

    for file in os.listdir(FOLDER_TO_MONITOR):

        path = os.path.join(FOLDER_TO_MONITOR, file)

        if os.path.isfile(path):

            file_hash = calculate_hash(path)

            if file_hash:
                current_files[file] = file_hash

    # Detect added or modified files
    for file, current_hash in current_files.items():

        if file not in baseline:

            trigger_alert(f"New file added: {file}")

            log_change("ADDED", file, "N/A", current_hash)

            store_change_json({
                "file": file,
                "change": "ADDED",
                "timestamp": str(datetime.datetime.now())
            })

            create_jira_ticket(file, "ADDED", "N/A", current_hash)
            send_email_alert(file, "ADDED", "N/A", current_hash)


        elif baseline[file] != current_hash:

            trigger_alert(f"File modified: {file}")

            log_change("MODIFIED", file, baseline[file], current_hash)

            store_change_json({
                "file": file,
                "change": "MODIFIED",
                "timestamp": str(datetime.datetime.now())
            })

            create_jira_ticket(file, "MODIFIED", baseline[file], current_hash)
            send_email_alert(file, "MODIFIED", baseline[file], current_hash)


    # Detect deleted files
    for file in baseline:

        if file not in current_files:

            trigger_alert(f"File deleted: {file}")

            log_change("DELETED", file, baseline[file], "N/A")

            store_change_json({
                "file": file,
                "change": "DELETED",
                "timestamp": str(datetime.datetime.now())
            })

            create_jira_ticket(file, "DELETED", baseline[file], "N/A")
            send_email_alert(file, "DELETED", baseline[file], "N/A")


    # Update baseline after scan
    with open(BASELINE_FILE, "w") as f:
        json.dump(current_files, f, indent=4)


 
# MAIN LOOP (PERIODIC MONITORING)
 

def start_monitoring():

    print("Starting File Integrity Monitoring...")

    while True:

        check_integrity()

        print("Next scan in 10 seconds...\n")

        time.sleep(10)


 
# PROGRAM ENTRY POINT
 

if __name__ == "__main__":

    if not os.path.exists(FOLDER_TO_MONITOR):

        os.makedirs(FOLDER_TO_MONITOR)

    start_monitoring()
