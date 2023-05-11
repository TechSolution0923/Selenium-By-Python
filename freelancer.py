from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

# configure webdriver
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen
# configure chrome browser to not load images and javascript
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
driver.get("https://www.freelancer.com/login")
# wait for page to load
element = WebDriverWait(driver=driver, timeout=5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
)

email_box = driver.find_element(By.ID, 'emailOrUsernameInput')
email_box.send_keys('cm3406443@gmail.com')

pass_box = driver.find_element(By.ID, 'passwordInput')
pass_box.send_keys('welcome2023')
# either press the enter key
# search_box.send_keys(Keys.ENTER)
# or click search button
login_button = driver.find_element(By.CLASS_NAME, 'ButtonElement ng-star-inserted')
login_button.click()

time.sleep(5)

print(driver.page_source)
# sel = Selector(text=driver.page_source)
# parsed = []
# for item in sel.xpath("//div[contains(@id,'leftmenuinnerinner')]/a"):
#     parsed.append({
#         'name': item.css('::text').get(),
#         'link': item.css('::attr(href)').get()
#         # 'author': item.css('.author::text').get()
#         # 'url': item.css('.tw-link::attr(href)').get(),
#         # 'username': item.css('.tw-link::text').get(),
#         # 'tags': item.css('.tw-tag ::text').getall(),
#         # 'viewers': ''.join(item.css('.tw-media-card-stat::text').re(r'(\d+)')),
#     })
# # print(parsed)
# fields = ['name', 'link']
# with open('result.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fields)
#     writer.writeheader()