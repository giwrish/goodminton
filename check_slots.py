import requests
import os
from requests.exceptions import RequestException
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN') 
chat_id = os.getenv('TELEGRAM_CHAT_ID')

START_TIME = "1915"
MIN_OCCURRENCES = 3 

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7,mr;q=0.6',
    'cookie': '__stripe_mid=320ab3c7-242d-4e13-9315-0adbd7235a1403a9b4; AMP_e67a9a8afa=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIzNmFhMDdjNS1lYmMwLTRmYTItOTkyYi1hNTUzYjRiODBhMGElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE2NTAxNTcwNTQzJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNjUwMTY3MzkyNSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTQlN0Q=; fpg=94; amplitudeDeviceId=undefined; amplitudeSessionId=undefined; __stripe_sid=66fd8e99-c28a-44aa-81fe-8055df120892a4388f',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://www.eversports.de/sb/squash-house-berlin-03',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def get_last_thursday_within_next_14_days():
    today = datetime.today()
    end_date = today + timedelta(days=14)

    for i in range(15):
        potential_thursday = end_date - timedelta(days=i)
        if potential_thursday.weekday() == 3:
            return potential_thursday.strftime('%Y-%m-%d')

def send_alert(start_date):
    message = f"Badminton Court available on {start_date} at {START_TIME}!"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            print("Telegram alert sent successfully")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except RequestException as e:
       print(f"Error sending Telegram alert: {e}")

def check_availability(start_date):
    url = f'https://www.eversports.de/api/slot?facilityId=76443&startDate={start_date}&courts[]=77394&courts[]=77395&courts[]=77396'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json() 
        
        occurrences = [slot for slot in data['slots'] if slot['date'] == start_date and slot['start'] == START_TIME]
        
        count = len(occurrences)
        
        print(f"Courts Available : {3-count}")
        
        # if count < MIN_OCCURRENCES:
        send_alert(start_date)
    
    except RequestException as e:
        print(f"Failed to check slots: {e}")

def main():
    start_date = get_last_thursday_within_next_14_days()
    print(f"Starting availability checker for date: {start_date}")
    check_availability(start_date)

if __name__ == "__main__":
    main()