from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import time

def channel_url():
    driver_path = "chromedriver"
    driver = webdriver.Chrome(service=Service(driver_path))
    # Channel url we want to scrape
    URL = "https://www.youtube.com/@MrBeast/videos"
    
    driver.get(URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Accept all"]'))
    )
    accept_button = driver.find_element(By.XPATH, '//button[@aria-label="Accept all"]')
    accept_button.click()

    time.sleep(6)

    while True:
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break

    channel_title = driver.find_element(By.XPATH, '//ytd-channel-name[@id="channel-name"]').text

    titles = driver.find_elements(By.ID, "video-title")
    titles = [title.text for title in titles]

    views = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]/span[1]')

    videos = []
    for title, view in zip(titles, views):
        video_dict = {
            "channel name": channel_title,
            "title": title,
            "views": view.text
        }
        videos.append(video_dict)

    fields = ["channel name", "title", "views"]

    with open("youtube_scraper.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(videos)

    driver.close()

channel_url() 
