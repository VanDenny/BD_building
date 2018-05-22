"""step 1 导入依赖库"""
from os import path
import pyautogui as pag
from browsermobproxy import Server
from selenium import webdriver
import re
from Clawer_Base.clawer_frame import Clawer
from Clawer_Base.user_agents import User_agents
import pandas as pd
from Clawer_Base.shape_io import Shapefile_Write
from Clawer_Base.progress_bar import view_bar
import time
import json

"""step 2 新建浏览器监控类"""
class Monitor(object):
    """
    step 3 配置chromedriver 和 browermobproxy 路径
    需要使用完整路径，否则browsermobproxy无法启动服务
    我是将这两个部分放到了和monitor.py同一目录
    同时设置chrome为屏蔽图片，若需要抓取图片可自行修改
    """
    PROXY_PATH = path.abspath(r"D:\Anaconda3\browsermob-proxy-2.1.4\bin/browsermob-proxy.bat")
    CHROME_PATH = path.abspath(r"D:\Anaconda3\chromedriver.exe")
    CHROME_OPTIONS = {"profile.managed_default_content_settings.images": 2}

    def __init__(self):
        """
        类初始化函数暂不做操作
        """
        pass
        
    def initProxy(self):
        """
        step 4 初始化 browermobproxy
        设置需要屏蔽的网络连接，此处屏蔽了css，和图片（有时chrome的设置会失效），可加快网页加载速度
        新建proxy代理地址
        """
        self.server = Server(self.PROXY_PATH)
        self.server.start()        
        self.proxy = self.server.create_proxy()
        self.proxy.blacklist(["http://.*/.*.css.*", "http://.*/.*.jpg.*", "http://.*/.*.png.*", "http://.*/.*.gif.*"], 200)
        
    def initChrome(self):
        """
        step 5 初始化selenium， chrome设置
        将chrome的代理设置为browermobproxy新建的代理地址
        """            
        chromeSettings = webdriver.ChromeOptions()
        chromeSettings.add_argument('--proxy-server={host}:{port}'.format(host = "localhost", port = self.proxy.port))
        chromeSettings.add_experimental_option("prefs", self.CHROME_OPTIONS)
        self.driver = webdriver.Chrome(executable_path = self.CHROME_PATH, chrome_options = chromeSettings)
     
    def genNewRecord(self, name = "monitor", options={'captureContent':True}):
        """
        step 6 新建监控记录，设置内容监控为True
        """
        self.proxy.new_har(name, options = options)
    
    def getContentText(self, targetUrl):
        """
        step 7 简单的获取目标数据的函数
        其中 targetUrl 为浏览器获取对应数据调用的url，需要用正则表达式表示
        """
        if self.proxy.har['log']['entries']:
            for loop_record in self.proxy.har['log']['entries']:
                try:
                    if re.fullmatch(targetUrl , loop_record["request"]['url']):
                        return loop_record["response"]['content']["text"]
                except Exception as err:
                    print(err)
                    continue
        return None

    
    def start(self):
        """step 8 配置monitor的启动顺序"""
        try:
            self.initProxy()
            self.initChrome()
            print('初始化完成')
        except Exception as err:
            print(err)
    
    def quit(self):
        """
        step 9 配置monitor的退出顺序
        代理sever的退出可能失败，目前是手动关闭，若谁能提供解决方法，将不胜感激
        """
        self.driver.close()
        self.driver.quit()
        try:
            self.proxy.close()
            self.server.process.terminate()
            self.server.process.wait()
            self.server.process.kill()
        except OSError:
            pass

class BD_Build_clawer(Clawer):
    def __init__(self, url):
        self.url = url
        self.headers = User_agents().get_headers()
        self.params = ''
        self.proxys = {'proxies': ''}
        self.cookies = ''
        self.key_type = ''

    def scheduler(self):
        return self.parser(self.respond)

    def parser(self, json_dict):
        print(self.respond)
        res_list = []
        for parts in json_dict:
            if isinstance(parts, list):
                for part in parts:
                    print(part)
                    if isinstance(part, list) and len(part) == 6:
                        build_info = {}
                        point_list = []
                        part[0][0][0] = 129 + part[0][0][0]
                        part[0][0][1] = 129 + part[0][0][1]
                        for ord, point in enumerate(part[0]):
                            if ord >= 1:
                                point[0] = point[0] + last_point[0]
                                point[1] = point[1] + last_point[1]
                            point_list.append(point)
                            last_point = point
                        point_list.append(point_list[0])
                        build_info['geo'] = point_list
                        build_info['id'] = part[1]
                        build_info['fe_2'] = part[2]
                        build_info['height'] = part[3]
                        build_info['fe_4'] = part[4]
                        build_info['code'] = part[5]
                        res_list.append(build_info)
        return res_list

class get_url:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.url = url
        self.PROXY_PATH =

    def open_web(self, win_size=(800,800)):
        self.driver.set_window_size(*win_size)
        self.driver.get(self.url)

    def win_setting(self):
        enlarge_element = self.driver.find_element_by_xpath("//div[@class='BMap_smcbg in']")
        for i in range(6):
            time.sleep(1)
            enlarge_element.click()

    def initProxy(self):
        """
        step 4 初始化 browermobproxy
        设置需要屏蔽的网络连接，此处屏蔽了css，和图片（有时chrome的设置会失效），可加快网页加载速度
        新建proxy代理地址
        """
        self.server = Server(self.PROXY_PATH)
        self.server.start()
        self.proxy = self.server.create_proxy()

    def initWeb(self):
        self.open_web()
        self.win_setting()

    def move(self, x_offset, y_offset):
        








if __name__ == "__main__":
    bdbuild_clawer = BD_Build_clawer(r'https://ss3.bdstatic.com/8bo_dTSlR1gBo1vgoIiO_jowehsv/pvd/?qt=tile&param=3N5L%40%3BJ8FLE%3A%3BEK9FK52%3F3J96E9FA%3BC96E98O5K%3FCDI8A%3DB%3FBE92A%3BB6KCHLA%3BC6KH8DM%3D%3B%40BPEB%3E38%40JPE2%403J6KLH%3AO3O8%3AJ54%403B8FJE%3E4')
    res_list = bdbuild_clawer.process()
    print(res_list)
    num = len(res_list)
    shape_writer = Shapefile_Write('ploygon', [('id', 'C'),
                                               ('fe_2', 'C'),
                                               ('height', 'C'),
                                               ('fe_4', 'C'),
                                               ('code', 'C'),
                                               ])
    for order, i in enumerate(res_list):
        view_bar(order, num)
        print(order)
        points = i['geo']
        shape_writer.plot(points,(i['id'], i['fe_2'], i['height'], i['fe_4'], i['code']))
    shape_writer.save(r'D:\program_lib\BD_Building\test_shape')

    df = pd.DataFrame(res_list)
    df.to_csv('a_test.csv')
    # print(df)
    # monitor = Monitor()
    # monitor.start()
    # monitor.genNewRecord()
    #
    # monitor.driver.get("https://s.taobao.com/search?q=薯条")
    # # targetUrl = "https://s.taobao.com/api.*?"
    # # text = monitor.getContentText(targetUrl)
    # # with open('1.har', 'w') as outfile:
    # #     json.dump(monitor.proxy.har, outfile)
    # print(monitor.proxy.har)
    # monitor.quit()