import requests
import webbrowser
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
import PySimpleGUI as sg
import sys
import os
from webdriver_manager.chrome import ChromeDriverManager

discord_base_url = 'https://discord.com/channels/@me'
discord_redirect_url = 'https://discord.com/login?redirect_to=%2Fchannels%2F%40me'


def main():

    # First, get users phone/email and password
    username, password = username_password_GUI()

    # Opens the discord dashboard in browser
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(discord_base_url)

    try:
        print("Attempting Login to page style 1")

        email_or_phone_xpath = '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input'
        password_xpath = '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[2]/div[2]/div/input'
        submit_xpath = '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[2]/button[2]'

        login(driver, email_or_phone_xpath=email_or_phone_xpath, password_xpath=password_xpath, submit_xpath=submit_xpath, username=username, password=password)

    except:
        print('Login failed, must be page style 2')

        email_or_phone_xpath = '/html/body/div/div[2]/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input'
        password_xpath = '/html/body/div/div[2]/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input'
        submit_xpath = '/html/body/div/div[2]/div/div/div/form/div/div/div[1]/div[2]/button[2]'

        login(driver, email_or_phone_xpath=email_or_phone_xpath, password_xpath=password_xpath, submit_xpath=submit_xpath, username=username, password=password)

    time.sleep(5)

    # With the dashboard open, now to change online status
    online_status_xpath = '/html/body/div/div[2]/div/div[2]/div/div/div/div/div[1]/section/div[2]/div[1]'
    online_status_button = driver.find_element_by_xpath(online_status_xpath)

    # Click the button
    online_status_button.click()

    # Wait for the status button to show up
    time.sleep(0.25)

    # Then click invisible
    invisible_status_xpath = '/html/body/div/div[6]/div/div/div/div/div[5]/div'
    invisible_status = driver.find_element_by_xpath(invisible_status_xpath)
    invisible_status.click()

    # Just to ensure everything went right!
    time.sleep(2)


def login(driver, email_or_phone_xpath, password_xpath, submit_xpath, username, password):

    email_or_phone_input = driver.find_element_by_xpath(email_or_phone_xpath)
    password_input = driver.find_element_by_xpath(password_xpath)

    submit = driver.find_element_by_xpath(submit_xpath)

    email_or_phone_input.send_keys(username)
    password_input.send_keys(password)

    submit.click()


def username_password_GUI():

    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Please enter your email/phone and password below in the corresponding fields!')],
        [sg.Text('Email/Phone'), sg.InputText()],
        [sg.Text('Password'), sg.InputText(password_char="*")],
        [sg.Button('Submit'), sg.Button('Exit')]
    ]

    window = sg.Window('Discord_Appear_Offline', layout)

    Done = False

    while not Done:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            exit()
        elif event == 'Submit' and values[0] != '' and values[1] != '':
            print(values)

            username = values[0]
            password = values[1]

            Done = True

        else:
            continue

    window.close()

    return username, password

if __name__ == '__main__':
    main()