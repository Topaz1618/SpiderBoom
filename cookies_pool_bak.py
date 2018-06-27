import random
import json
import requests
from redis_conn import redis_client
from settings import TEST_URL_MAP


class Redis_Process(object):
    def __init__(self, store_type, website):
        self.redis = redis_client()
        self.store_type = store_type
        self.website = website

    def name(self):
        '''拼接 hash name '''
        Hash_name = self.store_type +':' + self.website
        print('HASH>>>',Hash_name)
        return Hash_name

    def set(self, username, value):
        ''' 设置键值对 '''
        hash_name = self.name()
        set_value = self.redis.hset(hash_name,username,value)
        return set_value

    def get(self, username):
        '''根据键名获取键值   '''
        get_value =  self.redis.hget(self.name(), username)
        print(get_value)
        return get_value

    def delete(self, username):
        '''根据键名删除键值对 '''
        del_value = self.redis.hdel(self.name(), username)
        return del_value

    def count(self):
        '''获取数目'''
        count_value = self.redis.hlen(self.name())
        return count_value

    def random(self):
        ''' 返回随机 cookies  '''
        lucky_value = random.choice(self.redis.hvals(self.name()))
        return lucky_value

    def usernames(self):
        '''获取全部用户'''
        all_user = self.redis.hkeys(self.name())
        return all_user

    def all(self):
        '''获取全部键值对'''
        all_value = self.redis.hgetall(self.name())
        return all_value

# class ValidTester(object):
#     def __init__(self,website):
#         self.website = website
#         self.cookies_db = Redis_Process('cookies', self.website)
#         self.accounts_db = Redis_Process('accounts', self.website)
#
#     def tester(self, username, cookies):
#         raise NotImplementedError
#
#     def run(self):
#         cookies_groups = self.cookies_db.all()
#         for username, cookies in cookies_groups.items():
#             self.tester(username, cookies)
#
# class WeiboValidTester(ValidTester):
#     '''cookies 检查'''
#     def __init__(self, website='weibo'):
#         ValidTester.__init__(self, website)
#
#     def test(self, username, cookies):
#         try:
#             cookies = json.loads(cookies)
#         except TypeError:
#             print('不合法 cookies', username)
#             self.cookies_db.delete(username)
#             return
#         try:
#             url = TEST_URL_MAP[self.website]
#             response = requests.get(url, cookies=cookies, timeout=5, allow_redirects=False)
#             if response.status_code == 200:
#                 print(' %s Cookies有效\n >>> 测试结果:%s ' %(username, response.text[0:50]))
#             else:
#                 print('%s Cookies失效\n >>> 状态码 & Header：%s %s' %(username,response.status_code,response.headers))
#                 self.cookies_db.delete(username)
#         except ConnectionError as e:
#             print('Error :', e.args)
#
# def random(website):
#     """
#     获取随机的Cookie, 访问地址如 /weibo/random
#     :return: 随机Cookie
#     """
#     pass



if __name__ == '__main__':
    a = Redis_Process('account','weibo')
    # a.set('aaa','12')
    a.get('aaa')