from selenium import webdriver
import os 
from select import select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC3
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os
from idna import valid_contextj
from datetime import datetime, timedelta
import logging
import shutil
import pymysql

conn = pymysql.connect(
    host='10.244.18.98',
    user='abhishek',
    password='abhi',
    db='ob',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
vehicles = []
allocated_docks = {}
op = webdriver.ChromeOptions()
op.add_argument("user-data-dir=/home/flipkart/.config/google-chrome/Profile 166")
# op.add_argument('--headless=new')
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': r"/home/flipkart/ob_tv",
    'directory_upgrade': True
}
op.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=op)

def get_shift():
    current_hour = datetime.now().hour
    if 7 <= current_hour < 16: 
        return "morning"
    elif 16 <= current_hour < 22: 
        return "evening"
    else:  
        return "night"


def download_sheet(shift):
    time.sleep(1)
    link = f"https://script.google.com/a/macros/flipkart.com/s/AKfycbzEYbVAH3nPtTvbWRACidaudcXcnwAZ8SGtaxEwW9Lh0UNOEIehnIwDoEWaavuA3ENW/exec?action={shift}"
    driver.get(link)
    print(driver.title)
    logging.warning(f"Downloaded: {shift} OB Report")


def update_allocations():
    df = pd.read_csv(f"ob_{shift}.csv")
    unique_vehicles = df.drop_duplicates(subset='VEHICLE NO')

    allocated_docks.clear()  

    for index, row in unique_vehicles.iterrows():
        dock = row["DOCK"]
        vehicle = row["VEHICLE NO"]
        destination = row["Destination"]
        status = row["STATUS"]
        dock_in_time = row["DOCK  IN TIME"]

        if dock not in allocated_docks:
            allocated_docks[dock] = []

        allocated_docks[dock].append({
            "Vehicle": vehicle,
            "Destination": destination,
            "Status": status,
            "Dock In Time": dock_in_time
        })

        print(allocated_docks)


while True:
    shift = get_shift()
    print(shift)
    # download_sheet(shift)
    update_allocations()
    # time.sleep(600) 