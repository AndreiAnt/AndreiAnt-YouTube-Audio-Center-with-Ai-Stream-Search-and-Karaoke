from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.webdriver.common.keys import Keys

script_dir = os.path.dirname(os.path.realpath(__file__))

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=old")  # Uncomment to run headless
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def accept_cookies(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
            #EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"))
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Accept folosirea cookie-urilor și a altor date în scopurile descrise']"))
        )
        accept_button.click()
        time.sleep(0.5)
    except Exception as e:
        print("Accept button not found or not necessary.")

def read_search_query_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            search_query = file.read().strip()
            return search_query
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def perform_search(driver, search_query):
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='search']"))
        )
        search_box.clear()
        search_box.send_keys(search_query)
        
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='search-icon-legacy']"))
        )
        search_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error performing search: {e}")

def navigate_to_youtube(driver):
    driver.get('https://www.youtube.com')
    time.sleep(1)



def extract_video_info(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ytd-video-renderer"))
        )
        videos = driver.find_elements(By.XPATH, "//ytd-video-renderer")

        with open(os.path.join(script_dir, 'Info_Suggested_Videos.txt'), 'w', encoding='utf-8') as file:
            video_count = 1
            for video in videos:
                video_title = video.find_element(By.ID, "video-title").text
                # Skip videos that are marked as "Mix" or "Sponsored"
                if "Mix" in video_title or any("Sponsored" in d.text for d in video.find_elements(By.XPATH, ".//span[contains(text(), 'Sponsored')]")):
                    continue
                
                video_link = video.find_element(By.ID, "thumbnail").get_attribute('href')
                if "/shorts/" in video_link:
                    continue  # Skip saving this video link if it contains "/shorts/"
                if not video_link.startswith('https://'):
                    video_link = f"https://www.youtube.com{video_link}"
                video_views = video.find_element(By.CSS_SELECTOR, "div#metadata-line span.inline-metadata-item").text
                
                file.write(f"Video{video_count}:\n")
                file.write(f"Video_Link: {video_link}\n")
                file.write(f"Video_Title: {video_title}\n")
                file.write(f"Video_Views: {video_views}\n\n")
                video_count += 1

        print("Video information extracted and saved.")
    except Exception as e:
        print(f"Failed to extract video information: {e}")




def empty_info_suggested_videos():
    with open(os.path.join(script_dir, 'Info_Suggested_Videos.txt'), 'w', encoding = 'utf-8') as file:
        file.write("")


def scroll_page(driver):
    # You might need to adjust the range depending on how much data you need to load
    for _ in range(2):  # Scroll down one times
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Wait a second to allow the page to load


def main():
    driver = initialize_driver()
    empty_info_suggested_videos()
    navigate_to_youtube(driver)
    
    accept_cookies(driver)
    file_path = os.path.join(script_dir, 'Final_Search.txt')
    search_query = read_search_query_from_file(file_path)
    
    if search_query:
        perform_search(driver, search_query)
        time.sleep(2)  # Allow time for search results to load, might need adjustment based on connection speed
        scroll_page(driver)# Allow time for the page to load more videos, might need adjustment based on connection speed
        extract_video_info(driver)  # Call the new method to extract and save video info

    else:
        print("No search query found.")

    driver.quit()

if __name__ == "__main__":
    main()

