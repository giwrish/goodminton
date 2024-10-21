import requests
import os
import logging
from requests.exceptions import RequestException
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, filename='availability_checker.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

bot_token = os.getenv('TELEGRAM_BOT_TOKEN') 
chat_id = os.getenv('TELEGRAM_CHAT_ID')

START_TIME = "1915"
MIN_OCCURRENCES = 3 

def get_last_thursday_within_next_14_days():
    today = datetime.today()
    end_date = today + timedelta(days=14)

    for i in range(15):
        potential_thursday = end_date - timedelta(days=i)
        if potential_thursday.weekday() == 3:
            return potential_thursday.strftime('%Y-%m-%d')

def send_alert():
    message = f"Badminton Court available on {start_date} at {START_TIME}!"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("Telegram alert sent successfully")
        else:
            logging.error(f"Failed to send alert. Status code: {response.status_code}")
    except RequestException as e:
        logging.error(f"Error sending Telegram alert: {e}")

def check_availability(start_date):
    url = f'https://www.eversports.de/api/slot?facilityId=76443&startDate={start_date}&courts[]=77394&courts[]=77395&courts[]=77396'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json() 
        
        occurrences = [slot for slot in data['slots'] if slot['date'] == start_date and slot['start'] == START_TIME]
        
        count = len(occurrences)
        
        logging.info(f"Occurrences found: {count}")
        
        if count < MIN_OCCURRENCES:
            logging.warning("Less than 3 occurrences found, court is available")
            send_alert()
        else:
            logging.info(f"all courts are booked")
    
    except RequestException as e:
        logging.error(f"Failed to fetch data: {e}")

def main():
    start_date = get_last_thursday_within_next_14_days()
    logging.info(f"Starting availability checker for date: {start_date}")
    check_availability(start_date)

if __name__ == "__main__":
    main()
