# coding=utf-8

import unittest

from QingShuSchoolPlatformTest.common.browser_config import browserSelect
from QingShuSchoolPlatformTest.common.login import *
from QingShuSchoolPlatformTest.page_object.pxPage.px_StudentListPage import StudentListPage


class StudentListTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = browserSelect()
        cls.url = test_pxUrl + '/testpx/Home'
        cls.pagurl = StudentListPage.page_url
        cls.username = "testpx_yezi"
        cls.password = "123456"
        cls.userinfo = "叶子"      #用户姓名
        cls.tableId = StudentListPage.tableId
        login(cls, cls.url, cls.username, cls.password, cls.userinfo)

    #测试用例
    def test_studentList(self):
        u"""导航栏-跳转到学员名单页面"""
        try:
            studentList_page = StudentListPage(self.driver, self.pagurl, u"青书学堂培训测试机构")
            time.sleep(1)
            #通过导航栏跳转到学员名单页面
            studentList_page.dropdown_select(StudentListPage.stuManager_loc,StudentListPage.stuList_loc)
            time.sleep(1)
            currentUrl=self.driver.current_url
            assert StudentListPage.page_url==currentUrl,'跳转到学员名单页面失败'
        except:
            raise AttributeError("打开学员名单模块失败")

    def test_studentList_01_add(self):
        u"""学员名单-添加"""
        try:
            studentList_page = StudentListPage(self.driver,self.pagurl,u"青书学堂测试机构")
            self.driver.get(self.pagurl)
            # 添加新生前统计一下总数据条数
            totalRowsNum1 = studentList_page.totalRowsCount(self.tableId)
            #添加新生
            studentList_page.click(StudentListPage.addStudentBtn_loc)
            time.sleep(1.5)
            now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))  # 获取当前时间
            userName = "stu" + now    #为避免重复，用户名用pxstu+当前时间字符串
            studentList_page.input(StudentListPage.userNameTxt_loc, userName)
            studentList_page.input(StudentListPage.pwdTxt_loc, "123456")
            studentList_page.input(StudentListPage.displayNameTxt_loc,"叶子")
            time.sleep(0.5)
            studentList_page.click(StudentListPage.addBtn_loc)
            time.sleep(1)
            # 添加之后再次统计总数据条数
            totalRowsNum2 = studentList_page.totalRowsCount(self.tableId)
            assert totalRowsNum2 == totalRowsNum1 + 1, '学生账号没显示在列表中'
        except:
            raise AssertionError("学员名单-添加学生账号失败")

    def test_studentList_02_scan(self):
        u"""学员名单-查看"""
        try:
            studentList_page = StudentListPage(self.driver, self.pagurl, u"青书学堂培训测试机构")
            self.driver.get(self.pagurl)
            # 点击第一行的查看按钮
            editBtn = studentList_page.find_table_element(self.tableId, 3, 1, 5, 1)
            editBtn.click()
            time.sleep(1)
            #获取学生信息详情页面的url
            currentUrl = self.driver.current_url
            time.sleep(0.5)
            assert "http://peixun.qingshuxuetang.com/testpx/Administrator/StudentInfo" in currentUrl, "查看学生详情出错"
            studentList_page.click(StudentListPage.scan_goBack_loc)   #返回
        except:
            raise AssertionError("学员名单-查看学生详情出错")

    def test_studentList_03_edit(self):
        u"""学员名单-编辑"""
        try:
            studentList_page = StudentListPage(self.driver,self.pagurl,u"青书学堂培训测试机构")
            self.driver.get(self.pagurl)
            #获取第一行学生的姓名
            name1 = studentList_page.find_table_element(self.tableId,0,1,2).text

            #点击第一行的编辑按钮
            editBtn = studentList_page.find_table_element(self.tableId,3,1,5,2)
            editBtn.click()
            time.sleep(1)

            newName = name1 + "new"
            studentList_page.input(StudentListPage.displayNameTxt_loc,newName)
            time.sleep(0.3)
            studentList_page.click(StudentListPage.submitBtn_loc)
            time.sleep(0.5)
            studentList_page.click(StudentListPage.confirmSubmitBtn_loc)
            time.sleep(1)
            name2 = studentList_page.find_table_element(self.tableId,0,1,2).text
            assert name2 == newName,"编辑修改学生姓名失败"
        except:
            raise AssertionError("学员名单-编辑失败")

    def test_studentList_04_delete(self):
        u"""学员名单-删除"""
        try:
            studentList_page = StudentListPage(self.driver, self.pagurl, u"青书学堂培训测试机构")
            self.driver.get(self.pagurl)
            # 每次执行删除之前都需要刷新一下（因为每点一次删除按钮就多一个dialog对话框，导致确定删除按钮的定位改变）
            self.driver.refresh()
            time.sleep(0.5)
            # 删除前统计一下总数据条数
            totalRowsNum1 = studentList_page.totalRowsCount(self.tableId)

            # 点击第一行的删除安钮
            deleteBtn = studentList_page.find_table_element(self.tableId, 3, 1, 5, 3)
            deleteBtn.click()
            time.sleep(0.5)
            studentList_page.click(StudentListPage.deleteConfirmBtn_loc)  # 删除
            time.sleep(1)
            # 添加之后再次统计总数据条数
            totalRowsNum2 = studentList_page.totalRowsCount(self.tableId)
            assert totalRowsNum2 == totalRowsNum1 - 1, '学生账号没从列表中删除'
        except:
            raise AssertionError("学员名单-删除学生账号失败")

    @classmethod
    def tearDownClass(cls):
        currenturl=cls.driver.current_url
        logout(cls,currenturl)    #注销登录
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
