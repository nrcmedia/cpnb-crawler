import time
import pickle
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
def init_driver():
    driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
 
def lookup(driver, query):
    driver.get('https://www.debestseller60.nl/index.asp')
    try:
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, "btnGoPrev")))
        button.click()
    except TimeoutException:
        print("Button not found on site")
 
 
def scrape(html):

	soup = BeautifulSoup(html)

	week = soup.find('span', {'id': 'spnWeek'}).text.strip()
	week = week.replace('\n', ' ').replace('\r', '')

	week = re.sub(' ', '', week)
	week = re.sub('-week,', '', week)
	print week
	titels = [h2.text for h2 in soup.findAll('h2')]
	with open('boeken/' + str(week) + '.html', 'w') as html_out:
		html_out.write(html.encode('utf-8'))
	return [week].append(titels)

if __name__ == "__main__":
    driver = init_driver()
    data = []
    while True:
	    lookup(driver, "Selenium")
	    data.append(scrape(driver.page_source))

	    pickle.dump(data, open('boekentop60.p', 'wb'))
	    time.sleep(2)
    driver.quit()