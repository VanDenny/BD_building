from selenium import webdriver
from selenium.webdriver import ActionChains
import pyautogui as pag
import time
# driver = webdriver.Chrome()
# driver.set_window_size(800, 800)
# driver.get("https://map.baidu.com/")
# enlarge_element = driver.find_element_by_xpath("//div[@class='BMap_smcbg in']")
#
# for i in range(6):
#     time.sleep(1)
#     enlarge_element.click()
# time.sleep(1)
# print(pag.size())
for i in range(10):
    pag.moveTo(10, 950, 0.5)
    pag.dragTo(265, 950, 1)

