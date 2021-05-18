from selenium import webdriver
import time
import PySimpleGUI as sg
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
from pathlib import Path

discord_base_url = 'https://discord.com/channels/@me'
discord_redirect_url = 'https://discord.com/login?redirect_to=%2Fchannels%2F%40me'
discord_config_path = Path(os.getenv('APPDATA')) / 'Go O'
discord_config_filename = 'discord_config.cfg'

def get_status():

    # First, get users phone/email and password
    username, password = username_password_GUI()

    if username == 'Quit' and password == 'Quit':
        return 'Quit'

    driver = get_driver()
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
    online_status_xpath = '/html/body/div/div[2]/div/div[2]/div/div/div/div/div[1]/section/div[2]/div[1]/div'

    # Get the button
    online_status_button = driver.find_element_by_xpath(online_status_xpath)

    # Click the button
    online_status_button.click()

    # Wait for the status button to show up
    time.sleep(0.25)

    return driver


# Opens a Chrome Selenium driver with necessary options such as headless, and other options to hide from browser
def get_driver():
    # Enable headless options
    options = webdriver.ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-default-apps')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Opens the discord dashboard in browser
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    options.add_argument("--lang=en-US")
    options.add_argument('--plugins=[1, 2, 3, 4, 5]')

    return driver


def set_offline():

    driver = get_status()

    if driver == 'Quit':
        return

    # Click invisible
    invisible_status_xpath = '/html/body/div/div[6]/div/div/div/div/div[5]/div'
    invisible_status = driver.find_element_by_xpath(invisible_status_xpath)
    invisible_status.click()

    # Just to ensure everything went right!
    time.sleep(2)
    driver.close()

    # IF we are returning here, we were successful, return status 0
    return 0

def set_online():

    # Get the status bar open
    driver = get_status()

    # Click online
    visible_status_xpath = '/html/body/div/div[6]/div/div/div/div/div[1]/div'
    visible_status = driver.find_element_by_xpath(visible_status_xpath)
    visible_status.click()

    # Just to ensure everything went right!
    time.sleep(2)
    driver.close()

    # IF we are returning here, we were successful, return status 0
    return 0


def login(driver, email_or_phone_xpath, password_xpath, submit_xpath, username, password):

    email_or_phone_input = driver.find_element_by_xpath(email_or_phone_xpath)
    password_input = driver.find_element_by_xpath(password_xpath)

    submit = driver.find_element_by_xpath(submit_xpath)

    email_or_phone_input.send_keys(username)
    password_input.send_keys(password)

    submit.click()

    print('Login Successful!')

    # IF we are returning here, we were successful, return status 0
    return 0


def username_password_GUI():

    username, password = None, None

    # Check if Discord login exists
    if not os.path.exists(discord_config_path / discord_config_filename):
        try:
            os.makedirs(discord_config_path)
        except:
            print('Directories exist, no file created')
    else:
        fd = open(discord_config_path / discord_config_filename, 'r')
        username = fd.readline().rstrip()
        password = fd.readline().rstrip()
        fd.close()

        return username, password

    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Please enter your email/phone and password below in the corresponding fields!')],
        [sg.Text('Email/Phone'), sg.InputText()],
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

    fd = open(discord_config_path / discord_config_filename, 'w')
    fd.write(username + '\n')
    fd.write(password)
    fd.close()

    return username, password

# if __name__ == '__main__':
    # main()