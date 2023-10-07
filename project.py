from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time


SERVICE = Service('C:/Users/doga/OneDrive/Masaüstü/chromedriver.exe')
DRIVER = webdriver.Chrome(service=SERVICE)


def log_in():
    DRIVER.get('https://www.linkedin.com/jobs/search/?currentJobId=3394302772&geoId=102105699&keywords=developer&location=T%C3%BCrkiye&refresh=true')
    DRIVER.maximize_window()
    time.sleep(3)
    sign_in_button = DRIVER.find_element(By.XPATH, '/html/body/div[1]/header/nav/div/a[2]')
    sign_in_button.click()

    time.sleep(3)
    e_mail = DRIVER.find_element(By.NAME, 'session_key')
    e_mail.send_keys() # LinkedIn E-mail

    password = DRIVER.find_element(By.NAME, 'session_password')
    password.send_keys() # LinkedIn Password

    button = DRIVER.find_element(By.CSS_SELECTOR, '.login__form_action_container button')
    button.click()

log_in()

def get_skill_data():

    skills_button = DRIVER.find_element(By.CSS_SELECTOR, '.jobs-unified-top-card__job-insight-text-button span')
    skills_button.click()
    time.sleep(2)
    skills = DRIVER.find_elements(By.CSS_SELECTOR, '.job-details-skill-match-status-list li div div')

    skills_needed = []
    for skill in skills:
        skills_needed.append(skill.text)

    for i in skills_needed:
        if len(i) == 0:
            skills_needed.remove(i)

    close_button = DRIVER.find_element(By.CSS_SELECTOR, '.jobs-skill-match-modal button')
    close_button.click()
    time.sleep(2)

    return skills_needed

def scroll():
    overflow_bar = DRIVER.find_element(By.CLASS_NAME, "overflow-x-hidden")
    for p in range(5):
        DRIVER.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", overflow_bar)


# ======================================================================== #

time.sleep(25)

job_type = []
company_name = []
company_location = []
applicant_count = []
job_title = []
company_field = []
number_of_workers = []
job_description = []
short_description = []
job_link = []
expected_skills = []


def scrape_all_datas():
    all_listings = DRIVER.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
    for listing in all_listings:
        listing.click()
        time.sleep(3)
        try:
            company_field.append([i.text for i in DRIVER.find_elements(By.CSS_SELECTOR, '.jobs-unified-top-card__job-insight span')][1].split('·')[1])
            job_type.append(DRIVER.find_element(By.CSS_SELECTOR, '.jobs-unified-top-card__job-insight span').text)
            company_name.append(DRIVER.find_element(By.CSS_SELECTOR, '.jobs-unified-top-card__company-name a').text)
            company_location.append(DRIVER.find_element(By.CLASS_NAME, 'jobs-unified-top-card__bullet').text)
            applicant_count.append(DRIVER.find_element(By.CLASS_NAME, 'jobs-unified-top-card__applicant-count').text.split(' ')[0])
            job_title.append(DRIVER.find_element(By.CSS_SELECTOR, '.ember-view h2').text)
            number_of_workers.append(DRIVER.find_element(By.CLASS_NAME, 'jobs-company__inline-information').text.split(' ')[0])
            expected_skills.append(get_skill_data())
            job_description.append(DRIVER.find_element(By.XPATH, '//*[@id="job-details"]/span').text)
            short_description.append(DRIVER.find_element(By.CSS_SELECTOR, '.jobs-company__box p div').text.split("…")[0])
            job_link.append(DRIVER.find_element(By.CLASS_NAME, 'job-card-list__title').get_attribute("href"))

            DRIVER.execute_script("arguments[0].scrollIntoView();", listing)
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            continue


# ========================================================== #

last_page = 9

scrape_all_datas()
for i in range(1, last_page):
    pages = DRIVER.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator.artdeco-pagination__indicator--number')
    pages[i].click()
    time.sleep(5)
    scrape_all_datas()
    if i == 8:
        while last_page < 15:
            pages = DRIVER.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator.artdeco-pagination__indicator--number')
            pages[6].click()
            last_page += 1
            time.sleep(5)
            scrape_all_datas()



df = pd.DataFrame(list(zip(company_field, job_type, company_name, company_location, applicant_count, job_title, number_of_workers, expected_skills, job_description, short_description, job_link)),
                  columns=['company_field', 'job_type', 'company_name', 'company_location', 'applicant_count', 'job_title', 'number_of_workers', 'expected_skills', 'job_description', 'short_description', 'job_link'])

df.to_excel('job_listings', encoding='utf-8-sig', index=False)




