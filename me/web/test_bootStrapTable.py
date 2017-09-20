#coding=utf-8
#bootstrapTable分页、翻页
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from QingShuSchoolPlatformTest.page_object.test_BasePage import BasePage

class BootStrapTable(BasePage):

    # 跳转到最后一页
    def jump_to_lastPage(self, tableId):
        js1 = "totalPagesNum=$('#" + tableId + "').bootstrapTable('getOptions').totalPages;" \
               "$('#" + tableId + "').bootstrapTable('selectPage',totalPagesNum);"
        self.driver.execute_script(js1)

    #获取列表的所有页数
    def totalPagesCount(self, tableId):
        js2 = "return $('#" + tableId + "').bootstrapTable('getOptions').totalPages;"
        totalPagesNum = self.driver.execute_script(js2)
        return totalPagesNum

    # 获取列表的所有行数
    def totalRowsCount(self, tableId):
        js3 = "return $('#" + tableId + "').bootstrapTable('getOptions').totalRows;"
        totalRowsNum = self.driver.execute_script(js3)
        return totalRowsNum

    # 跳转到指定页
    def jump_to_Page(self, tableId, pageNum):
        js3 = "$('#" + tableId + "').bootstrapTable('selectPage',"+pageNum+");"
        self.script(js3)
        time.sleep(1)

    #设置每页显示的信息条数
    def set_pageSize(self,pageSize):
        pageSize_loc = (By.CLASS_NAME, 'page-size')
        if pageSize==10:
            pageSelect_loc=(By.XPATH, '/html/body/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/span[2]/span/ul/li[1]/a')
        elif pageSize==25:
            pageSelect_loc = (By.XPATH,'/html/body/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/span[2]/span/ul/li[2]/a')
        elif pageSize==50:
            pageSelect_loc = (By.XPATH, '/html/body/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/span[2]/span/ul/li[3]/a')
        else:
            pageSelect_loc = (By.XPATH, '/html/body/div[2]/div/div/div[1]/div[2]/div[4]/div[1]/span[2]/span/ul/li[4]/a')
        #下拉选择每页显示的行数
        self.dropdown_select(pageSize_loc,pageSelect_loc)

    #------查找table当前页中的元素-----
    #rowNum  元素所在页的行号
    #colNum  元素在table中列号
    #elementNum  元素在单元格（行号列号确定一个单元格）中的位置号
    #例如 // *[ @ id = "teacherTable"] / tbody / tr[2] / td[5] / a[1]
    #tableId="teacherTable"；rowNum=2，colNum=5,elementNum=1 ---表示teacherTable中第2行第5列中的第1个元素
    #typeId 表示控件类型：显示信息的字段类型为0， 勾选框类型为1, 单元格中只有一个button的类型为2, 单元格中有多个button的类型为3
    def find_table_element(self,tableId,typeId,rowNum,colNum,elementNum=1):
        if typeId == 0:
            element_loc = (By.XPATH, "//*[@id='" + tableId + "']/tbody/tr[" + str(rowNum) + "]/td[" + str(colNum) + "]")
        elif typeId == 1:
            element_loc = (By.XPATH, "//*[@id='" + tableId + "']/tbody/tr[" + str(rowNum) + "]/td[" + str(colNum) + "]/input")
        elif typeId == 2:
            #elementNum默认设置的1
            element_loc = (By.XPATH,"//*[@id='" + tableId + "']/tbody/tr[" + str(rowNum) + "]/td[" + str(colNum) + "]/a")
        else:
            element_loc = (By.XPATH,"//*[@id='" + tableId + "']/tbody/tr[" + str(rowNum) + "]/td[" + str(colNum) + "]/a[" + str(elementNum) + "]")
        time.sleep(0.5)
        return self.find_element(*element_loc)

    #----------查找table最后一页、最后一行中的元素-----
    def find_table_lastPage_lastRow_element(self, tableId,typedId, colNum, elementNum=1):
        # 跳转到最后一页
        self.jump_to_lastPage(tableId)
        time.sleep(0.5)
        totalPagesNum = self.totalPagesCount(tableId)
        totalRowsNum = self.totalRowsCount(tableId)
        # 最后一页最后一行
        pageSize =int(totalRowsNum/totalPagesNum)
        if pageSize>0 and pageSize<=10:
            pageSize=10
        elif pageSize>10 and pageSize<=25:
            pageSize=25
        else:
            pageSize=50
        lastRowNum = totalRowsNum-(totalPagesNum - 1)*pageSize
        # 点击最后一页,最后一行的编辑按钮
        element_loc = self.find_table_element(tableId, typedId, lastRowNum, colNum, elementNum)
        return element_loc
