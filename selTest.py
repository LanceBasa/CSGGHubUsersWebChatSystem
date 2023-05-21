import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_and_check(driver):
    driver.get("http://127.0.0.1:5000/login")

    # Find the username and password input fields
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    # Enter the username and password
    username_input.send_keys("bobby")
    password_input.send_keys("1234")
    time.sleep(3)

    # Submit the login form
    login_button = driver.find_element(By.NAME, "submit")
    login_button.click()

    # Wait for the page to load and check if the login was successful
    try:
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='profileInfo offset-1 col-9']"))
        )
        print("Login successful!")
    except:
        print("Login failed!")

    # Wait for a few seconds before closing the browser
    time.sleep(10)

    # Close the browser
    driver.quit()


# Test with Chrome
chrome_driver = webdriver.Chrome()
login_and_check(chrome_driver)


# Test with Firefox
firefox_driver = webdriver.Firefox()
login_and_check(firefox_driver)
