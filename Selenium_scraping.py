from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd

import requests
from bs4 import BeautifulSoup

# jobs = {"Data Analyst", "Data Scientist"}
# locations = {'India', 'Singapore'}


def get_job_postings(keyword, location):
    job_data = []

    url = "https://www.glassdoor.co.in/Job/index.htm"  # Replace with the website URL you want to interact with
    path = "C:/selenium drivers/chromedriver-win64/chromedriver.exe"

    options = Options()
    options.headless = False
    options.add_argument("user-agent=Chrome/115.0.5790.171")

    driver = webdriver.Chrome(options=options, service=Service(path))
    driver.get(url)

    # sign in
    sign_in = driver.find_element(By.ID, "SignInButton")
    sign_in.click()
    driver.switch_to.window(driver.window_handles[-1])

    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    condition = ec.presence_of_element_located((By.ID, "modalUserEmail"))
    wait.until(condition)

    driver.implicitly_wait(10)
    email_input = driver.find_element(By.ID, "modalUserEmail")
    email_input.send_keys("kiramisogi@gmail.com")
    email_input.send_keys(Keys.ENTER)

    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    condition = ec.presence_of_element_located((By.ID, "modalUserPassword"))
    wait.until(condition)

    password_input = driver.find_element(By.ID, "modalUserPassword")
    password_input.send_keys("Kira@misogi1415")
    password_input.send_keys(Keys.ENTER)

    # Switch back to the main window/tab
    driver.switch_to.window(driver.window_handles[0])

    # job title
    job_element = driver.find_element(By.ID, 'searchBar-jobTitle')
    job_element.send_keys(keyword)
    job_element.send_keys(Keys.ENTER)
    driver.implicitly_wait(15)

    # job location
    location_element = driver.find_element(By.ID, 'searchBar-location')
    location_element.send_keys(location)
    location_element.send_keys(Keys.ENTER)
    driver.implicitly_wait(20)
    driver.switch_to.window(driver.window_handles[-1])

    wait = WebDriverWait(driver, 100)  # Wait up to 10 seconds
    condition = ec.presence_of_element_located((By.CLASS_NAME, "modal_main gdGrid css-1gy9wmw e8e8plt4"))
    wait.until(condition)
    close_pop = driver.find_element(By.CLASS_NAME, "gd-ui-button.editState.css-8atqhb.e8e8plt0.css-1rp50a3.evpplnh1")
    close_pop.click()
    # close_pop = driver.find_element(By.XPATH, "//*[@id='JAModal']/div/div[2]/span")
    # close_pop.click()

    # driver.switch_to.window(driver.window_handles[0])

    # save urls
    WebDriverWait(driver, 10).until(ec.url_changes(driver.current_url))
    website = driver.current_url

    driver.implicitly_wait(10)
    payload = {'api_key': 'b625656fd1d9a0117348372bbe0c9875',
               'url': website}
    response = requests.get('https://api.scraperapi.com', params=payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")

        job_cards = soup.find_all('li', {'class': 'react-job-listing css-108gl9c eigr9kq3'})
        print(len(job_cards))
        for card in job_cards:
            job_type = keyword
            title = card.find('div', {'class': 'job-title mt-xsm'}).text.strip()
            company = card.find('div', {'class': 'job-search-8wag7x'}).text.strip()
            loc = card.find('div', {'class': 'location mt-xxsm'}).text.strip()
            job_data.append({'Job': job_type, 'Title': title, 'Company': company, 'Location': loc})

            return job_data
    else:
        print(f"Failed to fetch data: Status Code {response.status_code}")
        return None


if __name__ == "__main__":
    keyword_to_search = input("Enter the job keyword to search: ")
    location_to_search = input("Enter the location to search: ")
    job_postings = get_job_postings(keyword_to_search, location_to_search)
    jobs = pd.DataFrame(job_postings)
    print(jobs)
