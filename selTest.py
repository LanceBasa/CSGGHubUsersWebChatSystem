import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


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
    time.sleep(1)
    login_button.click()

    try:
        success_message = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.ID, "loginForm"))
        )
        print("Reject non-registered user -- Pass")
    except:
        print("Reject non-registered user -- Failed")

    time.sleep(1)

    #test for registered user
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "submit")

    # Enter the username and password
    username_input.send_keys("bobby")
    password_input.send_keys("1234")
    time.sleep(1)

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

    time.sleep(1)
    logout_button= driver.find_element(By.XPATH, '//a[@href="/logout"]')
    logout_button.click()

    try:
        success_message = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='col-12 welcomeBlurb']"))
        )
        print("Logout registered user -- Pass")
    except:
        print("Logout registered user -- Fail")

    # Wait for a few seconds before closing the browser
    time.sleep(1)

    login_nav= driver.find_element(By.XPATH, '//a[@href="/login"]')
    login_nav.click()
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "submit")

    # Enter the username and password
    username_input.send_keys("bobby")
    password_input.send_keys("1234")
    login_button.click()
    time.sleep(1)




def edit_profile_check(driver):
    editProfileButton=driver.find_element(By.XPATH, '//a[@href="/edit_profile"]')
    editProfileButton.click()
    time.sleep(1)

    editAboutMe=driver.find_element(By.ID, 'about_me')
    editAboutMe.clear()
    editAboutMe.send_keys("This is a test")  # Set the new text


    time.sleep(1)
    editProfileSubmit=driver.find_element(By.ID, 'submit')
    editProfileSubmit.click()
    
    try:
        success_message = WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='profileInfo offset-1 col-9']"), "This is a test")
        )       
        print("Changed about me -- Pass")
    except:
        print("Changed about me -- Fail")

    time.sleep(1)
    editProfileButton=driver.find_element(By.XPATH, '//a[@href="/edit_profile"]')
    editProfileButton.click()
    editAboutMe=driver.find_element(By.ID, 'about_me')
    editAboutMe.clear()
    editAboutMe.send_keys("This is test 2")  # Set the new text
    checkboxes = driver.find_elements(By.XPATH, '//ul[@class="scroll_editpage"]/li[@class="edit_favs"]/input[@type="checkbox"]')
    for checkbox in checkboxes:
        checkbox.click()
    time.sleep(1)
    editProfileSubmit=driver.find_element(By.ID, 'submit')
    editProfileSubmit.click()
    try:
        success_message = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='gunsAndMaps offset-3 col-3']"))
        )       
        print("Edited Fav weapons -- Pass")
    except:
        print("Edited Fav weapons -- Fail")


    time.sleep(1)


def chat_check(driver):
    chatNav=driver.find_element(By.XPATH, '//a[@href="/chat"]')
    chatNav.click()

    try:
        success_message = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='messages col-4']"))
        )
        print("Check if messages is accessible -- Pass")
    except:
        print("Check if messages is accessible -- Fail")


    time.sleep(1)
    message_input = driver.find_element(By.ID, "message")
    message_input.send_keys("Hello, Selenium!")
    # Submit the new message
    message_input.send_keys(Keys.ENTER)


    try:
        success_message = WebDriverWait(driver, 2).until(
            EC.text_to_be_present_in_element((By.XPATH, "//ul[@id='chatMessages']/li[last()]"), "Hello, Selenium!")
        )
        print("Sending message -- Pass")
    except:
        print("Sending message -- Fail")

    
    profileLink=driver.find_element(By.XPATH, '//a[@href="/profile/bobby"]')
    profileLink.click()

    try:
        success_message = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='profileInfo offset-1 col-9']"))
        )
        print("Clickable username in chat -- Pass")
    except:
        print("Clickable username in chat -- Fail")




    time.sleep(4)





# Test with Chrome
print("---------- Testing with chrome ----------")
chrome_driver = webdriver.Chrome()
login_logout_check(chrome_driver)
edit_profile_check(chrome_driver)
chat_check(chrome_driver)
chrome_driver.close()


# Test with Firefox
print("---------- Testing with Firefox ----------")
firefox_driver = webdriver.Firefox()
login_logout_check(firefox_driver)
edit_profile_check(firefox_driver)
chat_check(firefox_driver)
firefox_driver.close()
