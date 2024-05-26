# requires firefox

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

gecko_path = "geckodriver.exe"


def article():
    website = "https://www.cnbc.com/search/?query=market&qsearchterm=markets"
    links = []
    link = ""

    options = Options()
    options.headless = False
    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(website)
    driver.implicitly_wait(6)

    try:
        try:
            for i in range(4):
                i += 1
                link = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[3]/div/div/div/div/div/div[2]/div/section/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[2]/div['+str(i)+']/div/div[2]/div[2]/a')
                links.append(link.get_attribute("href"))

        except NoSuchElementException:
            link = "error"

        if link != "":
            for link_ in links:
                print(link_)

    finally:
        driver.quit()


article()
