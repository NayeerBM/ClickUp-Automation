import sys
from datetime import date,datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def main():
    
    driver = webdriver.Firefox()
    #navigate to ClickUp
    wait=WebDriverWait(driver,10)
    driver.get("https://app.clickup.com/login")

    #1. fill-up input field
    email_address=""
    password=""
    wait.until(EC.presence_of_element_located((By.Id,"login-email-input")))
    driver.find_element(By.Id,"login-email-input").send_keys(email_address)
    driver.find_element(By.Id,"login-password-input").send_keys(password)
    driver.find_element(By.Class,"login-page-new__main-form-button").click()
    
    # 2. Navigate to "Staff Daily Task" folder and find current month's folder
    driver.find_element(By.Class,"cu2-project-list-bar-item__avatar ng-tns-c679-22 ng-star-inserted").click()
    currentDate=date.today()
    currentMonth=currentDate.strftime("%B")
    currentYear=currentDate.strftime("%Y")
    monthTarget=f"{currentMonth} {currentYear}"
    
    
    
if __name__=="__main__":
    main()
    

def decryptPassword(password):
    
    return password