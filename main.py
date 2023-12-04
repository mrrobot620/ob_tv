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

def read_data_from_db():
    sql = "SELECT * FROM allocated"

    # Execute the SQL query
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()  # Fetch all the data

    return result



op = webdriver.ChromeOptions()
# op.add_argument('--headless=new')
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory' : r"/home/administrator/cbs_bag_hold/data",
    'directory_upgrade': True
}
op.add_experimental_option('prefs' , prefs)
driver = webdriver.Chrome(options=op)


driver.get("http://10.24.1.71/tc")

print(driver.title)

def login():
    username = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[1]")
    username.send_keys("ca.2670054")

    password = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
    password.send_keys("Veer@809")


    try:
        cross = driver.find_element(By.XPATH , "/html/body/div[4]/div/button")
        cross.click()
    except:
        print("Cross Button Failed")

    time.sleep(1)

    submit = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/div[4]/button/span")
    submit.click()
    time.sleep(5)

def ekart_Selection():
    try:
        ekart = driver.find_element(By.XPATH , "/html/body/form/label[2]")
        ekart.click()
    except Exception as E:
        print(f"Ekart Not Found {E}")
    try:
        submit = driver.find_element(By.XPATH , "/html/body/form/div/button")
        submit.submit()

    except Exception as e:
        print(f"Submit Button not Found  {e}")


def facility_selection():
    try:
        driver.get("http://10.24.1.71/tc?location=174222&locationExternalId=171385&locationName=MotherHub_YKB")
    except Exception as E:
        print(f"Error {E}")




def load_extractor(vehicle_number):
    try:
        driver.get(f"http://10.24.1.71/tc/loading?contract_type=fleet&location=174222&locationExternalId=171385&locationName=MotherHub_YKB&ptID=1&vehicle={vehicle_number}")
    except Exception as E:
        print(E)
    try:
        load_data = driver.find_element(By.XPATH , "/html/body/div[1]/div/div/div/div/main/div/div/div/div[3]/div[2]/div/div/div/div").text
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div/div/div/div[3]/div[2]/div/div/div/form/div/div[3]/div[2]/div[2]/div/div[3]/button/i").click()
        print(load_data)
    except:
        print("Load Data not Visible")
    return load_data


ekart_Selection()
time.sleep(1)
login()
time.sleep(2)
time.sleep(1)
while True:
    for item in read_data_from_db():
        dock_number = item['dock_number']
        vehicle_data = item['vehicle_data']
        destination = item['destination']
        dock_in_time = item['dock_in_time']
        status = item['status']
        print(f"Dock Number: {dock_number}")
        print(f"Vehicle Data: {vehicle_data}")
        print(f"Destination: {destination}")
        print(f"Dock In Time: {dock_in_time}")
        print(f"Status: {status}")
        load_extractor()
    try:
        with conn.cursor() as cursor:
            sql = f"INSERT INTO dock57(b , c , d , e) VALUES (%s , %s , %s ,%s)"
            cursor.execute(sql , (vehicle , load_extractor() , dock , destination))
            conn.commit()
    except Exception as E:
        print(f"failed to send to sql server {E}" )

