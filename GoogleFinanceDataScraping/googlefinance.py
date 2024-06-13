import selenium
from selenium import webdriver
import time

from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("start")

options = Options()  #webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)
driver.get('https://www.google.com/finance/quote/AEFES:IST?hl=tr')
driver.maximize_window()

print(driver.title)

thisDict = {

}

# date : <p jsname="LlMULe" class="hSGhwc-ZlY4af">31 May 2024 18:10</p>
# price : <p jsname="BYCTfd" class="hSGhwc-SeJRAd" style="">TRY ₺199,00</p>


priceOld = "123"

for i in range(1, 100):
    try:
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p[jsname='BYCTfd'].hSGhwc-SeJRAd"))
        )
        dateAndTime = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p[jsname='LlMULe'].hSGhwc-ZlY4af"))
        )

        if price.text != "" and price.text != priceOld and dateAndTime.text != "":
            dateTime = dateAndTime.text
            date = dateTime[0:12]
            time = dateTime[11:]
            print(date + " " + time + ". price = " + price.text + "    and old price = " + priceOld)

            thisDict[time] = price.text  # Corrected to store the price text

            priceOld = price.text

    except StaleElementReferenceException:
        print("StaleElementReferenceException caught. Retrying...")
        continue
    except TimeoutException:
        print("Timed out waiting for element to load")
        break


#print(thisDict)
print("\n")
print(sorted(thisDict.items()))

driver.quit()
