import os
import time
import logging
import requests
import json
from logging.handlers import RotatingFileHandler
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


# Load config 
CONFIG_FILE = "resources/config.json"
CONFIG = None
with open(CONFIG_FILE) as f:
        CONFIG = json.loads(f.read())

# Create _output path
output_path = os.path.join(os.getcwd(), CONFIG.get("output_path"))
if not os.path.exists(output_path):
    os.makedirs(output_path)
# Create an specific folder for this execution
execution_output_folder = os.path.join(output_path, datetime.utcnow().strftime('%Y%m%d%H%M%S')) 
os.makedirs(execution_output_folder)

# Configure Logging
logging.basicConfig(
    handlers=[RotatingFileHandler(
                os.path.join(execution_output_folder, "kinderup_picture_downloader.log"), 
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

    logger.info(f'Start. Output folder: {execution_output_folder}')

    start_time = time.time()

    # selenium-wire
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": execution_output_folder}
    options.add_experimental_option("prefs",prefs)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options = options)

    # Filter just the requests with multimedia content, in the Pictures view
    driver.scopes = ['.*kinderServices/api/v01/schools/.*/classrooms/.*/kids/.*/pictures']
    
    # Get into entrypoint URL
    url = CONFIG.get("kinderup").get("login_url")
    driver.get(url)
    logger.info(f'Navigating to URL {url}')

    # Log into KinderUP
    app_elems = CONFIG.get("kinderup").get("view_elements")
    username = driver.find_element(By.ID, app_elems.get("login_user"))
    password = driver.find_element(By.ID, app_elems.get("login_pass"))
    username.send_keys(os.environ['KINDERUP_USER'])
    password.send_keys(os.environ['KINDERUP_PASS'])
    driver.find_element(By.CLASS_NAME, app_elems.get("login_button")).click()
    logger.info('Login performed')

    # Get into Pictures view
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, app_elems.get("pictures_button")))).click()
    logger.info('Navigating to Pictures view')

    # Load all thumbnails (Scrolling down and pressing the "+" button)
    logger.info('Saving all download buttons')
    html = driver.find_element(By.TAG_NAME, 'html')
    multimedia_elems = []
    while True:
        html.send_keys(Keys.END)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, app_elems.get("more_pictures_button")))).click()
            
        except Exception as e:
            # Sometimes it takes a little bit of time to make the "+" button really clickable
            if isinstance(e, ElementClickInterceptedException):
                time.sleep(1)
            else:
                break
            
    for request in driver.requests:
        headers = {
            "Authorization": request.headers['Authorization'],
            "Content-Type": "application/json"
            }
        req = protected_get(request.url, headers=headers)
        for multimedia_elem in req.json():
            multimedia_elems.append(multimedia_elem)

    # Download all pictures and videos
    # Doing it reverse in order to have the older ones with the lower index
    for i,v in enumerate(reversed(multimedia_elems)):
        elem_url = v.get('originalPicture')
        elem_name = f"{i}-{v.get('name')}"
        elem_path = os.path.join(execution_output_folder, elem_name)
        r = protected_get(elem_url)
        with open(elem_path, 'wb') as f:
            f.write(r.content)
        logging.info(f"{v.get('mediaType')} {i} Downloaded. Saved as: {elem_path}")

    logging.info(f'Download Finished. {i} Elements downloaded. Taken {int(time.time() - start_time)} seconds')


def protected_get(url, headers=None):
    """
    As we are making a lot of requests, sometimes we need to wait sometime before continuing
    """
    try:
        req = requests.get(url, headers=headers)
        logger.info(f'REQUEST URL:{url}   HEADERS:{headers}')        
    except requests.ConnectionError:
        time.sleep(1)
        req = requests.get(url, headers=headers)
        logger.info(f'Retrying - REQUEST URL:{url}   HEADERS:{headers}')
    logger.info(f'REQUEST RESPONSE STATUS CODE: {req.status_code} URL:{req.url}')
    return req

if __name__ == "__main__":
    main()