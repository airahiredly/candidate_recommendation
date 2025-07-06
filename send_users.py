import os
import json
import requests
import sys

def send_user_data(user, job_details, webhook_url):
    headers = {'Content-Type': 'application/json'}
    # Combine user and job details into a single payload
    payload = {
        "user": user,
        "jobDetails": job_details
    }
    response = requests.post(webhook_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"✅ Successfully sent data for {user.get('NAME')}")
    else:
        print(f"❌ Failed to send data for {user.get('NAME')} - Status Code: {response.status_code}")
        print("Response:", response.text)

def main():
    users_json_str = os.getenv("USERS_JSON")
    job_details_str = os.getenv("JOB_DETAILS")
    webhook_url = os.getenv("WEBHOOK_URL")

    if not users_json_str:
        print("Error: USERS_JSON environment variable is not set.")
        sys.exit(1)

    if not job_details_str:
        print("Error: JOB_DETAILS environment variable is not set.")
        sys.exit(1)

    try:
        users = json.loads(users_json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding USERS_JSON: {e}")
        sys.exit(1)

    try:
        job_details = json.loads(job_details_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JOB_DETAILS: {e}")
        sys.exit(1)

    if not isinstance(users, list):
        print("Error: USERS_JSON must be a JSON array.")
        sys.exit(1)

    for user in users:
        send_user_data(user, job_details, webhook_url)

if __name__ == "__main__":
    main()
