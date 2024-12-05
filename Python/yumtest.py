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
username = 'admin'
password = '12345678'

login_url = "https://yumtest.online/login"

# try:
driver.get(login_url)

# Find username and password fields
username_field = driver.find_element(By.ID, "email")  # Replace with actual field name or ID
password_field = driver.find_element(By.ID, "password")  # Replace with actual field name or ID

# Enter credentials
username_field.send_keys(username)
password_field.send_keys(password)

# Find login button and submit
update_button = driver.find_element(By.XPATH, '//button[text()="Login"]')
update_button.click()

# Replace with an element appearing after login
WebDriverWait(driver, 30).until(
EC.presence_of_element_located((By.XPATH, "//h3[@class='mb-3 leading-4 text-gray-600 text-base' and text()='Total Users']"))
)
login_ur = "https://yumtest.online/admin/practice-sets"
driver.get(login_ur)

new_practice_set_link = WebDriverWait(driver, 30).until(
EC.element_to_be_clickable((By.XPATH, "//a[@class='qt-btn qt-btn-success' and text()='New Practice Set']")))
new_practice_set_link.click()

title_field = driver.find_element(By.ID, "title")  # Replace with actual field name or ID

# Enter credentials
title_field.send_keys("MORNING")

dropdown = WebDriverWait(driver, 30).until(
EC.element_to_be_clickable((By.ID, "vs1__combobox"))
)
dropdown.click()

# Now wait for the option to be clickable and select it
desired_option = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='vs__selected' and normalize-space(text())=' SCHEW (COMMUNITY HEALTH WORKERS) ']"))
)
desired_option.click()

# Click the dropdown to open it
dropdown = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "vs2__combobox"))
)
dropdown.click()

# Wait for the desired option to be clickable and select it
desired_option = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='vs__selected' and normalize-space(text())=' DAY 2 (WEEK 2 (1400qts)) ']"))
)
desired_option.click()

checkbox = WebDriverWait(driver, 30).until(
EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @role='switch']"))
)

# Toggle the checkbox (click it)
checkbox.click()
textarea = driver.find_element(By.XPATH, "//textarea")
driver.execute_script("arguments[0].value = arguments[1];", textarea, "Wk2 Dy2")

save_button = WebDriverWait(driver, 30).until(
EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'qt-btn-success')]"))
)
save_button.click()


# except Exception as e:
#     print(f"Error during execution: {e}")

#  # Ensure the WebDriver is properly closed
# finally:
#     # You can add a sleep here if you want to see the result before closing
#     sleep(5)  # Adjust the sleep time as necessary
#     driver.quit()