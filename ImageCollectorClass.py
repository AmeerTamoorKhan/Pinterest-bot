from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import pandas as pd
import time
import os
import shutil
from random import randint
import urllib.request
import ssl
import glob
from PIL import Image
import streamlit as st

ssl._create_default_https_context = ssl._create_unverified_context


class ImageGrabber:
    count = 0
    format = None

    def __init__(self, search, total_images, filename=None, progress=None, score=None):
        self.search = search
        self.total_images = total_images
        self.filename = filename.lower()
        self.captions = []
        self.Images = []
        self.unique_imgs = set()
        self.flag = True
        #format = None
        self.progress = progress
        self.score = score

        self.df = pd.DataFrame(columns=['Image Name', 'Caption'])
        if os.path.isdir(self.filename):
            shutil.rmtree(self.filename)
            os.mkdir(self.filename)
        else:
            os.mkdir(self.filename)

        self.init_driver()
        self.login()
        self.search_bar()
        self.image_grab(progress)
        self.save_captions()
        self.resize_images()
        self.close()

    def init_driver(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path="Driver/chromedriver", options=self.options)
        self.pinterest= self.driver.get('https://www.pinterest.com/')

    def login(self):
        username = 'khanameerkhan1994@gmail.com'
        password = '92553734982'
        time.sleep(4)
        login_button = self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button').click()
        time.sleep(4)
        usename_field = self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(username)
        time.sleep(randint(1, 3))
        password_field = self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        enter_login = self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/form/div[5]/button').click()

    def search_bar(self):
        #time.sleep(5)
        search = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBoxContainer"]/div/div/div[2]/input')))
        search.send_keys([self.search, Keys.RETURN])
        #time.sleep(5)

    def image_grab(self, progress_bar=None):
        count = 0
        while self.flag:
            imgs = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="Yl- MIw Hb7"]//a')))
            #imgs = self.driver.find_elements_by_xpath('//div[@class="Yl- MIw Hb7"]//a')
            print(len(imgs))
            for i in range(len(imgs)):
                href = imgs[i].get_attribute('href')
                self.driver.execute_script(f'''window.open("{href}","_blank");''')
                self.driver.switch_to.window(self.driver.window_handles[1])
                try:
                    img = self.driver.find_element_by_xpath('//div[@class="MIw QLY Rym ojN p6V sLG zI7 iyn Hsu"]//img')
                    caption = self.driver.find_element_by_xpath('//h1[@class="lH1 dyH iFc ky3 pBj DrD IZT"]').text
                    if caption not in self.unique_imgs:
                        print(self.count)
                        self.unique_imgs.add(caption)
                        src = img.get_attribute('src')
                        self.format = src.split(".")[-1]
                        self.captions.append((str(self.search) + str(self.count) + "."+ str(self.format), caption))
                        urllib.request.urlretrieve(src, f"{self.filename}/{self.search}{str(self.count)}.{self.format}")
                        self.count += 1
                        count = count + 1 / float(self.total_images)
                        if count >= 1:
                            count = 1.0
                        self.progress.progress(count)
                        #self.score.text(self.count)
                        #progress_bar['value'] += 100/self.total_images
                        #progress_bar.update()
                except (StaleElementReferenceException, NoSuchElementException):
                    pass

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                #time.sleep(1)

                if self.count == self.total_images:
                    self.flag = False
                    break

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def save_captions(self):
        if os.path.isdir(self.filename) and self.captions:
            self.df['Image Name'] = [x[0] for x in self.captions]
            self.df['Caption'] = [x[1] for x in self.captions]
            self.df.to_csv(f'{self.filename}'+'/'+f'{self.filename}.csv', index=False)

    def resize_images(self):
        for img in glob.glob(f'{self.filename}/*.{self.format}'):
            image = Image.open(img)
            image.thumbnail((100, 100))
            image.save(img)

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    pass