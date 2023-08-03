import os
import time
import logging
import requests
from logging.handlers import RotatingFileHandler
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


output_path = "_output"
url = "https://padres.kinderup.es/"


# Create _output path
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Configure Logging
logging.basicConfig(
    handlers=[RotatingFileHandler(
                os.path.join(output_path, "picture_downloader.log"), 
                maxBytes=20000000, 
                backupCount=1000)],
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Download elements from KinderUp's Pictures view 
    """

    # Configure Chrome driver
    options = Options()
    prefs = {"download.default_directory": output_path}
    options.add_experimental_option("prefs",prefs)
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    
    # Get into entrypoint URL
    driver.get(url)
    logger.info('Navigating to URL')

    # Log into KinderUP
    username = driver.find_element(By.ID, "user")
    password = driver.find_element(By.ID, "pass")
    username.send_keys(os.environ['KINDERUP_USER'])
    password.send_keys(os.environ['KINDERUP_PASS'])
    driver.find_element(By.CLASS_NAME, "login-button").click()

    # Get into Pictures view
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "flaticon-picture"))).click()
    logger.info('Navigating to Pictures view')

    # Load all thumbnails (Scrolling down and pressing the "+" button)
    logger.info('Saving all downlodeable elements')
    html = driver.find_element(By.TAG_NAME, 'html')
    while True:
        html.send_keys(Keys.END)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[alt="Mostrar mas fotos"]'))).click()
            
        except Exception as e:
            # Sometimes it takes a little bit of time to make the "+" button really clickable
            if isinstance(e, ElementClickInterceptedException):
                time.sleep(1)
            else:
                break
    download_buttons = driver.find_elements(By.CSS_SELECTOR, '[alt="Descargar"]')

    videos_url = []

    # Download all pictures
    # Doing it reverse in order to have the older pictures with the lower index
    for i,v in enumerate(reversed(download_buttons)):
        action = ActionChains(driver)
        action.move_to_element(v).click().perform()
        logger.info(f'Downloading element {i}')

        # A video gets opened instead of get downloaded
        if driver.current_url != url:
            video_url = driver.current_url
            driver.execute_script("window.history.go(-1)")
            videos_url.append([i, video_url])
            logger.info(f'Element {i} is a video. URL: {video_url}')
            time.sleep(3)


    # Download videos
    for video in videos_url:
        index = video[0]
        video_url = video[1]
        video_name = f"{index}-{video_url.split('.mp4')[0].split('/')[-1]}.mp4"
        video_path = os.path.join(output_path, video_name)
        r = requests.get(video_url)
        with open(video_path, 'wb') as f:
            f.write(r.content)
        logging.info(f'Video {index} Downloaded. Saved as: {video_path}')

    # screenshot_filename = f"_output/{datetime.utcnow().strftime('%Y%m%d%H%M%S.%f')[:-3]}-screenshot.png"

    # driver.save_screenshot(screenshot_filename)


if __name__ == "__main__":
    main()