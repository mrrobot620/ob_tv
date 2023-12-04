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