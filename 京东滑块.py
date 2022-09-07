import random
import time
from selenium.webdriver import Chrome
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
import pyautogui
from urllib import request
from cv2 import cv2
import numpy as np


class Jd:
    def __init__(self, user, password):  # 类的对象初始化
        self.user = user
        self.password = password
        self.web = Chrome()

    def login(self):  # 登陆操作
        self.web.maximize_window()
        self.web.get('https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue')
        self.web.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[3]').click()
        self.web.find_element(By.XPATH, '//*[@id="loginname"]').send_keys(self.user)
        self.web.find_element(By.XPATH, '//*[@id="nloginpwd"]').send_keys(self.password)
        self.web.find_element(By.XPATH, '//*[@id="loginsubmit"]').click()

    def xpath_find(self, xpath_f):  # 寻找页面元素
        wait.WebDriverWait(self.web, 5).until(lambda x:x.find_element(By.XPATH, xpath_f))
        element = self.web.find_element(By.XPATH, xpath_f)
        return element

    def xpath_send(self, xpath_f, key):  # 页面输入操作
        wait.WebDriverWait(self.web, 5).until(lambda x:x.find_element_by_xpath(xpath_f))
        element = self.web.find_element(By.XPATH, xpath_f)
        element.send_keys(key)

    def img_down(self):  # 验证码图片下载
        bigimg = self.web.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src')
        request.urlretrieve(bigimg, 'big.png')
        smallimg = self.web.find_element(By.XPATH, '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img').get_attribute('src')
        request.urlretrieve(smallimg, 'small.png')

    def calculate_distance(self):  # 偏移量计算
        big_rgb = cv2.imread('big.png')
        big_gray = cv2.cvtColor(big_rgb, cv2.COLOR_BGR2GRAY) #  色彩图转为灰度图
        small_rgb = cv2.imread('small.png', 0)
        res = cv2.matchTemplate(big_gray, small_rgb, cv2.TM_CCOEFF_NORMED) #  模板匹配
        value = cv2.minMaxLoc(res)
        # print(value)
        x = value[2][0]
        return x

    def get_diff_location(self):  # 图像处理方法
        # 获取图片并灰度化
        block = cv2.imread("small.png", 0)
        template = cv2.imread("big.png", 0)
        # 二值化后的图片名称
        blockName = "block.jpg"
        templateName = "template.jpg"
        # 将二值化后的图片进行保存
        cv2.imwrite(blockName, block)
        cv2.imwrite(templateName, template)
        block = cv2.imread(blockName)
        block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
        block = abs(255 - block)
        cv2.imwrite(blockName, block)
        block = cv2.imread(blockName)
        template = cv2.imread(templateName)
        # 获取偏移量
        result = cv2.matchTemplate(block, template,
                                   cv2.TM_CCOEFF_NORMED)  # 查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
        x, y = np.unravel_index(result.argmax(), result.shape)
        print(x,y)
        return y

    def slide_by_pyautogui(self, x): #  pyautogui操作鼠标
        a = self.xpath_find('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]').location
        pyautogui.moveTo(1220, 590, duration=0.1)
        pyautogui.mouseDown()
        # y = 590 + random.randint(9, 19)
        y = 590 + random.gauss(0, 3)
        # print(y)
        pyautogui.moveTo(1220 + int(pow(x * x * random.randint(15, 23) / 20, 0.5))-20, y, duration=(random.randint(20, 31)) / 100)
        time.sleep(0.5)
        pyautogui.moveTo(1220 + int(pow(x * x * random.randint(15, 23) / 20, 0.5))+20, y, duration=(random.randint(20, 31)) / 100)
        time.sleep(0.7)
        pyautogui.moveTo(1220 + int(pow(x * x * random.randint(15, 23) / 20, 0.5)), y, duration=(random.randint(20, 31)) / 100)
        y = 590 + random.gauss(0, 3)
        pyautogui.mouseUp()
        # pyautogui.moveTo()
        # pyautogui.mouseUp(1220 + int(pow(x * random.randint(17, 21) / 20, 0.5)), y, duration=(random.randint(20, 31)) / 100)
        # y = 590+random.gauss(0,3)
        # pyautogui.moveTo(1220+x, duration=0.3)
        # pyautogui.mouseUp()

    def run(self):
        self.login()
        while True:
            self.img_down()
            x = self.calculate_distance()
            self.slide_by_pyautogui(x)
            time.sleep(2)
            result = self.web.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[4]/div[2]/div').text
            if '不匹配' in result:
                break


if __name__ == '__main__':
    jd = Jd('用户名', '密码')
    jd.run()
