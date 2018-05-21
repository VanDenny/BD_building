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
def drag_left(n):
    for i in range(n):
        pag.moveTo(20, 150, 0.5)
        pag.dragTo(275, 150, 1)

def drag_right(n):
    for i in range(n):
        pag.moveTo(275, 150, 0.5)
        pag.dragTo(20, 150, 1)

def drag_down(n):
    for i in range(n):
        pag.moveTo(10, 200, 0.5)
        pag.dragTo(10, 150, 1)


if __name__ == "__main__":
    drag_left(10)

