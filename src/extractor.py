#!/usr/bin/python3
import os
import sys
import configparser
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from base_logger import log

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__))).parent.absolute()
DATA_DIR = rf'{BASE_DIR}\data'


class FiservExtractor:

    config = configparser.ConfigParser()
    config.read(rf'{BASE_DIR}/config.ini')

    username = str(config['FISERV']['user'])
    password = str(config['FISERV']['password'])
    URL = 'https://www.fiserv.com.ar/'

    def __init__(self, url: str=URL, number_of_files: int=5):
        try:
            self.url = url
            self.number_of_files = number_of_files + 1
            log.info(f'Initialize FiservExtractor with url: {self.url}')
        except Exception as e:
            log.error(f'Error initializing FiservExtractor.{e}')
            sys.exit(1)

    def extract_files(self, detach_exec: bool=False):
        """ Function that initialize a webdriver an interact with Fiserv, dowloading files using Selenium.

        Args:
            detach_exec (bool, optional): flag that allow executing the webdriver on screen (good for testing). 
            Defaults to False.
        """

        log.debug('Execution started')

        chrome_options = Options()
        chrome_options.add_experimental_option('detach', detach_exec)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        prefs = {
            'download.default_directory' : rf'{DATA_DIR}',
            'profile.default_content_setting_values.automatic_downloads': 1,
            'download.prompt_for_download': False,
            'safebrowsing_for_trusted_sources_enabled': False,
            'safebrowsing.enabled': False
            }
        chrome_options.add_experimental_option('prefs', prefs)

        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
            log.info('Webdriver initialized successfully')
            driver.get(url=self.url)
            log.info(f'Get {self.url} successfully')
        except Exception as e:
            log.error(f'Error initializing the webdriver or getting the url.\n{e}')
            sys.exit(1)

        driver.maximize_window()

        time.sleep(10)

        # Close popup
        try:
            driver.execute_script(
                "arguments[0].click();", 
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH, 
                            '//div[@class="modal-header"]//button//span'
                        )
                )))
            log.info('Popup closed')
        except Exception as e:
            log.error(f'Error closing popup: {e}')

        time.sleep(20)

        # Login
        try:
            log.info('Trying to login')
            driver.find_element(By.ID, 'ID').send_keys(self.username)
            driver.find_element(By.ID, 'PSW').send_keys(self.password)

            driver.execute_script(
                "arguments[0].click();", 
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH, 
                            '//div[@class="form"]//div[@class="form-group"]//button[@class="btn btn-default"]'
                        )
                )))
            # TODO: check if url changes to validate correctly.
            log.info('Login successfully')
        except Exception as e:
            log.error(f'Error trying to login: {e}')
            sys.exit(1)

        time.sleep(15)

        try:
            log.info('Entrying to movements')
            driver.execute_script(
                "arguments[0].click();", 
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH, 
                            '//li[@name="movements"]//button//span/span'
                        )
                )))
            time.sleep(20)
            log.info('Entrying to liquidacion electronica')
            driver.execute_script(
                "arguments[0].click();", 
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH, 
                            '//*[@id="tabMovimientos"]/md-tabs-wrapper/md-tabs-canvas/md-pagination-wrapper/md-tab-item[5]//span'
                        )
                )))
            log.info('Entry to movements successfully')
        except Exception as e:
            log.error(f'Error navigate on the site: {e}')
            sys.exit(1)

        time.sleep(20)

        for num in range(1, self.number_of_files):
            file_name = driver.find_element(
                By.XPATH, 
                f'//*[@id="componenteFiltroMovimiento"]/div[11]/div/div[1]/md-table-container/table/tbody/tr[{num}]/td[1]'
                ).text

            if self.check_if_exists(filename=file_name):
                log.info(f'{file_name} exists. Skip the download')
            else:
                try:
                    log.info(f'{file_name} doesnt exists. Download on "{DATA_DIR}"')
                    driver.execute_script(
                        "arguments[0].click();", 
                        WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH, 
                                    f'//*[@id="componenteFiltroMovimiento"]/div[11]/div/div[1]/md-table-container/table/tbody/tr[{num}]/td[5]/button'
                                )
                        )))
                except Exception as e:
                    log.error(f'Error trying to download the file {file_name} : {e}')

            time.sleep(10)

        driver.close()
        log.info('Closing webdriver')

        self.delete_unnecessary_files()

        log.debug('Execution finished')

    @staticmethod
    def check_if_exists(filename: str):
        """ Check if file exists. If exists, skip the download.
        
        Arguments:
            filename {str} -- filename to verify the existence

        Returns:
            bool -- True if file exists, else False
        """
        exists = [True for file in os.listdir(DATA_DIR) if file.startswith(filename)]
        return True if True in exists else False

    @staticmethod
    def check_local_files() -> list:
        """ Not implemented yet. Check files already downloaded in our DATA_DIR.

        Returns:
            list: files on DATA_DIR
        """
        files = os.listdir(DATA_DIR)
        return files

    @staticmethod
    def delete_unnecessary_files():
        """ Not implemented yet. Delete duplicated and files older than 31 days. """
        files = os.listdir(DATA_DIR)
        duplicated_common = 'some regex exp. with [(0-9)]'
        if duplicated_common in files:
            print(files)

FE = FiservExtractor()


if __name__ == "__main__":
    FE.extract_files()
