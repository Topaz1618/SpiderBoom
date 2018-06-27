from selenium import webdriver

#
def init_browser():
    """
    通过browser参数初始化全局浏览器供模拟登录使用
    :return:
    """
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    print(browser)

init_browser()