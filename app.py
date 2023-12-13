import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import http.client, urllib
import os
from dotenv import load_dotenv

driver = webdriver.Chrome()
currentCredits = 144

load_dotenv()

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
        driver.get('https://sisxe.aub.edu.lb/StudentSelfService/ssb/studentProfile')
        credits = driver.find_element(By.XPATH, value='/html/body/div[25]/div[2]/div[1]/ul/li[3]/span/span[2]')
        return credits.text
    except:
        login()
        getCredits()

while True:
    credits = getCredits()
    if credits != currentCredits:
        sendNotification()
        currentCredits = credits
    time.sleep(1800)
