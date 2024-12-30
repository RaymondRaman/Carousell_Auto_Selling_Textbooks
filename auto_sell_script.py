"""
Author: Raymond Li
Date: 2024-12-28
Description: This script is used to automatically sell textbooks on Carousell.
To use this script, you need to fill in the required information in the initialization of the Carousell class.
1. The path to save the cookies (Please use EditThisCookie extension to export the cookies and save them in a text file)
2. The path to the Excel file containing the details of the textbooks to sell

Remark:
Please make sure the photo folder name is the same with title in excel.
"""

# import necessary libraries
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import glob
import json
import sys


class Carousell:
    def __init__(self):
        self.DIR = os.getcwd()
        with open(f'{self.DIR}/config.json', 'r') as config_file:
            config = json.load(config_file)

        options = webdriver.ChromeOptions()
        options.page_load_strategy = config['chrome_options']['page_load_strategy']
        for argument in config['chrome_options']['arguments']:
            options.add_argument(argument)

        self.driver = webdriver.Chrome(options=options)
        self.xpaths = config['xpaths']
        self.wait = WebDriverWait(self.driver, 30)
        self.category = config['category']
        self.textbooks = config['textbooks']

    def upload_photos(self, file_paths):
        upload_photo_button = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, self.xpaths['upload_photo_button'])))
        upload_photo_button.send_keys('\n'.join(file_paths))

    def select_category(self):
        # Click the category button
        category = self.driver.find_element(
            By.XPATH,
            self.xpaths['category']
        )
        category.click()

        # Fill in the title
        category_input = self.driver.find_element(
            By.XPATH,
            self.xpaths['category_input']
        )
        category_input.send_keys(self.category)

        # Click the category_select button
        # category_select_path = self.xpaths['category_select'].replace(
        #     "placeholder", self.category)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['category_select']))
        )
        category_select = self.driver.find_element(
            By.XPATH,
            self.xpaths['category_select']
        )
        category_select.click()

    def select_condition(self, condition):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths[condition]))
        )

        target_condition = self.driver.find_element(
            By.XPATH,
            self.xpaths[condition]
        )
        target_condition.click()

    def fill_in_title(self, title):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['title_input']))
        )

        title_input = self.driver.find_element(
            By.XPATH,
            self.xpaths['title_input']
        )
        title_input.send_keys(title)

    def select_level(self):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.textbooks['level']))
        )

        level = self.driver.find_element(
            By.XPATH,
            self.textbooks['level']
        )
        level.click()

    def fill_in_description(self, description):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['description_input']))
        )

        description_input = self.driver.find_element(
            By.XPATH,
            self.xpaths['description_input']
        )
        description_input.send_keys(description)

    def fill_in_price(self, price):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['price_input']))
        )

        price_input = self.driver.find_element(
            By.XPATH,
            self.xpaths['price_input']
        )
        price_input.send_keys(price)

    def submit_post(self):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['submit_button']))
        )

        submit_button = self.driver.find_element(
            By.XPATH,
            self.xpaths['submit_button']
        )
        submit_button.click()

    def sell(self, title, condition, price, description, file_paths):
        carousell.driver.get('https://www.carousell.com.hk/sell')
        self.upload_photos(file_paths)

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['category']))
        )
        print(f"""******* Photos have been successfully uploaded *******\n""")
        self.select_category()

        self.select_condition(condition)

        self.fill_in_title(title)

        if self.category == 'Textbooks':
            self.select_level()

        self.fill_in_description(description)

        self.fill_in_price(price)

        self.submit_post()

        # wait for the post to be uploaded
        time.sleep(40)
        print(f"""******* Item has been successfully uploaded *******\n""")

    def login(self):
        # Open the coursell website
        self.driver.get('https://www.carousell.com.hk/')

        # Load cookies from a file
        with open(f'{carousell.DIR}/cookie.txt', 'r') as f:
            cookies = json.load(f)

        # Add each cookie to the browser
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                cookie['sameSite'] = "None"
            self.driver.add_cookie(cookie)

        # Refresh the page to apply the cookies
        self.driver.refresh()

    def get_photo_directory(self, title):
        photo_directory = (
            f'{self.DIR}/photos/'
            f'{title}'
        )
        file_paths = glob.glob(os.path.join(
            photo_directory, '**', '*.jpg'), recursive=True)

        if len(file_paths) == 0:
            print(
                "Please make sure the photo folder name is the same with title in excel.")
            sys.exit(1)

        return file_paths


if __name__ == '__main__':
    # Create a new instance of the Chrome driver
    carousell = Carousell()
    carousell.login()
    print(f"""******* Login Successful  *******\n""")

    # Load the excel file to get the item to sell
    df = pd.read_excel(os.path.join(carousell.DIR, 'items_to_sell.xlsx'))

    for index, row in df.iterrows():
        title, condition, price, description = row['Listing Title'], row[
            'Condition'], row['Price'], row['Description']

        # Sell the item
        print(f"""******* Selling the item *******\nTitle: {title}\nCondition: {
              condition}\nPrice: {price}\nDescription: {description}\n""")

        # Generate photo_directory and file_paths for each textbook
        file_paths = carousell.get_photo_directory(title)

        carousell.sell(title, condition, price, description, file_paths)

    # Close the browser
    carousell.driver.quit()
