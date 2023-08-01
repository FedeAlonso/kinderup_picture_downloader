from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
asd = driver.get("https://padres.kinderup.es/")

screenshot_filename = f"_output/{datetime.utcnow().strftime('%Y%m%d%H%M%S.%f')[:-3]}-screenshot.png"

driver.save_screenshot(screenshot_filename)
