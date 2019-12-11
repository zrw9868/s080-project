from bs4 import BeautifulSoup as soup
from lxml import html
import requests 
from selenium import webdriver
import time


url = "https://www.wunderground.com/history/daily/KLGA/date/2019-1-1"
driver = webdriver.Firefox(executable_path = '/downloads/geckodriver.exe')
driver.get(url)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(30)


result = driver.find_element_by_class_name("observation-table ng-star-inserted")




print(result)


