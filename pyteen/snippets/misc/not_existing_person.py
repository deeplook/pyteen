# conda install -c conda-forge geckodriver  # (or some other for Selenium)

from hashlib import md5
from random import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def fetch(webdriver_path: str = "geckodriver") -> str:
    """Download an image from thispersondoesnotexist.com and save with its MD5 hash as name."""
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=webdriver_path)
    driver.get("https://thispersondoesnotexist.com")
    sleep(random())
    img_el = driver.find_element_by_xpath('//*[@id="face"]')
    buff = img_el.screenshot_as_png
    digest = md5(buff).hexdigest()
    path = f"{digest}.png"
    open(path, "wb").write(buff)
    return path
