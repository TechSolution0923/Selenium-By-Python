from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

def main():
    # configure webdriver
    # configure chrome browser to not load images and javascript
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.openrice.com/en/hongkong/restaurants")
    # wait for page to load
    element = WebDriverWait(driver=driver, timeout=15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'section[class=sr1-center-content-wrapper]'))
    )

    items = []
    results = []
    lastNumber = 1

    print("**********1**********")

    for i in range(lastNumber):
        items = items.concat(extractMainInfo(driver))
        if i != lastNumber - 1:
            aTags = driver.find_elements(By.CLASS_NAME, 'div.js-pagination a')
            nextBtn = driver.find_element(By.CLASS_NAME, 'div.js-pagination a:nth-child('+Len(aTags)+')')
            nextBtn.click()
            time.sleep(10)

    for item in items:
        driver.get(item.openrice_link)
        time.sleep(10)
        phone = getPhone(driver)
        
        insertData = {
            name: item.name,
            address: item.address,
            openrice_link: item.openrice_link,
            phone: phone
        }
        results.append(insertData)
        
    print(results)

def extractMainInfo(driver):
    sel = Selector(text = driver.page_source)

    data = []
    for item in sel.xpath("//div[contains(@id = 'or-route-poi-list-main')] / ul / li[contains(@class = 'sr1-listing-content-cell')]"):
        data.append({
            'name' : item.css('h2.title-name a::text').get(),
            'address' : item.css('div.details-wrapper div.central-content-container div.icon-info-wrapper div.address span::text').get(),
            'openrice_link' : item.css('h2.title-name a::attr(href)').get()
        })
    return data

def getPhone(driver):
    element = WebDriverWait(driver=driver, timeout=50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=left-col]'))
    )
    phone = ''
    try:
        phone = driver.find_element(By.CLASS_NAME, 'div.or-section div.left-middle-col-section section.telephone-section div.content').get_attribute('text')
    except:
        print("Error: get phone number")
        
    return phone


def saveCSV(results):
    fields = ['name', 'link']
    with open('result.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

if __name__ == '__main__':
    main()