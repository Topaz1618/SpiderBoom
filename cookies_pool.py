from redis_conn import redis_client
import time
import unittest
import random
import requests
import json
import threading
from redis_conn import redis_client
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

class CP(object):
    def __init__(self,website):
        self.redis = redis_client()
        self.website = website
        # self.cookie_generate()
        self.cookie_check()

    def cookie_generate(self):
        '''
        1. 去 redis 拿用户名密码
        2. 使用 selenium 访问拿到cookie （可能会涉及到验证码，去请求打码平台）
        3.保存 cookie
        :return:
        '''
        key = self.website + '_account'
        a = self.redis.hgetall(key)
        for k, v in a.items():
            t = threading.Thread(target=self.new_cookies,args=(k.decode(),v.decode()))
            t.start()
            # self.new_cookies(k.decode(),v.decode())

    def new_cookies(self,username, password):
        print('正在从账号{}获取cookie'.format(username))
        url = 'http://my.sina.com.cn/profile/unlogin'
        browser = webdriver.Chrome()
        browser.get(url)
        wait = WebDriverWait(browser, 10)  # 只等待需要的时间
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
                print('成功获取到Cookies', cookies, type(cookies))
                cookies_str = json.dumps(cookies)
                self.save_cookies(cookies_str)
                self.cookie_check()

        except WebDriverException as e:  # 有些账号密码错误我也没有办法
            print('该账号访问失败')

    def save_cookies(self,cookies):
        website_name = self.website + '_cookies'
        self.redis.lpush(website_name, cookies)


    def cookie_check(self):
        '''
        1. 利用requests库访问个人主页
        2. 不合格删除
        :return:
        '''
        website_name = self.website + '_cookies'
        real_cookies = self.cookie_radom(website_name)
        url = 'https://weibo.cn'
        response = requests.post(url,cookies=real_cookies)
        print(response.status_code)

    def cookie_radom(self,website):
        '''
        1. 先判断是否有cookie，没有去生成
        2. 有就去检查 cookie，
        3. 返回一个随机有效的 cookie
        :return:
        '''
        cookies_list = self.redis.lrange(website, 0, 10)
        radmon_cookies = random.sample(cookies_list, 1)
        real_cookies = json.loads(radmon_cookies[0].decode())
        # print('radmon',real_cookies,type(real_cookies))
        return  real_cookies

    def verification_code(self):
        '''验证码处理'''
        pass


# https://www.jianshu.com/p/6784c261126e
# https://www.jianshu.com/p/172159f243d8

if __name__ == "__main__":
    website = input('your website >>>')
    CP(website)


    #http://my.sina.com.cn/profile/unlogin