# coding=utf-8
#---【培训-管理员】-学员服务-学员名单-----

from selenium.webdriver.common.by import By
from QingShuSchoolPlatformTest.page_object.test_bootStrapTable import BootStrapTable

class StudentListPage(BootStrapTable):

    page_url="http://peixun.qingshuxuetang.com/testpx/Administrator/StudentList"
    # 定位器，通过元素属性定位元素对象
    #导航栏
    stuManager_loc = (By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/ul[1]/li[2]/a')  # 导航栏-学员服务
    stuList_loc = (By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/ul[1]/li[2]/ul/li[1]/a')  # 子模块-学员名单

    tableId = "studentTable"  #学生列表ID

    addStudentBtn_loc = (By.ID, 'addStudentBtn')  # 添加新生
    #添加新生页面元素对象
    userNameTxt_loc = (By.ID, 'userNameTxt')  # 用户名
    pwdTxt_loc = (By.ID, 'pwdTxt')  # 密码
    displayNameTxt_loc = (By.ID, 'displayNameTxt')  # 姓名
    sexRadioM_loc = (By.XPATH, '//*[@id="studentAddForm"]/div[4]/div/label[1]')  # 性别男
    sexRadioF_loc = (By.XPATH, '//*[@id="studentAddForm"]/div[4]/div/label[2]')  # 性别女
    addBtn_loc = (By.XPATH, '/html/body/div[8]/div[3]/div/button/span')  # 添加按钮

    #tipsShow_loc = (By.ID, 'ui-id-5')  # 提示信息框
    confirmBtn_loc = (By.XPATH,'/html/body/div[9]/div[3]/div/button[1]/span')  #提示框-取消
    deleteConfirmBtn_loc =(By.XPATH,'/html/body/div[9]/div[3]/div/button[2]/span')  #提示框-删除

    submitBtn_loc = (By.ID, 'submitBtn')  # 编辑页面-保存
    confirmSubmitBtn_loc = (By.XPATH,'/html/body/div[10]/div[3]/div/button/span')  #提交成功提示框-确定

    scan_userNameTxt_loc = (By.XPATH,'//*[@id="studentAdmin"]/div[2]/div/text()')    #查看学生详情页面-用户名
    scan_goBack_loc = (By.XPATH,'/html/body/div[1]/div[2]/div/div[4]/a')          #查看学生详情页面-返回
