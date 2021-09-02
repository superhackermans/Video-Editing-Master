from selenium_stealth import stealth
import selenium
import undetected_chromedriver.v2 as uc
import time
import os


username = "benchon27@gmail.com"
password = "Pest7082!"

options = uc.ChromeOptions()
options.add_argument('--user-data-dir=./chrome_profile/')
driver = uc.Chrome(options=options)

def login():
    # Create empty profile
    # os.mkdir('./chrome_profile')
    # Path('./chrome_profile/First Run').touch()
    # stuff to try to stop the driver from freezing, "Timed out receiving message from renderer" jenkins
    # #https://stackoverflow.com/questions/48450594/selenium-timed-out-receiving-message-from-renderer
    # options.add_argument("start-maximized"); # https://stackoverflow.com/a/26283818/1689770
    # options.add_argument("enable-automation"); # https://stackoverflow.com/a/43840128/1689770
    # options.add_argument("--no-sandbox"); #https://stackoverflow.com/a/50725918/1689770
    # options.add_argument("--disable-infobars"); #https://stackoverflow.com/a/43840128/1689770
    # options.add_argument("--disable-dev-shm-usage"); #https://stackoverflow.com/a/50725918/1689770
    # options.add_argument("--disable-browser-side-navigation"); #https://stackoverflow.com/a/49123152/1689770
    # options.add_argument("--disable-gpu"); #https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
    # options.add_argument("--disable-notifications")

    #https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
    with driver:
        driver.get(
            "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAmgQ")
        driver.find_element_by_xpath("//input[@type='email']").send_keys(username)
        driver.find_element_by_xpath("//span[text()='Next']").click()
        driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_xpath("//span[text()='Next']").click()

def description():
    with driver:
        driver.get(
            "https://studio.youtube.com/channel/UC9IZYXzt4dl13MAycfoyMdQ")
        


if __name__ == '__main__':
    login()