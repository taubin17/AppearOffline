import time
import PySimpleGUI as sg
import os
from pathlib import Path
import SteamLogin


steam_config_path = Path(os.getenv('APPDATA')) / 'Go O'


def prompt_login():
    print('Prompting Login')
    sg.popup('Please sign into your Steam account using the Steam application!')


def login(driver, username_css, password_css, submit_xpath, username, password):
    username_input = driver.find_element_by_css_selector(username_css)
    password_input = driver.find_element_by_css_selector(password_css)

    submit = driver.find_element_by_xpath(submit_xpath)

    username_input.send_keys(username)
    password_input.send_keys(password)

    submit.click()
    return


'''
def get_driver():
    # Enable headless options
    options = webdriver.ChromeOptions()

    # options.add_argument('--headless')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-default-apps')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Opens the discord dashboard in browser
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver
'''


def set_offline():

    # Check if a user is logged in. If not, log them in
    if SteamLogin.get_login_status() is False:
        # LOGIN
        print('Login')
        prompt_login()
        return -1

    os.system('start steam://friends/status/invisible')

    return 0


def set_online():

    # Check if the user is logged in. If not, log them in
    if SteamLogin.get_login_status() is False:
        # LOGIN
        print('Login')
        prompt_login()
        return -1

    os.system('start steam://friends/status/online')

    return 0


if __name__ == '__main__':
    set_offline()
    time.sleep(3)
    set_online()