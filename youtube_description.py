from selenium_stealth import stealth
import selenium
import undetected_chromedriver.v2 as uc
import time
import os


username = "benchon27@gmail.com"
password = "Pest7082!"

def login():
    # Create empty profile
    os.mkdir('./chrome_profile')
    Path('./chrome_profile/First Run').touch()

    options = uc.ChromeOptions()
    options.add_argument('--user-data-dir=./chrome_profile/')
    driver = uc.Chrome(options=options)
    with driver:
        driver.get(
            "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAmgQ")
        driver.find_element_by_xpath("//input[@type='email']").send_keys(username)
        driver.find_element_by_xpath("//span[text()='Next']").click()
        driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_xpath("//span[text()='Next']").click()
        time.sleep(20)

if __name__ == '__main__':
    login()