# coding=utf-8
'''
Created on 2017-3-8
@author: liyj
Project:基础类BasePage，封装所有页面都公用的方法，
定义open函数，重定义find_element，switch_frame，send_keys等函数。
在初始化方法中定义驱动driver，基本url，title,
WebDriverWait提供了显式等待方式。
'''

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage(object):
    """
    BasePage封装所有页面都公用的方法，例如driver, url ,FindElement等
    """
    #初始化driver、url、pagetitle等
    #实例化BasePage类时，最先执行的就是__init__方法，该方法的入参其实就是BasePage的入参。
    #__init__方法不能有返回值，只能返回None
    #self是实力本身，相较于类Page类而言
    def __init__(self,selenium_driver,base_url,pagetitle):
        self.driver = selenium_driver
        self.base_url = base_url
        self.pagetitle = pagetitle

    #通过title断言进入的页面是否正确
    #使用title获取当前窗口title,检查输入的title是否是当前title中，返回比较结果
    def on_page(self,pagetitle):
        return pagetitle in self.driver.title

    # 打开页面，并校验页面链接是否加载正确
    # 以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。
    def _open(self,url,pagetitle):
        self.driver.maximize_window()
        self.driver.get(url)
        # 使用assert进行校验，打开的窗口title是否与配置的title一致。调用on_page()方法
        assert self.on_page(pagetitle),u"打开页面失败 %s"%url

    # 定义open方法，调用_open()进行打开链接
    def open(self):
        self._open(self.base_url,self.pagetitle)

    #重写元素定位方法
    def find_element(self,*loc):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print(u"%s 页面元素未能找到 %s 元素"%(self,loc))

    #重写click方法
    def click(self,loc):
        try:
            self.driver.find_element(*loc).click()
        except:
            print(u"%s 页面元素不能点击 %s 元素" % (self, loc))

    # 重写switch_frame方法
    def switch_frame(self,loc):
        return self.driver.switch_to.frame(loc)


    # 定义script方法，用于执行js脚本
    def script(self,src):
        self.driver.execute_script(src)

    # 重写定义输入（send_keys）方法
    def input(self, loc, vaule):
        try:
                self.find_element(*loc).click()
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))

    #下拉选择框操作方法
    def dropdown_select(self,loc1,loc2):
        try:
            self.find_element(*loc1).click()
            time.sleep(1)
            self.find_element(*loc2).click()
        except:
            print(u"下拉选择出错了")
