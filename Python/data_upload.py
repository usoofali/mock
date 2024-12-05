from data import paper_remark, links,lga,lgas

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
password = '123456'

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
    photos = 'photos'
    if not os.path.exists(photos):
        print("Folder photos does not exist.")
        exit()
    directory = photos
    absolute_directory = os.path.abspath(directory)
    cnt = 0
    for filename in os.listdir(photos):
        cnt += 1
        file_path = os.path.join(absolute_directory, filename)

        if os.path.isfile(file_path):
            try:
                
                
                index, bg, gender, dob, phone, email = os.path.splitext(filename)[0].split("_")
                ind0, ind1, ind2, ind3 = index.split('.')
                new_path = f"{ind0}/{ind1}/{ind2}/{ind3}"

                if new_path in links:
                    driver.get(links[new_path])
                    # WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, "picture-upload")))
                    # sleep(1)
                    
                    gender_select = Select(driver.find_element(By.NAME, "gender"))
                    gender_select.select_by_value(gender)  # Or use select_by_value if you know the value

                    # Date of Birth input
                    
                    dob_field = driver.find_element(By.NAME, "dob")
                    driver.execute_script("arguments[0].value = arguments[1];", dob_field, dob)
                    
                    lga_key = lgas[lga[new_path]]
                    lga_field = Select(driver.find_element(By.NAME, "lga_id"))
                    lga_field.select_by_value(lga_key)

                    # Blood Group dropdown
                    blood_group_select = Select(driver.find_element(By.NAME, "blood_group"))
                    blood_group_select.select_by_value(bg)  # Or use select_by_value if you know the value
                    
                    paper_rem = paper_remark[new_path]
                    remark = paper_rem[1]
                    papers = paper_rem[0]
                    
                    remark_select = Select(driver.find_element(By.NAME, "remark"))
                    remark_select.select_by_value(remark)  # Or use select_by_value if you know the value
                    
                    paper_select = Select(driver.find_element(By.ID, "papers"))
                    if remark == "fresh":
                        paper_select.select_by_value("1") 
                        paper_select.select_by_value("2") 
                        paper_select.select_by_value("3") 
                        paper_select.select_by_value("4") 
                        paper_select.select_by_value("5")
                    else:
                        result = papers.split(",")
                        cnts = 1
                        for i in result:
                            cnts+=1
                            paper_select.select_by_value(str(cnts))
                            
                    
                     # Or use select_by_value if you know the value

                    # Phone input
                    phone_field = driver.find_element(By.NAME, "phone")
                    phone_field.clear()  # Clear the field before sending keys
                    phone_field.send_keys(phone)  # Ensure phone is formatted correctly

                    # Email input
                    email_field = driver.find_element(By.NAME, "email")
                    email_field.clear()  # Clear the field before sending keys
                    email_field.send_keys(email)  # Ensure email is formatted correctly
                    
                    update_button = driver.find_element(By.XPATH, '//button[text()="Update"]')
                    update_button.click()

                    # Wait for update to complete
                    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, "picture-upload")))
                    
                    driver.get(links[new_path])
                    
                    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, "picture-upload")))
                    sleep(2)
                    dropzone = driver.find_element(By.ID, 'dropzone')
                    

                    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                    file_input.send_keys(file_path)

                    # # Wait for the form fields to be available
                    WebDriverWait(driver, 65).until(EC.presence_of_element_located((By.ID, "picture-upload")))
                    
                    driver.get(links[new_path])
                    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, "picture-upload")))
                    # sleep(2)
                    
                    print(str(cnt) +"-"+ new_path)
                    # sleep(20)

                    
                else:
                    print(f"Link for {new_path} not found in links dictionary.")
                    continue

                
            except Exception as e:
                print(f"Could not process {filename}: {e}")
except Exception as e:
    print(f"Error during execution: {e}")

 # Ensure the WebDriver is properly closed
# finally:
#     driver.quit()