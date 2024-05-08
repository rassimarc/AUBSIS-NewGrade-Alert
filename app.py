import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import http.client, urllib
import os
from dotenv import load_dotenv
import sqlite3

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

load_dotenv()

def getCredits_DB():
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('database.sqlite')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Select the value from the 'number' column of the 'credits' table
    cursor.execute('SELECT number FROM credits')

    # Fetch the result (assuming only one row exists, or use fetchone() for a single result)
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    return result[0]

def updateCredits(credits):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('database.sqlite')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Update the value in the 'number' column of the 'credits' table
    cursor.execute('UPDATE credits SET number = ?', (credits,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def sendNotification():
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": os.getenv('TOKEN'),
        "user": os.getenv('USER_TOKEN'),
        "title": "New Grade Alert",
        "message": "A new grade has been posted on AUBsis",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()


def login():
    driver.get('https://www-banner.aub.edu.lb/pls/weba/twbkwbis.P_WWWLogin')

    # Find and input username and password
    username = driver.find_element(by='name', value='sid')
    password = driver.find_element(by='name',value='PIN')

    username.send_keys(os.getenv('AUBSISID'))
    password.send_keys(os.getenv('PASSWORD'))

    # Find and click the login button
    login_button = driver.find_element(By.XPATH, value='/html/body/div[19]/div[3]/div[2]/div[1]/form/div/div/button')
    login_button.click()

    student_services = driver.find_element(By.ID, value='bmenu--P_StuMainMnu___UID1')
    student_services.click()
    time.sleep(1)

    student_records = driver.find_element(By.XPATH, value='/html/body/div[19]/div[3]/div[2]/div[2]/div/div[1]')
    student_records.click()
    time.sleep(1)

    final_grades = driver.find_element(By.ID, value='contentItem12')
    final_grades.click()
    time.sleep(1)

    submit_button = driver.find_element(By.XPATH, value='/html/body/div[3]/div[4]/div[2]/div[1]/div[3]/form/button')
    submit_button.click()
    time.sleep(1)

def getCredits():
    try:
        driver.refresh()
        credits = driver.find_element(By.XPATH, value='/html/body/div[3]/div[4]/div[2]/div[1]/div[2]/table[3]/tbody/tr[5]/td[2]/p')
        numberOfCredits = int(float(credits.text))
        print(numberOfCredits)
        return numberOfCredits
    except:
        login()
        return getCredits()

currentCredits = getCredits_DB()

while True:
    try:
        credits = getCredits()
        if credits != currentCredits:
            sendNotification()
            updateCredits(credits)
            currentCredits = credits
    except:
        pass
    time.sleep(1800)
