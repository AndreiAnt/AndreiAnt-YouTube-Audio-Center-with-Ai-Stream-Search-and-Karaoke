from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#empty Thumbnail_Links.txt
with open("./Youtube_Scrapers/Suggested_Videos/Thumbnail_Links.txt", "w", encoding='utf-8') as file:
    pass

# Function to initialize the WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=old")  # Run headless to speed up
    return webdriver.Chrome(options=chrome_options)

def process_video(driver, video_link):
    driver.get("https://www.softr.io/tools/download-youtube-thumbnail")
    time.sleep(0.5)  # Wait for the page to load
    input_element = driver.find_element(By.ID, "videoLinkInput")
    input_element.clear()
    input_element.send_keys(video_link)
    download_button = driver.find_element(By.ID, "downloadButton")
    download_button.click()
    time.sleep(0.5)  # Wait time for redirect to complete or new page to load
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
    thumbnail_url = driver.execute_script("return window.location.href;")
    if len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return thumbnail_url

# Open and read input file
with open("./Youtube_Scrapers/Suggested_Videos/Info_Suggested_Videos.txt", "r", encoding='utf-8') as file:
    video_links = [line.strip().split("Video_Link: ")[1] for line in file if "Video_Link" in line]

# Process each video link and write to file
driver = init_driver()
for video_link in video_links:
    thumbnail_link = process_video(driver, video_link)
    with open("./Youtube_Scrapers/Suggested_Videos/Thumbnail_Links.txt", "a", encoding='utf-8') as output_file:
        output_file.write(f"{thumbnail_link}\n")
        output_file.flush()

driver.quit()
print("Thumbnail links extracted successfully.")
