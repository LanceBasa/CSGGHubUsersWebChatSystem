import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_logout_check(driver):
    #get the address
    driver.get("http://127.0.0.1:5000/login")

    # Find the username and password input fields
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "submit")

    #test for non-registered user
    username_input.send_keys("notRegisteredUsername")
    password_input.send_keys("notRegisteredPassword")
    time.sleep(3)
    login_button.click()

    try:
        success_message = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "loginForm"))
        )
        print("Reject non-registered user -- Pass")
    except:
        print("Reject non-registered user -- Failed")

    time.sleep(2)

    #test for registered user
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "submit")

    # Enter the username and password
    username_input.send_keys("bobby")
    password_input.send_keys("1234")
    time.sleep(2)

    # Submit the login form
    login_button.click()

    # Wait for the page to load and check if the login was successful
    try:
        success_message = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='profileInfo offset-1 col-9']"))
        )
        print("Login registered user -- Pass")
    except:
        print("Login registered user -- Fail")

    time.sleep(2)
    logout_button= driver.find_element(By.XPATH, '//a[@href="/logout"]')
    logout_button.click()

    # Wait for a few seconds before closing the browser
    time.sleep(2)

    login_nav= driver.find_element(By.XPATH, '//a[@href="/login"]')
    login_nav.click()
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "submit")

    # Enter the username and password
    username_input.send_keys("bobby")
    password_input.send_keys("1234")
    login_button.click()
    time.sleep(2)




def edit_profile_check(driver):
    editProfileButton=driver.find_element(By.XPATH, '//a[@href="/edit_profile"]')
    editProfileButton.click()
    time.sleep(1)
    

    time.sleep(10)




# Test with Chrome
chrome_driver = webdriver.Chrome()
login_logout_check(chrome_driver)
chrome_driver.close()


# Test with Firefox
firefox_driver = webdriver.Firefox()
login_logout_check(firefox_driver)
firefox_driver.close()
