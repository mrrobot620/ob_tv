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
    host='localhost',
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
    link = f"https://script.google.com/a/macros/flipkart.com/s/AKfycbxf4GprUXV0v2d2KTooldSohq6kNQ6cB18RfL5okOJtVnxBKMYN8ZtSZkFOlIIV8-mt/exec={shift}"
    driver.get(link)
    print(driver.title)
    logging.warning(f"Downloaded: {shift} OB Report")

def convert_to_mysql_datetime(date_str):
    timezone_info = date_str.split('(')[-1].split(')')[0]
    date_str_without_timezone = date_str.replace(f' ({timezone_info})', '')
    date_obj = datetime.strptime(date_str_without_timezone, '%a %b %d %Y %H:%M:%S %Z%z')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def update_database(allocations):
    with conn.cursor() as cursor:
        for dock, dock_data in allocations.items():
            dock_str = str(dock)

            for data in dock_data:
                vehicle = data["Vehicle"]
                destination = data["Destination"]
                dock_in_time = convert_to_mysql_datetime(data["Dock In Time"])  # Convert datetime string

                sql = (
                    f"INSERT INTO allocated (dock_number, vehicle_data, destination, dock_in_time, status) "
                    f"VALUES ('{dock_str}', '{vehicle}', '{destination}', '{dock_in_time}', 'INPROGRESS') "
                    f"ON DUPLICATE KEY UPDATE "
                    f"vehicle_data = '{vehicle}', destination = '{destination}', dock_in_time = '{dock_in_time}', status = 'INPROGRESS';"
                )

                try:
                    cursor.execute(sql)
                    conn.commit()
                    print(f"Data for dock {dock_str} updated successfully in the database.")
                except Exception as e:
                    conn.rollback()
                    print(f"Error updating data for dock {dock_str}: {e}")



def update_allocations():
    df = pd.read_csv(f"ob_{get_shift()}.csv", dtype=str)  
    unique_vehicles = df.drop_duplicates(subset='VEHICLE NO')
    allocated_docks.clear()
    for index, row in unique_vehicles.iterrows():
        dock = row["DOCK"]
        vehicle = row["VEHICLE NO"]
        destination = row["Destination"]
        status = row["STATUS"]
        dock_in_time = row["DOCK  IN TIME"]

        if status == "INPROGRESS":  
            if dock not in allocated_docks:
                allocated_docks[dock] = []

            allocated_docks[dock].append({
                "Vehicle": vehicle,
                "Destination": destination,
                "Status": status,
                "Dock In Time": dock_in_time
            })

    print(allocated_docks)
    update_database(allocated_docks)

def truncate_table(table_name):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {table_name}")
            conn.commit()
            print(f"Table '{table_name}' truncated")
    except Exception as e:
        print(f"Error truncating the table: {e}")


while True: 
    shift = get_shift()
    print(shift)
    download_sheet(shift)
    truncate_table("allocated")
    update_allocations()
    time.sleep(60)   