import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
import time
import random
from dotenv import load_dotenv

load_dotenv()

login = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
path = '/Users/egor_datsishin/PycharmProjects/Analyser_activities_from_Strava/gpx_files'


def get_data(id: int):
    url = f'https://www.strava.com/activities/{id}/export_gpx'
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': path}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(login)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
    time.sleep(random.randrange(2, 3, 1))

    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    target_file = max(files, key=os.path.getctime)
    output_file = f'{path}' + '/' + f'{id}.gpx'
    os.rename(target_file, output_file)


# if __name__ == '__main__':
#     get_data()
