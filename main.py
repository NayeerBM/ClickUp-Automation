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
location={"-":1,"Home":2,"Office":3,"On Site":4,"Leave":5}
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
        
        driver.close()
        driver.quit()
    
    except Exception as e:
        display_Error(e)        
    
    

    
#Logs into ClickUp
def login():
    #navigate to ClickUp
    driver.get("https://app.clickup.com/login")
    wait.until(EC.presence_of_element_located((By.ID,"login-email-input"))).send_keys(config_data["email"])
    wait.until(EC.presence_of_element_located((By.ID,"login-password-input"))).send_keys(config_data["password"])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"login-page-new__main-form-button"))).click()

def checkOut():
    try:
        goToName()
        time.sleep(3)
        #click on "Show empty fields"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class^='cu-task-custom-fields__collapsed-text']"))).click()
        #click on Check-Out
        wait.until(EC.presence_of_all_elements_located((By.XPATH,"//input[@containerclass='popover_white'][@type='checkbox']")))[1].click()

    except Exception as e:
        print(e)
        display_Error(e)
#def checkOut(driver,currentDate):
def checkIn():
    try:
        
        goToName()
        time.sleep(3)
        #click on "Show empty fields"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class^='cu-task-custom-fields__collapsed-text']"))).click()
        #clicks on Check-In Column
        wait.until(EC.presence_of_all_elements_located((By.XPATH,"//input[@containerclass='popover_white'][@type='checkbox']")))[0].click()
        time.sleep(5)
        #clicks on Health Level Column - Skip first as it's causing too many issues
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,f"/html/body/app-root/cu-task-keeper/cu-manager-view-task/div[2]/div/div/div[2]/div[3]/main/cu-task-custom-fields/div/section/div[5]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/div/cu-emoji-custom-field-value/div/div[{config_data['health level']}]"))).click()
        except:
            pass
        #Selects Location
        selectedOption=location[config_data['location']]
        print(config_data['location'],selectedOption)
        driver.find_element(By.XPATH,"/html/body/app-root/cu-task-keeper/cu-manager-view-task/div[2]/div/div/div[2]/div[3]/main/cu-task-custom-fields/div/section/div[7]/div[2]/cu-custom-field/cu-edit-task-custom-field-value/div/div").click()
        wait.until(EC.presence_of_element_located((By.XPATH,f"/html/body/div/div[2]/div/div/div[2]/cu-select-option[{selectedOption}]/div/div"))).click()
        for task in config_data["tasks"]:
            #Fill up tasks
            wait.until(EC.presence_of_element_located((By.XPATH,f"//input[@class='cu-task-row-new__input']"))).send_keys(task)
            wait.until(EC.presence_of_element_located((By.XPATH,f"//input[@class='cu-task-row-new__input']"))).send_keys(Keys.ENTER)
    except Exception as e:
        print(e)
        display_Error(e)

def goToName():
    currentDate=date.today().strftime("%d.%m.%Y")
    # driver.get("https://app.clickup.com/3635363/v/l/3ey53-50708/370328")
    time.sleep(3)  
    wait.until(EC.presence_of_element_located((By.XPATH,f"//a[@href='https://app.clickup.com/3635363/v/l/3ey53-50708/3703285']")))
    wait.until(EC.presence_of_element_located((By.XPATH,f"//div[@data-test='nav-section__{currentDate}']"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH,f"/html/body/app-root/cu-app-shell/cu-manager/div[1]/div/div[2]/main/cu-dashboard/cu-left-sidebar/div/cu-sidebar-toggle/button"))).click()
    name=config_data["name"]
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/cu-app-shell/cu-manager/div[1]/div/div[2]/main/cu-dashboard/div/div/cu-dashboard-table/div/div[2]/cu-list-group/div"))).click()
    scrollDownElement=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/cu-app-shell/cu-manager/div[1]/div/div[2]/main/cu-dashboard/div")))
    ActionChains(driver).move_to_element(scrollDownElement).send_keys(Keys.PAGE_DOWN).perform()
    
    elem_not_found = True
    while elem_not_found:
        try:
            # wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/cu-app-shell/cu-manager/div[1]/div/div[2]/main/cu-dashboard/div/div/cu-dashboard-table/div/div[2]/cu-list-group/div"))).click()
            
            ActionChains(driver).move_to_element(scrollDownElement).send_keys(Keys.PAGE_DOWN).perform()
            wait.until( EC.presence_of_element_located((By.XPATH, f"//span[@data-test='task-row-main__{name}']"))).click()
            #Once element is loaded do whatever you want with it 
            elem_not_found = False
        except Exception as e:
            y=10
def decryptPassword(password):
    NotImplemented

def encryptPassword(password):
    NotImplemented

def display_Error(error_message):
    print(error_message)
    if(isBrowserAlive()==True):
        driver.close()
        driver.quit()
    exit(0)
    
def isBrowserAlive():
    try:
        driver.current_url
        return True
    except:
        return False

if __name__=="__main__":
    main()