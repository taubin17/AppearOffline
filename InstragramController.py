from selenium import webdriver
import time
import PySimpleGUI as sg
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
from pathlib import Path
import win32api
import requests
import re
from mozdownload import FactoryScraper
import get_geckodriver

instagram_base_url = 'https://www.instagram.com'
instagram_config_path = Path(os.getenv('APPDATA')) / 'Go O'
instagram_config_filename = 'instagram_config.cfg'


def get_to_status():

    # First, get users phone/email and password
    username, password = username_password_GUI()

    if username == 'Quit' and password == 'Quit':
        return 'Quit'

    driver = get_driver_firefox()
    driver.get(instagram_base_url)

    time.sleep(2.5)

    print("Attempting Login to page style 1")

    email_phone_username_css = '#loginForm > div > div:nth-child(1) > div > label > input'
    password_css = '#loginForm > div > div:nth-child(2) > div > label > input'
    submit_css = '#loginForm > div > div:nth-child(3) > button'

    login(driver, email_or_phone_css=email_phone_username_css, password_css=password_css, submit_css=submit_css, username=username, password=password)

    time.sleep(3)

    # Now need to get passed remember me screen
    remember_me_css_selector = '#react-root > section > main > div > div > div > div > button'
    remember_me_input = driver.find_element_by_css_selector(remember_me_css_selector)
    remember_me_input.click()

    time.sleep(0.5)

    # Turn off notifications
    notifications_off_css_selector = 'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm'
    notifications_off_input = driver.find_element_by_css_selector(notifications_off_css_selector)
    notifications_off_input.click()

    time.sleep(0.5)

    # Click on profile picture
    profile_picture_css_selector = '#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg > div > div:nth-child(5) > span > img'
    profile_picture_input = driver.find_element_by_css_selector(profile_picture_css_selector)
    profile_picture_input.click()

    time.sleep(0.5)

    # Click settings
    settings_css_selector = '#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg > div > div:nth-child(5) > div.poA5q > div.uo5MA._2ciX.tWgj8.XWrBI > div._01UL2 > a:nth-child(3) > div'
    settings_input = driver.find_element_by_css_selector(settings_css_selector)
    settings_input.click()

    time.sleep(0.5)

    # Click privacy
    privacy_css_selector = '#react-root > section > main > div > ul > li:nth-child(7) > a'
    privacy_input = driver.find_element_by_css_selector(privacy_css_selector)
    privacy_input.click()

    return driver


# Opens a Chrome Selenium driver with necessary options such as headless, and other options to hide from browser
def get_driver_chrome():
    # Set the screen size to be maximized
    width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    size_option = f'--window-size={width},{height}'

    # Enable headless options
    options = webdriver.ChromeOptions()

    # options.add_argument(size_option)
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-default-apps')
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--disable-blink-features=AutomationControlled')

    # Opens the instagram dashboard in browser
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # test = 'cdc_asdjflasutopfhvcZLmcfl_'
    # print(len(test))

    # pattern = r'Headless'

    # user_agent = driver.execute_script("return navigator.userAgent")
    # print(f'Before: {user_agent}')
    # user_agent = re.sub(pattern, '', user_agent)
    # print(f'After: {user_agent}')
    # driver.close()

    # options.add_argument(f'(user-agent={user_agent}')
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver


def get_driver_firefox():

    # Set the screen size to be maximized
    width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    size_option = f'--window-size={width},{height}'

    GeckoDriver = get_geckodriver.install()

    # Enable headless options
    options = webdriver.FirefoxOptions()

    # options.add_argument(size_option)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-default-apps')
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--disable-blink-features=AutomationControlled')

    # Opens the instagram dashboard in browser
    driver = webdriver.Firefox(options=options)

    # pattern = r'Headless'

    # user_agent = driver.execute_script("return navigator.userAgent")
    # print(f'Before: {user_agent}')
    # user_agent = re.sub(pattern, '', user_agent)
    # print(f'After: {user_agent}')
    # driver.close()

    # options.add_argument(f'(user-agent={user_agent}')
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver


def set_offline():

    driver, status = get_status()

    if status is False:
        # This means we are already online
        print('Already False')
        return 0

    online_checkbox_xpath = '/html/body/div[1]/section/main/div/article/main/section[2]/div/div/div/label'
    online_checkbox = driver.find_element_by_xpath(online_checkbox_xpath)
    online_checkbox.click()

    driver.close()

    # IF we are returning here, we were successful, return status 0
    return 0


def get_status():
    driver = get_to_status()

    time.sleep(1)

    # Now to get the status
    online_checkbox_xpath = '/html/body/div[1]/section/main/div/article/main/section[2]/div/div/div/label/input'
    online_checkbox = driver.find_element_by_xpath(online_checkbox_xpath)

    status = online_checkbox.is_selected()

    return driver, status


def set_online():

    # Get the status bar open
    driver, status = get_status()

    if status is True:
        # This means we are already online
        print('Already Online')
        return 0

    online_checkbox_xpath = '/html/body/div[1]/section/main/div/article/main/section[2]/div/div/div/label'
    online_checkbox = driver.find_element_by_xpath(online_checkbox_xpath)
    online_checkbox.click()

    driver.close()

    # IF we are returning here, we were successful, return status 0
    return 0


def login(driver, email_or_phone_css, password_css, submit_css, username, password):

    email_or_phone_input = driver.find_element_by_css_selector(email_or_phone_css)
    password_input = driver.find_element_by_css_selector(password_css)

    submit = driver.find_element_by_css_selector(submit_css)

    email_or_phone_input.send_keys(username)
    password_input.send_keys(password)

    submit.click()

    print('Login Successful!')

    # IF we are returning here, we were successful, return status 0
    return 0


def username_password_GUI():

    username, password = None, None

    # Check if Discord login exists
    if not os.path.exists(instagram_config_path / instagram_config_filename):
        try:
            os.makedirs(instagram_config_path)
        except:
            print('Directories exist, no file created')
    else:
        fd = open(instagram_config_path / instagram_config_filename, 'r')
        username = fd.readline().rstrip()
        password = fd.readline().rstrip()
        fd.close()

        return username, password

    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Please enter your email/phone/username and password below in the corresponding fields!')],
        [sg.Text('Email/Phone/Username'), sg.InputText()],
        [sg.Text('Password'), sg.InputText(password_char="*")],
        [sg.Button('Submit', bind_return_key=True), sg.Button('Exit')]
    ]

    window = sg.Window('Discord_Status_Setup', layout)

    Done = False

    while not Done:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            return 'Quit', 'Quit'
        elif event == 'Submit' and values[0] != '' and values[1] != '':
            print(values)

            username = values[0]
            password = values[1]

            Done = True

        else:
            continue

    window.close()

    fd = open(instagram_config_path / instagram_config_filename, 'w')
    fd.write(username + '\n')
    fd.write(password)
    fd.close()

    return username, password


if __name__ == '__main__':
    set_online()
