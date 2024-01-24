import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def delete_bookmarks(delete=0):
    service = Service(
        executable_path="./Chrome_Drivers/chromedriver-win64/chromedriver.exe"
    )

    options = Options()
    options.add_argument("user-data-dir=.\\AppData\\Local\\Google\\Chrome\\User Data")
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://twitter.com/i/bookmarks")

    count = 0

    while count < delete:
        time.sleep(1)
        wait = WebDriverWait(driver, 10)
        bookmark_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="removeBookmark"]')
            )
        )
        bookmark_button.click()
        count += 1
        time.sleep(1)

    print(f"Deleted {delete} tweets from bookmarks")

    # Click the bookmark button
    # bookmark_button.click()

    time.sleep(1)

    driver.close()


def main():
    delete_bookmarks(delete=10)


if __name__ == "__main__":
    main()
