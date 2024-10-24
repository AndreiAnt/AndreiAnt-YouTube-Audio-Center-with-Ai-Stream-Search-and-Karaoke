from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

#empty Video_Duration.txt
with open("./Youtube_Scrapers/Suggested_Videos/Video_Duration.txt", "w", encoding='utf-8') as file:
    pass

# Path to the ChromeDriver (update the path according to your setup)
chrome_options = Options()
chrome_options.add_argument("--headless=old")  # Uncomment to run headless
driver = webdriver.Chrome(options=chrome_options)

# Open the file with 'a' mode (append) to ensure we keep writing to the same file
with open("./Youtube_Scrapers/Suggested_Videos/Video_Duration.txt", "a", buffering=1) as output_file:
    # Read "Info_Suggested_Videos.txt"
    with open("./Youtube_Scrapers/Suggested_Videos/Info_Suggested_Videos.txt", "r") as file:
        lines = file.readlines()

    # Loop through the lines of the text file
    for line in lines:
        if line.startswith("Video_Link:"):
            # Reload the page to start fresh for each video link
            driver.get('https://yt1s.com.co/')
            
            # Extract the YouTube link
            video_link = line.split("Video_Link:")[1].strip()

            # Find the search box, enter the video link
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.index-module--search--fb2ee'))
            )
            search_box.clear()
            search_box.send_keys(video_link)

            # Wait for the page to load the duration (adjust time as needed)
            time.sleep(3.5)  # Give the page time to display the duration

            # Find the duration element and extract the text
            try:
                # This XPath will target the <p> element containing the duration
                duration_p = driver.find_element(By.XPATH, "//p[contains(text(),'Duration')]").text
                # Remove the "Duration: " prefix to get only the time
                duration = duration_p.replace("Duration: ", "").strip()
            except:
                duration = "Not Found"

            # Write only the duration into the output file (no link or extra info) and flush
            output_file.write(f"{duration}\n")
            output_file.flush()  # Ensure it is written immediately

# Close the browser
driver.quit()
