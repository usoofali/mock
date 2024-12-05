from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.support.ui import Select
from time import sleep  # Import sleep for delays

from selenium.webdriver.chrome.service import Service

service = Service("/home/admin/.cache/selenium/chromedriver/linux64/128.0.6613.119/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(options)

# /home/admin/.cache/selenium/chromedriver/linux64/128.0.6613.119
username = 'cshtg130'
password = 'CSHT G'

login_url = "https://app.chprbn.gov.ng/institution/auth"

try:
    driver.get(login_url)

    # Find username and password fields
    username_field = driver.find_element(By.NAME, "username")  # Replace with actual field name or ID
    password_field = driver.find_element(By.NAME, "password")  # Replace with actual field name or ID

    # Enter credentials
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Find login button and submit
    login_button = driver.find_element(By.CSS_SELECTOR, "button.ripple-button-primary")  # Adjust selector if needed
    login_button.click()

    # Wait for login to complete (adjust timeout if necessary)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "content")))  # Replace with an element appearing after login
    login_ur = "https://app.chprbn.gov.ng/institution/uploads"
    driver.get(login_ur)
    
    wait = WebDriverWait(driver, 20)  # 10 seconds timeout
    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-target="#graduandUploadModal"]')))

    # Check if the button is disabled and enable it using JavaScript
    is_disabled = button.get_attribute('disabled') is not None
    if is_disabled:
        driver.execute_script("arguments[0].removeAttribute('disabled')", button)
    
    # Optionally, wait until the button is clickable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-target="#graduandUploadModal"]')))

    # Click the button to toggle the modal
    button.click()

    # Wait for the modal to be visible
    modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#graduandUploadModal')))
    
    # Now you can interact with the modal if needed
    # Example: Interact with an element inside the modal
    # modal_element = modal.find_element(By.CSS_SELECTOR, 'YOUR_ELEMENT_SELECTOR')
    # modal_element.click()
    sleep(60)
except Exception as e:
    print(f"Error during execution: {e}")

 # Ensure the WebDriver is properly closed
# finally:
#     driver.quit()