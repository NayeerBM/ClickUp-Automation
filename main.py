import sys
import json
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver_service=Service('./driver/geckodriver.exe')

def main():
    global driver
    global wait
    global config_data
    global currentDate
    #check if any arguments have been passed
    if(len(sys.argv)==1):
        print("No arguments passed. Please specify whether to checkin or checkout")
        exit(0)

    try:
        #read from config.json
        with open('config.json','r') as file:
            config_data=json.load(file)

        #check if any value is empty
        for key,value in config_data.items():
            if(not value):
                # print(f"{key} is empty")
                # exit(0)
                display_Error(f"{key} is empty")
        
        driver=webdriver.Firefox(service=driver_service)
        wait=WebDriverWait(driver,10)

        login()
        
        actionType=sys.argv[1]
        if(actionType=="checkin"):
            checkIn()
        elif(actionType=="checkout"):
            checkOut()
        else:
            print('''Invalid argument. Please use "python main.exe <argument>"''')
    
    except Exception as e:
        display_Error(e)        
    
    

    
#Logs into ClickUp
def login():
    #navigate to ClickUp
    driver.get("https://app.clickup.com/login")
    wait.until(EC.presence_of_element_located((By.ID,"login-email-input"))).send_keys(config_data["email"])
    wait.until(EC.presence_of_element_located((By.ID,"login-password-input"))).send_keys(config_data["password"])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"login-page-new__main-form-button"))).click()
    print("Finished logging in")

def checkIn():
    pass

#def checkOut(driver,currentDate):
def checkOut():
    print("Started checkOut function")
    try:
        
        currentDate=date.today().strftime("%d.%m.%Y")
        # driver.get("https://app.clickup.com/3635363/v/l/3ey53-50708/370328")
        
        wait.until(EC.presence_of_element_located((By.XPATH,f"//a[@href='https://app.clickup.com/3635363/v/l/3ey53-50708/3703285']")))
        wait.until(EC.presence_of_element_located((By.XPATH,f"//div[@data-test='nav-section__{currentDate}']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH,f"/html/body/app-root/cu-app-shell/cu-manager/div[1]/div/div[2]/main/cu-dashboard/cu-left-sidebar/div/cu-sidebar-toggle/button"))).click()
        name=config_data["name"]
        element=wait.until( EC.element_to_be_clickable((By.XPATH, f"//span[@data-test='task-row-main__{name}']"))).click()
        # driver.execute_script("return arguments[0].scrollIntoView();", element)
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element.click()
        # elem_not_found = True
        # y = 35 # setting initial scroll pixel size to 10.. find what suits you 
        # while elem_not_found:
        #     try:
        #         ActionChains(driver).scroll_by_amount(0, y).perform()
        #         wait.until( EC.presence_of_element_located((By.XPATH, f"//span[@data-test='task-row-main__{name}']")))
        #         #Once element is loaded do whatever you want with it 
        #         elem_not_found = False
        #     except:
        #         y += 35 # scrolling 35 pixels below if element is not found
    except Exception as e:
        print(e)
        display_Error(e)

def decryptPassword(password):
    NotImplemented

def encryptPassword(password):
    NotImplemented

def display_Error(error_message):
    print(error_message)
    if(isBrowserAlive()==True):
        driver.close()
    exit(0)
    
def isBrowserAlive():
    try:
        driver.current_url
        return True
    except:
        return False

if __name__=="__main__":
    main()