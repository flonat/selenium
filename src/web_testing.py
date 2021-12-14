import os
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebTesting():

    def __init__(self, link: str):
        """[summary]

        Parameters
        ----------
        link : str
            [description]
        """
        service = Service('./utils/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(link)


    @staticmethod
    def get_web_element(driver, x_path: str) -> WebElement:
        """[summary]

        Parameters
        ----------
        driver : [type]
            [description]
        x_path : str
            [description]

        Returns
        -------
        WebElement
            [description]
        """
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, x_path))
        )

        return element


    @staticmethod
    def send_keys_and_click_enter_from_element(web_element, keys) -> None:
        """[summary]

        Parameters
        ----------
        web_element : [type]
            [description]
        keys : [type]
            [description]
        """
        web_element.send_keys(keys)
        web_element.send_keys(Keys.RETURN)


    def log_in(self, user: str, password: str) -> None:
        """[summary]
            Assumes that no two-factor authentication is running
        Parameters
        ----------
        user : str
            [description]
        password : str
            [description]
        """
        css_path_insedi_login = 'a.button.is-fullwidth.is-centered'
        button_insedi_login = self.driver.find_element(By.CSS_SELECTOR, css_path_insedi_login)
        button_insedi_login.click()

        x_path_imperial_login_user = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]'
        button_imperial_login_user = WebTesting.get_web_element(self.driver, x_path_imperial_login_user)
        WebTesting.send_keys_and_click_enter_from_element(button_imperial_login_user, user)

        x_path_imperial_login_password = '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'
        button_imperial_login_password = WebTesting.get_web_element(self.driver, x_path_imperial_login_password)
        WebTesting.send_keys_and_click_enter_from_element(button_imperial_login_password, password)

    
    @staticmethod
    def get_date_latest_news_feed_of_module(driver: webdriver) -> str:
        """[summary]

        Parameters
        ----------
        driver : webdriver
            [description]

        Returns
        -------
        str
            [description]
        """
        x_path_dat_algo_module = '//*[@id="main-content"]/section[3]/div/div/div/section/section[1]/div[2]/div/div/div[8]/div[2]/a'
        dat_algo_element = WebTesting.get_web_element(driver=driver, x_path=x_path_dat_algo_module)
        dat_algo_element.click()

        x_path_news_feed = '//*[@id="navMenu"]/ul/li[2]/div/a/span'
        news_feed_element = WebTesting.get_web_element(driver=driver, x_path=x_path_news_feed)
        news_feed_element.click()

        x_path_date_last_feed = '/html/body/div[1]/div/div[2]/section[2]/div/div/div[1]/div/section[1]/div/div/header/div/div[1]/article/div[2]/div/div[2]/span'
        last_posted_date_element = WebTesting.get_web_element(driver=driver, x_path=x_path_date_last_feed)
        last_posted_date_text = last_posted_date_element.text

        return last_posted_date_text


    @staticmethod
    def get_name_latest_news_feed_of_module(driver: webdriver) -> str:
        """[summary]

        Returns
        -------
        str
            [description]
        """
        x_path_name_last_feed = '//*[@id="oC6bsXSsG"]/header/div/div[1]/article/div[2]/div/div[1]/a[1]'
        last_posted_name_element = WebTesting.get_web_element(driver=driver, x_path=x_path_name_last_feed)
        last_posted_name_text = last_posted_name_element.text

        return last_posted_name_text
    

    def append_date_of_las_posted_feed_to_csv(self):
        """[summary]

        Parameters
        ----------
        last_feed_date : str
            [description]
        """
        session_date = datetime.today()
        session_date_str = session_date.strftime('%d %B %Y')

        last_feed_date_str = WebTesting.get_date_latest_news_feed_of_module(self.driver)
        last_feed_name_str = WebTesting.get_name_latest_news_feed_of_module(self.driver)

        df = pd.DataFrame({'date_selenium_session': [session_date_str], 
            'date_last_feed_posted': last_feed_date_str, 'name_last_feed_posted': last_feed_name_str})
        df.to_csv('src/report/report.csv', mode='a', sep=';', index=False, header=False)
        

    def close_session(self) -> None:
        """[summary]
        """
        self.driver.close()    


if __name__ == '__main__':

    user = os.environ.get('USER')
    pwd = os.environ.get('PASSWORD')
    link = os.environ.get('LINK')
    
    imperial = WebTesting(link=link)

    imperial.log_in(user=user, password=pwd)

    # Not ideal to add a timeout, but this gives enough time for the two factor authentication
    time.sleep(20)

    imperial.append_date_of_las_posted_feed_to_csv()

    imperial.close_session()