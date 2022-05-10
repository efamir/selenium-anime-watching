from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import pickle
from os.path import exists


# writes cookies when Enter is pressed
def get_cookie():
    service = Service("driver/geckodriver")
    driver = webdriver.Firefox(service=service)
    try:
        driver.get("https://jut.su/")
        input("Please login to your account and then press Enter to finish.\n")
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))
    except Exception as ex:
        print(f"Something have gone wrong and here's exception: {ex}")
        exit()
    finally:
        driver.quit()


# finishes the program if user closes the browser
def exit_if_closed(driver: webdriver.Firefox):
    try:
        _ = driver.window_handles
    except Exception:
        exit()


def main():
    # driver object creation
    service = Service("driver/geckodriver")
    driver = webdriver.Firefox(service=service)
    # installing adblocker
    driver.install_addon("ublock_origin-1.42.4-an+fx.xpi")
    try:
        driver.get("https://jut.su/")
        actions = ActionChains(driver)
        # loads cookies
        for cookie in pickle.load(open("cookies", "rb")):
            driver.add_cookie(cookie)
        time.sleep(2)
        driver.refresh()

        while True:
            exit_if_closed(driver)
            try:
                # checks for existence and clicks the skip opening button
                skip_opening_button = driver.find_element(by=By.CLASS_NAME, value="vjs-overlay-skip-intro")
                actions.move_to_element(skip_opening_button)
                actions.click()
                actions.perform()
                time.sleep(3)
            except Exception:
                # delay so as not to press the button several times
                time.sleep(1)
            try:
                # checks for existence and clicks the next episode button
                skip_opening_button = driver.find_element(by=By.CLASS_NAME, value="vjs-overlay-bottom-right")
                actions.move_to_element(skip_opening_button)
                actions.click()
                actions.perform()
                time.sleep(2)
                play_button = driver.find_element(by=By.CLASS_NAME, value="vjs-big-play-button")
                actions.move_to_element(play_button)
                actions.click()
                time.sleep(0.2)
                # clicks the fullscreen button
                play_button = driver.find_element(by=By.CLASS_NAME, value="vjs-fullscreen-control")
                actions.move_to_element(play_button)
                actions.click()
                time.sleep(2)
            except Exception:
                pass
    finally:
        driver.quit()


if __name__ == '__main__':
    # writes cookies of user if they don't exist
    if not exists("cookies"):
        get_cookie()
    # the main program
    main()
