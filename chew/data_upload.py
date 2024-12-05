from data import all
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep  # Import sleep for delays

from selenium.webdriver.chrome.service import Service
options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options)



login = "http://192.168.1.101/candidate/auth"
answers = ['answeru2753', 'answeru2753', 'answeru2753', 'answeru2753']

try:
    for i in all:
        try:
            driver.get(login)
            username = i
            password = all[i].split()[0].lower()

            # Find username and password fields
            username_field = driver.find_element(By.NAME, "username")  # Replace with actual field name or ID
            password_field = driver.find_element(By.NAME, "password")  # Replace with actual field name or ID

            # Enter credentials
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            lga_field = Select(driver.find_element(By.NAME, "test_id"))
            lga_field.select_by_value(5)

            # Find login button and submit
            login_button = driver.find_element(By.XPATH, "//button[text()='Sign in']") # Adjust selector if needed
            login_button.click()

            # Wait for login to complete (adjust timeout if necessary)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "username")))  # Replace with an element appearing after login
            sleep(1)
            
            start_button = driver.find_element(By.XPATH, "//button[text()='Start Exam']") # Adjust selector if needed
            start_button.click()
            sleep(1)
            random.shuffle(answers)
            for i in answers:
                radio_button = driver.find_element(By.ID, i)
                radio_button.click()
                sleep(0.01)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "wizardForm")))  # Replace with an element appearing after login
            sleep(1)
            
        except Exception as e:
            print("This is error:",i)
    
except Exception as e:
    print(f"Error during execution: {e}")

 # Ensure the WebDriver is properly closed
# finally:
#     driver.quit()