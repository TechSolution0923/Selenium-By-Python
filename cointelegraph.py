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
# configure chrome browser to not load images and javascript
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://cointelegraph.com/tags/bitcoin")
# wait for page to load
element = WebDriverWait(driver=driver, timeout=50).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=tag-page__rows]'))
)

sel = Selector(text=driver.page_source)
parsed = []
for item in sel.xpath("//div[contains(@class='tag-page__posts-col')] / div[contains(@class='posts-listing')] / ul[contains(@class='posts-listing__list')] / li[contains(@class='posts-listing__item')]"):
    parsed.append({
        'url' : item.css('div.post-card-inline__content div.post-card-inline__header a::attr(href)').get(),
        'title' : item.css('div.post-card-inline__content div.post-card-inline__header a span::text').get(),
        'content' : item.css('div.post-card-inline__content p.post-card-inline__text::text').get()
    })

fields = ['title', 'content', 'url']
with open('result.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(parsed)