from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


a = 0
b = 0
c = 0 
content = ""


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=old")  # Ensure GUI is off
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def navigate_to_youtube(driver):
    driver.get('https://www.youtube.com')
    time.sleep(1)  # Wait for the page to load

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Accept folosirea cookie-urilor și a altor date în scopurile descrise']"))
            #EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"))
        )
        accept_button.click()
        time.sleep(0.5)
    except Exception as e:
        print("Nu a fost gasit butonul Accept All sau nu a fost necesar.")

def search_youtube(driver, search_query):
    search_box = driver.find_element(By.NAME, "search_query")
    first_part = search_query[:-1]  # All characters except the last
    last_char = search_query[-1]    # The last character
    search_box.send_keys(first_part)
    time.sleep(0.3)  # Natural typing pause
    search_box.send_keys(last_char)

def collect_suggestions(driver):
    try:
        suggestions = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//li[@role='presentation']"))
        )
        with open("./Youtube_Scrapers/Search_Suggestions/Sugestii.txt", "w") as file:
            for suggestion in suggestions:
                full_suggestion = suggestion.text.replace("\n", "").strip()  # Replace line breaks with spaces
                if full_suggestion:
                    file.write(full_suggestion + "\n")
                    print(full_suggestion)
    except Exception as e:
        print("Nu au fost gasite sugestii.", e)

def wait_for_completion():
    global a
    if True:
        with open("./Youtube_Scrapers/Search_Suggestions/Gata.txt", "r") as file:
            if 'gata' in file.read():
                a = 1


def copy_searchtxt():
    global content
    with open("./Youtube_Scrapers/Search_Suggestions/Search.txt", "r") as file:
        content=file.read()
        print("\n\n")
        print("content = ", content)


def check_if_content_changed():
    global b, content
    with open("./Youtube_Scrapers/Search_Suggestions/Search.txt", "r") as file:
        if content!=file.read():
            b = 1
            time.sleep(2)
        else:
            b = 0

def refresh_searchbar(driver):
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.clear()  # Clear the text from the search box

def clear_searchtxt():
    with open("./Youtube_Scrapers/Search_Suggestions/Search.txt", "w") as file:
        file.write("")

def clear_sugestii():
    with open("./Youtube_Scrapers/Search_Suggestions/Sugestii.txt", "w") as file:
        file.write("")

def clear_gata():
    with open("./Youtube_Scrapers/Search_Suggestions/Gata.txt", "w") as file:
        file.write("")

def clear_all():    
    clear_searchtxt()
    clear_sugestii()
    clear_gata()

def check_if_searchtxt_is_not_empty():  
    with open("./Youtube_Scrapers/Search_Suggestions/Search.txt", "r") as file:
        if file.read() == "":
            return False
        else:
            return True

def main():



    global a, b, c
    driver = initialize_driver()
    clear_all()
    navigate_to_youtube(driver)
    accept_cookies(driver)

    while True:

        if c == 0:
            print("Start!\n")
            c = 1

        wait_for_completion()
        if a == 1:
            break

        if b == 1:
            if check_if_searchtxt_is_not_empty():
                with open("./Youtube_Scrapers/Search_Suggestions/Search.txt", "r") as file:
                    search_query = file.read().strip()

                search_youtube(driver, search_query)
                print("\n\n")
                print("Cautare: ", search_query)
                collect_suggestions(driver)
                print("\n\n")
                print("Sugestiile au fost salvate in fisierul Sugestii.txt")
                copy_searchtxt()

            else:
                b == 0
            
            

        check_if_content_changed()
        refresh_searchbar(driver)
        
    
    driver.quit()


    

if __name__ == "__main__":
    main()
