import requests
import time

URL = 'http://example.com/crac_qinghai'

# Function to check CRAC website for changes

def check_for_changes():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()  # Assuming a JSON response
        # Logic to monitor changes in data
        print('Monitoring changes for Qinghai registration...')
    else:
        print('Failed to retrieve data')

while True:
    check_for_changes()
    time.sleep(60)  # Check every minute