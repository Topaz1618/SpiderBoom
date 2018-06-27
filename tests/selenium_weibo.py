import time
import unittest
import requests
import json
from redis_conn import redis_client
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

#http://my.sina.com.cn/profile/unlogin
def new_cookies(username, password):
    print('正在从账号{}获取cookie'.format(username))
    url = 'http://my.sina.com.cn/profile/unlogin'
    browser = webdriver.Chrome()
    browser.get(url)
    wait = WebDriverWait(browser, 10)   #只等待需要的时间
    try:  # 找到登陆的用户名密码输入框
        elements_visible = EC.visibility_of_element_located((By.ID, 'hd_login'))
        login = wait.until(elements_visible)
        login.click()
        user_ele = EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="loginname"]'))
        passwd_ele = EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="password"]'))
        submit_ele = EC.visibility_of_element_located((By.CSS_SELECTOR, '.login_btn'))
        user = wait.until(user_ele)
        user.send_keys(username)
        wait.until(passwd_ele).send_keys(password)
        submit = wait.until(submit_ele)
        submit.click()  # 如果没有验证码就直接登陆了，接下来就检验登陆是否成功
        try:
            time.sleep(1)
            delay = browser.find_element_by_class_name('login_error_tips').text
            if '登陆' in delay:
                print('遇到登陆限制，进入睡眠一段时间')
                time.sleep(30)
                submit.click()
            if '错误' in delay:
                print('用户名密码错误，更换账号')
                return None
        except Exception as e:  # 如果超时，则出现了验证码
            print('出现验证码，开始识别')
            # 先找到验证码的图片地址，然后发去在线打码平
        else:
            cookies = {}
            for cookie in browser.get_cookies():
                cookies[cookie["name"]] = cookie["value"]
            print('成功获取到Cookies',cookies,type(cookies))
            save_cookies(cookies)
            test_cookies(cookies)

    except WebDriverException as e:  # 有些账号密码错误我也没有办法
        print('该账号访问失败')

def save_cookies(cookies):
    cookies_str = json.loads(cookies)
    print(type(cookies_str))
    website_name = 'weibo_cookies'
    r = redis_client()
    r.lpush(website_name,cookies_str)



def test_cookies(cookies):
    url = 'https://weibo.cn'
    response = requests.post(url,cookies=cookies)
    print(response.status_code)
    # if response.status_code == 200:
    #     html = response.text
    #     soup = BeautifulSoup(html,'html')
    #     title = soup.title.string
    #     if title == '我的首页':
    #         print("ok")
    #     else:
    #         print("失效")

if __name__ == "__main__":
    new_cookies('sdefu477@163.com','spiders')
