import requests
from selenium import webdriver

requests.packages.urllib3.disable_warnings()


def get_browser():
    return webdriver.Chrome()
