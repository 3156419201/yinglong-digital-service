import os
import smtplib
import hashlib
import requests
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Function to send email notifications
def send_email(subj, body):
    try:
        user = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        from_addr = os.getenv("EMAIL_FROM")
        to_addr = os.getenv("EMAIL_TO")
        
        msg = MIMEText(body)
        msg['Subject'] = subj
        msg['From'] = from_addr
        msg['To'] = to_addr
        
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Update SMTP server and port
            server.starttls()
            server.login(user, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to fetch and monitor the CRAC website
def monitor_crac_qinghai():
    url = "http://www.crac.org.cn/"
    response = requests.get(url)
    
    # Check response status
    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return
    
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    # Check for Qinghai specific keywords
    if any(keyword in soup.text for keyword in ["报名", "青海", "开始报名"]):
        # Hash the page content to track changes
        current_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Read last hash from the file
        try:
            with open("last_hash_qinghai.txt", "r") as f:
                last_hash = f.read().strip()
        except FileNotFoundError:
            last_hash = ""
        
        # Compare current hash with last hash
        if current_hash != last_hash:
            print("Change detected! Sending email notification...")
            send_email("Qinghai Registration Update", "Changes detected on the CRAC website.")
            # Save the new hash for future comparisons
            with open("last_hash_qinghai.txt", "w") as f:
                f.write(current_hash)
        else:
            print("No changes detected.")
    else:
        print("No relevant information found on the page.")

if __name__ == "__main__":
    monitor_crac_qinghai()