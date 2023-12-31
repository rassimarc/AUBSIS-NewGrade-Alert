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
    driver.get('https://sisxe.aub.edu.lb/StudentSelfService/ssb/studentProfile')

    # Find and input username and password
    username = driver.find_element(by='name', value='usernameUserInput')
    password = driver.find_element(by='name',value='password')

    username.send_keys(os.getenv('AUBSISID'))
    password.send_keys(os.getenv('PASSWORD'))

    # Find and click the login button
    login_button = driver.find_element(By.XPATH, value='/html/body/main/div/div/div/form/div[9]/div[2]/button')
    login_button.click()
    time.sleep(20)

def getCredits():
    try:
        credits = driver.find_element(By.ID, value='spp_overall_hours')
        numberOfCredits = int(credits.text)
        if credits==None:
            login()
            credits = driver.find_element(By.ID, value='spp_overall_hours')
        return numberOfCredits
    except:
        login()
        return getCredits()

currentCredits = getCredits_DB()

while True:
    credits = getCredits()
    if credits != currentCredits:
        sendNotification()
        updateCredits(credits)
        currentCredits = credits
    time.sleep(1800)
