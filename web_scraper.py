from enum import auto
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from get_env import hold_creds
from send_email import send_day_pass
import os

driver =''
def init_WebDriver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    touch_screen = webdriver.TouchActions(driver)

def been_there_done_that():
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'day')))
    already_success_confirmation = True
    just_got_success = True
    
    look_for_weekday = driver.find_element_by_class_name('weekDay')
    look_for_day = driver.find_element_by_class_name('day')
    for each_file in os.listdir('./phone_screenshots'):
        os.remove("./phone_screenshots/"+each_file)
        print(each_file)
    for each_image in os.listdir('./watch_screenshots'):
        os.remove("./watch_screenshots/"+each_image)
    phone_filetopath ='./phone_screenshots/{}-{}.png'.format(look_for_weekday.text, look_for_day.text)
    watch_filetopath = './watch_screenshots/{}-{}.png'.format(look_for_weekday.text, look_for_day.text)

    if already_success_confirmation or just_got_success:
        print('Got Success')
        driver.execute_script("window.scrollTo(0, 250)") 
        phone_element = driver.find_element_by_class_name('day-pass')
        watch_element = driver.find_element_by_class_name('day-pass-qr-code')
        print("Phone screenshot successfully saved!") if phone_element.screenshot(phone_filetopath) else print("Issue with saving phone screenshot!")
        print("Watch screenshot successfully saved!") if watch_element.screenshot(watch_filetopath) else print("Issue with saving watch screenshot!")
        return phone_filetopath, watch_filetopath
    else: 
        print('ERROR: Webpage did not return a success')

#DUO 2FA 
def duo_or_not(need_fill = True):
    if need_fill:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'iframeparent')))
        
        driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))

        duo_find_element = driver.find_elements_by_tag_name('button')[0]
        duo_find_element.click()

def  go_thru_motion(two_factor_enabled = True):
    driver.get('https://trojancheck.usc.edu/login')
    #first page
    elem = driver.find_elements_by_css_selector('button')
    get_login_btn = [each_btn for each_btn in elem if "Log in with your USC NetID" in each_btn.text][0]
    get_login_btn.click()

    #wait for page wipe
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'password')))

    #login page
    l_usnm = driver.find_element_by_id('username')
    l_pswd = driver.find_element_by_id('password')
    signin_btn = driver.find_element_by_class_name('form-button')
    usnm, pswd = hold_creds()

    l_usnm.send_keys(usnm)
    l_pswd.send_keys(pswd)
    signin_btn.click()
    
    duo_or_not(need_fill=two_factor_enabled)
    
    #wait for page wipe
    wait = WebDriverWait(driver, 60)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-row')))

    #continue forward
    btn_elements = driver.find_elements_by_css_selector('button')
    get_continue_btn = [each_btn for each_btn in btn_elements if "Continue" in each_btn.text][0]
    get_continue_btn.click()
        
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'footer')))

    look_for = "Thank you for completing your daily wellness assessment" #in a p tag
    look_for_p = driver.find_elements_by_css_selector('p')
    try:
        success_confirmation = True if [each_p for each_p in look_for_p if look_for in each_p.text][0] else False 
    except: 
        success_confirmation = False
    if success_confirmation:
        return been_there_done_that()
    else: 
        #start assessment
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-begin-assessment')))
        btn_elements = driver.find_elements_by_css_selector('button')
        get_continue_btn = [each_btn for each_btn in btn_elements if "Begin wellness assessment" in each_btn.text][0]
        get_continue_btn.click()
        #start screening
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-button-base')))
        btn_elements = driver.find_elements_by_css_selector('button')
        get_continue_btn = [each_btn for each_btn in btn_elements if "Start screening" in each_btn.text][0]
        get_continue_btn.click()
        
        #first page
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-flat-button')))
        btn_elements = driver.find_elements_by_css_selector('button')
        get_NO_btn = [each_btn for each_btn in btn_elements if "No" in each_btn.text]
        [each_NO.click() for each_NO in get_NO_btn]
        get_NEXT_btn = [each_btn for each_btn in btn_elements if "Next" in each_btn.text][0]
        get_NEXT_btn.click()
        
        #second page
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-flat-button')))
        btn_elements = driver.find_elements_by_css_selector('button')
        get_NO_btn = [each_btn for each_btn in btn_elements if "No" in each_btn.text]
        [each_NO.click() for each_NO in get_NO_btn]
        get_NEXT_btn = [each_btn for each_btn in btn_elements if "Next" in each_btn.text][0]
        get_NEXT_btn.click()
        
        #attest page
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-checkbox-input')))
        input_elements = driver.find_elements_by_class_name('mat-checkbox-inner-container')
        # click checkbox
        [print(each_val.click()) for each_val in input_elements]
        submit_elements = driver.find_elements_by_css_selector('button')
        submit_btn = [each_btn for each_btn in submit_elements if "Submit" in each_btn.text][0]
        submit_btn.click()
                
        return been_there_done_that()
    

def auto_troy(two_FA_enabled=True, to_watch=True):        
    try:
        init_WebDriver()
        screenshot_filepaths = go_thru_motion(two_factor_enabled = True)
        driver.close()
        return send_day_pass(screenshot_filepaths, hold_creds()[0]+'@usc.edu', to_watch=to_watch) if screenshot_filepaths else (lambda: NameError('No filepath'))()
    except Exception as e:
        print(str(e))

# if __name__ == '__main__':
#     auto_troy(two_FA_enabled=True, to_watch=True)
      