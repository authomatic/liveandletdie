import requests
from pyvirtualdisplay import Display
from selenium import webdriver

requests.packages.urllib3.disable_warnings()


def get_browser():
    global display
    display = Display(visible=0, size=(1024, 768))
    display.start()
    browser = webdriver.Firefox()
    return browser


def teardown():
    display.stop()