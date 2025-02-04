"""Gym Automatic Booking System"""

import sys
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
LOGIN_URL = 'https://██████████████.co.uk/login'
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
CLASS_NAME = sys.argv[3]

if len(sys.argv) > 4:
    INSTRUCTOR = sys.argv[4]
else:
    INSTRUCTOR = ""

def setup_driver():
    """
    Set up the driver for the program.

    This function initializes and configures the driver for the program.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-breakpad')
    options.add_argument('--disable-client-side-phishing-detection')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-password-generation')

    browser_driver = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=browser_driver, options=options)

def login(driver, username, password):
    """
    Perform user login.

    This function handles the login process for the user.
    """
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.NAME, 'login'))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.NAME, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']"))).click()

def navigate_to_classes(driver):
    """
    Navigate to the classes page.

    This function handles the navigation to the classes page.
    """
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@title='Book Classes']"))).click()
    day = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        # select the last button available, the third
        (By.XPATH, "//*[@id='event-booking-date-select']/li[2]")))
    logging.info("Found button for the day %s!",day.text)

    day.click()

def find_class(driver, class_name, instructor):
    """
    Find a class.

    This function searches for a specific class.
    """

    gym_classes = list(WebDriverWait(driver, 6).until(
            EC.visibility_of_any_elements_located((By.XPATH, ".//div[@class='class grid']"))))

    for gym_class in gym_classes:

        title = gym_class.find_element(By.CLASS_NAME, 'title').text
        instructor_assigned = gym_class.find_element(By.CSS_SELECTOR, '.description p').text

        if (title == class_name) and (instructor == ""  or (instructor in instructor_assigned)):
            logging.info("Found class %s %s!",class_name, instructor_assigned)
            return gym_class

    return None

def book_class(gym_class):
    """
    Book a class.

    This function handles the process of booking a class.
    """
    remaining_spaces = int(gym_class.find_element(By.CLASS_NAME, 'label').text.split()[-1])
    if remaining_spaces > 0:
        gym_class.find_element(By.CLASS_NAME, 'signup').click()
        logging.info("Class Booked! :)")
    else:
        gym_class.find_element(By.CLASS_NAME, 'waitinglist').click()
        logging.info("Joined the waiting list! :(")

def main():
    """
    Main function to initiate the gym class booking process.

    This function performs the following steps:
    1. Sets up the web driver.
    2. Logs in to the gym booking system.
    3. Navigates to the classes page.
    4. Searches for the specified class.
    5. Attempts to book the class if available, otherwise joins the waiting list.
    6. Logs the total duration of the process.
    """
    start_time = datetime.now()
    logging.info("User %s is trying to book %s...", USERNAME, CLASS_NAME)

    driver = setup_driver()

    try:
        login(driver, USERNAME, PASSWORD)
        navigate_to_classes(driver)

        gym_class = find_class(driver, CLASS_NAME, INSTRUCTOR)

        if gym_class:
            book_class(gym_class)
        else:
            logging.info("Class not found! :(")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logging.error("An error occurred: %s", e)
    finally:
        driver.quit()

    end_time = datetime.now()
    duration = end_time - start_time
    logging.info("Time taken: %s", str(duration)[:-7])

if __name__ == "__main__":
    main()
