# 02/26/2025
# Boaz Bilgory
# Runtastic_export_data_request.py
# Export Date 02/26/2025 ~18:30

import sys
import os
import shutil
import zipfile
#
from .args_parser import get_args
from . import check_if_already_ran as ciar
#
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys

from selenium.common.exceptions import ElementClickInterceptedException

# import undetected_chromedriver as uc
# from undetected_chromedriver import ChromeOptions
# from undetected_chromedriver import By
# driver = uc.Chrome(
#     browser_executable_path="C:\\Users\\boazusa\\AppData\\Local\\Google\\Chrome\\User Data")


import time
from datetime import datetime
import random

""" NOT IN USE
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
"""

DOWNLOADS_PATH = r"C:\Users\USER\Downloads"
DESTINATION_FOLDER = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC"


def error_message(_txt):
    print(f"{'*' * 20} {_txt:^30} {'*' * 20}")


# Function to wait for download completion
def wait_for_downloads(download_path, timeout=200):
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = os.listdir(download_path)
        if any(file.endswith(".crdownload") for file in files):  # Chrome partial download
            time.sleep(1)  # Wait and check again
        else:
            time.sleep(5)
            print(f'Download complete!\nelapsed time: {"%.2f" % (time.time() - start_time)} seconds')
            files = [os.path.join(download_path, f) for f in os.listdir(download_path)]
            latest_file = max(files, key=os.path.getmtime)  # Get the latest modified file
            return latest_file
    print("Timeout waiting for download!")
    # exit(1)  # TODO...
    return None


def clean_directory(directory, exclude_folder):
    """Remove all files and folders except the specified folder."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Skip the folder we want to keep
        if item == exclude_folder:
            continue

        # Remove files
        if os.path.isfile(item_path):
            os.remove(item_path)
        # Remove directories
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


class Selenium_Runtastic:
    def __init__(self, _email, _password):
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/134.0.6998.88 Safari/537.36")
        chrome_options.add_argument("--user-data-dir=C:\\Users\\boazusa\\AppData\\Local\\Google\\Chrome\\User Data")
        # chrome_options.add_argument(r"--user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 1")
        chrome_options.add_argument("--profile-directory=Default")  # Use your actual Chrome profile
        # chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")  # Fix for Jenkins
        chrome_options.add_argument("--disable-dev-shm-usage")  # Fix shared memory issues
        # chrome_options.add_argument("--window-size=1920,1080")  # Optional: set window size

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        self.driver.get('https://www.runtastic.com/login')
        self.email = _email
        self.password = _password
        self.downloaded_file = ""
        self.zipped_file = ""
        self.extract_to_path = ""

    def select_location(self):
        try:
            time.sleep(random.uniform(3, 5))
            israel_radio_span = self.driver.find_element("xpath",
                                                         "//span[@class='gl-radio-input__label' and text()='Israel']")
            israel_radio_span.click()
            #
            time.sleep(random.uniform(2, 4))
            # (1) Click Using XPath (Recommended), Locate and click the "Continue" button
            continue_button = self.driver.find_element("xpath",
                                                       "//a[contains(@class, 'gl-cta--primary') "
                                                       "and span[text()='Continue']]")
            #
            # (2) Click Using CSS Selector
            # continue_button = self.driver.find_element("css selector", "a.gl-cta--primary")
            #
            # (3) Click Using Partial Text (XPath)
            # continue_button = self.driver.find_element("xpath", "//a[span[contains(text(), 'Continue')]]")
            #
            time.sleep(random.uniform(3, 5))
            continue_button.click()
            time.sleep(1)
        except Exception as e:
            error_message(f"Select location accept Error:")
            lines = str(e).split("\n")
            print("\n".join(lines[:4]))
            sys.exit(1)  # Exit with an error

    def accept_cookies(self):  # optional, not always asked
        try:
            time.sleep(random.uniform(3, 5))
            # Check if the button exists
            buttons = self.driver.find_elements(By.XPATH,
                                                "//button[contains(@class, 'cm-btn') and contains(@class, "
                                                "'black-bttn--adl')]")
            if buttons:  # If the list is not empty, the button exists
                time.sleep(random.uniform(1, 3))
                buttons[0].click()  # Click the first matching button
                print("Accept cookies button clicked!")
        except Exception as e:
            error_message(f"Accept cookies button wasn't asked:")
            lines = str(e).split("\n")
            print("\n".join(lines[:4]))

    def login(self):
        try:
            # Account & Data: // *[ @ id = "ember714"]
            email = self.driver.find_element(By.ID, "ember730")
            for c in self.email:
                time.sleep(random.uniform(0.1, 0.4))
                email.send_keys(c)
            email.send_keys(Keys.TAB)

            time.sleep(random.uniform(1, 3))
            password = self.driver.find_element(By.ID, "ember732")
            for c in self.password:
                time.sleep(random.uniform(0.1, 0.5))
                password.send_keys(c)
            time.sleep(random.uniform(1, 2))
            password.send_keys(Keys.RETURN)
            #
            time.sleep(random.uniform(2, 5))
            #
            # (1) Click Using Partial Text (XPath)
            # login_button = self.driver.find_element("xpath", "//button[contains(text(), 'Log in')]")
            #
            # (2) Click Using CSS Selector
            login_button = self.driver.find_element("css selector", "button.bttn.js-submit")
            #
            # (3) Click Using Partial Button Text (XPath)
            # login_button = self.driver.find_element("xpath",
            #                                         "//button[contains(@class, 'js-submit') "
            #                                         "and contains(text(), 'Log in')]")
            #
            time.sleep(random.uniform(3, 5))
            login_button.click()
            time.sleep(1)
        except Exception as e:
            error_message(f"Email and Password Error:")
            lines = str(e).split("\n")
            print("\n".join(lines[:4]))
            sys.exit(1)  # Exit with an error

    def accept_terms(self):  # optional, not always asked
        try:
            self.driver.find_element(By.XPATH,
                                     "//button[@class='bttn bttn-adl is-block js-submit text-uppercase']").click()
        except Exception as e:
            error_message(f"accept_term Error:")
            lines = str(e).split("\n")
            print("\n".join(lines[:4]))

    def export_data(self):
        time.sleep(random.uniform(5, 10))
        try:
            buttons = self.driver.find_elements(By.XPATH,
                                                "//a[contains(@class, 'bttn') and contains(text(), 'Export Data')]")
            if buttons:
                buttons[0].click()
            else:
                export_button = self.driver.find_element("css selector", "a.bttn-primary.black-bttn-solid--adl")
                export_button.click()
                time.sleep(random.uniform(2, 5))
            return 1
        # except ElementClickInterceptedException as e:
        #     print(f"Element click intercepted!\nExport is already in process.")
        except Exception as e:

            error_message(f"Export button Error:")
            lines = str(e).split("\n")
            print("\n".join(lines[:4]))
            return -1
        #
        # input("PRESS ENTER")

    def download_data(self, download_timeout=450):
        time.sleep(random.uniform(5, 10))
        try:
            # 1. Click Using XPath (Recommended)
            download_link = self.driver.find_element("xpath",
                                                     "//a[contains(@class, 'text-adihaus-din-bold')"
                                                     " and text()='Download Export']")
            # 2. Click Using CSS Selector
            # download_link = self.driver.find_element("css selector", "a.text-adihaus-din-bold")
            # 3. Click Using Partial Link Text
            # download_link = self.driver.find_element("partial link text", "Download Export")
            #
            download_link.click()
            time.sleep(random.uniform(10, 20))
            self.downloaded_file = wait_for_downloads(DOWNLOADS_PATH, download_timeout)
            return self.downloaded_file
        except Exception as e:
            error_message(f"download data Error:")
            lines = str(e).split("\n")
            print("\n".join(lines[:4]))
            return None
        #
        # input("PRESS ENTER")

    def move_downloaded_file(self):
        if not self.downloaded_file:                        # search in Downloads for manual downloaded activities
            downloads_path = r"C:\Users\USER\Downloads"
            for file in os.listdir(downloads_path):
                if "export-" in file and file.endswith(".zip"):
                    self.downloaded_file = downloads_path + r'\\' + file
        if self.downloaded_file:                            # get automated downloaded activities
            source_file = self.downloaded_file
            destination_folder = DESTINATION_FOLDER

            # Ensure destination folder exists
            os.makedirs(destination_folder, exist_ok=True)

            # Move the file
            destination_path = os.path.join(destination_folder, os.path.basename(source_file))
            shutil.move(source_file, destination_path)
            self.zipped_file = destination_path
            return self.zipped_file
        else:
            print("File wasn't moved; please verify file was downloaded")
            return None

    def unzip_file(self, extract_to=DESTINATION_FOLDER):  # '.' - current folder (scripts folder)
        try:
            """Create new folder and Extracts a zip file to the specified directory."""
            folder_name = os.path.basename(self.zipped_file).split(".")[0]
            self.extract_to_path = extract_to + r'\\' + folder_name
            if not os.path.exists(self.extract_to_path):
                os.makedirs(self.extract_to_path)
            #
            if self.zipped_file:
                with zipfile.ZipFile(self.zipped_file, 'r') as zip_ref:
                    zip_ref.extractall(self.extract_to_path)
                print(f"Extracted to: {os.path.abspath(self.extract_to_path)}")
                return 1
            else:
                os.remove(extract_to + r'\\' + folder_name)
                return 0
        except Exception as e:
            print(f"Error - unzip_file: {e}")
            return 0

    def remove_unused_files_and_folders(self):
        if os.path.exists(self.extract_to_path):
            clean_directory(self.extract_to_path, "Sport-sessions")
            inside_folders = ['Elevation-data', 'GPS-data', 'Heart-rate-data']
            os.remove(self.zipped_file)
            for folder in inside_folders:
                shutil.rmtree(self.extract_to_path + r"\\" + "Sport-sessions" + r"\\" + folder)

    def sport_sessions_folder(self):
        if self.extract_to_path != "":
            return self.extract_to_path + r"\\" + "Sport-sessions"
        return None

    def driver_quit(self):  # destructor
        self.driver.quit()

    def view_account(self):
        self.select_location()
        self.accept_cookies()
        # self.login()
        # self.accept_terms()
        # input("Press enter to quit")
        time.sleep(5)
        self.driver_quit()
        return None

    def export_cycle(self):
        try:
            if ciar.has_run_recently(ciar.EXPORT_LAST_RUN_FILE):
                self.driver_quit()
                with open(ciar.EXPORT_LAST_RUN_FILE, "r") as f:
                    export_on = f.read()
                    print(f"Export already started on "
                          f"{datetime.fromtimestamp(float(export_on)).strftime('%Y-%m-%d %H:%M:%S')}")
                return 0
            else:
                flag = 1
                self.select_location()
                self.accept_cookies()
                self.login()
                self.accept_terms()
                flag = self.export_data()  # export
                self.driver_quit()
                #
                if flag == 1:
                    ciar.update_last_run(ciar.EXPORT_LAST_RUN_FILE)
                    ciar.remove_last_run_file(ciar.DOWNLOAD_LAST_RUN_FILE)
                    print("Export process was clicked")
                return flag
        except Exception as e:
            print(f"There was an error in starting the export process\n{e}")
            return -1

    def download_cycle(self):
        try:
            if ciar.has_run_recently(ciar.DOWNLOAD_LAST_RUN_FILE):
                self.driver_quit()
                with open(ciar.DOWNLOAD_LAST_RUN_FILE, "r") as f:
                    download_on = f.read()
                    print(f"Activities were already downloaded on "
                          f"{datetime.fromtimestamp(float(download_on)).strftime('%Y-%m-%d %H:%M:%S')}")
                    time.sleep(3)
                return 0
            else:
                self.select_location()
                self.accept_cookies()
                self.login()
                self.accept_terms()
                was_downloaded = self.download_data(1000)  # download
                self.driver_quit()
                if self.move_downloaded_file():
                    self.unzip_file()
                    self.remove_unused_files_and_folders()
                    #
                    ciar.update_last_run(ciar.DOWNLOAD_LAST_RUN_FILE)
                    ciar.remove_last_run_file(ciar.EXPORT_LAST_RUN_FILE)
                return self.sport_sessions_folder()

        except Exception as e:
            print(f"There was an error downloading the sport sessions:\n{e}")
            return -1

    def export_and_download_activities(self):
        # print(args.email, args.password)
        sport_sessions = None
        #
        if datetime.today().day in [2, 3, 4, 15, 16, 17]:
            out = self.export_cycle()
            if out == 1:
                print("Sports sessions json files export started successfully")
            elif out == 0:
                print("Sports sessions json files export was already started")
            else:
                print("Error occurred on sports sessions json files export")
            return sport_sessions
        #
        elif datetime.today().day in [6, 7, 8, 19, 20, 21]:
            sport_sessions = self.download_cycle()
            # sport_sessions = test.sport_sessions_folder()
            if isinstance(sport_sessions, str):
                print(f"sport_sessions path: {sport_sessions}")
                ciar.save_last_download_path(sport_sessions)
                return sport_sessions
            elif sport_sessions == 0:
                pass
            else:
                print("Error occurred while downloading the sports sessions json files")
            return None
        else:
            self.view_account()
            return None


if __name__ == "__main__":
    pass
    # args = get_args()  # Import and run the argument parser
    # # print(args.email, args.password)
    # sport_sessions = None
    # test = Selenium_Runtastic(args.email, args.password)
    # if datetime.today().day in [2, 3, 4]:
    #     out = test.export_cycle()
    #     if out == 1:
    #         print("Sports sessions json files export started successfully")
    #     elif out == 0:
    #         print("Sports sessions json files export was already started")
    #     else:
    #         print("Error occurred on sports sessions json files export")
    #
    # elif datetime.today().day in [6, 7, 8]:
    #     sport_sessions = test.download_cycle()
    #     # sport_sessions = test.sport_sessions_folder()
    #     if isinstance(sport_sessions, str):
    #         print(f"sport_sessions path: {sport_sessions}")
    #     elif sport_sessions == 0:
    #         pass
    #     else:
    #         print("Error occurred while downloading the sports sessions json files")
    # else:
    #     test.view_account()
    # # test.view_account()

    args = get_args()
    test = Selenium_Runtastic(args.email, args.password)
    test.export_and_download_activities()

# merge_runtastic analysis with this file
# create a pipline that runs the script on the 2nd and 6th of a month

"""

cd C:\\Users\\USER\\Documents\Python\\Selenium_Tutorial
python -m Runtastic_Selenium.Runtastic_export_data_request -e  *** -p ***
"""
