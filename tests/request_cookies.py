import json
import requests
import random
from bs4 import BeautifulSoup
from redis_conn import redis_client


cookies_str  ='SINAGLOBAL=7197080447005.269.1522336022669; un=gum1618@163.com; wb_timefeed_3229632007=1; wb_cmtLike_3229632007=1; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; login_sid_t=d06792a70189e205ea0b84359dbb0231; cross_origin_proto=SSL; YF-V5-G0=c998e7c570da2f8537944063e27af755; _s_tentry=login.sina.com.cn; Apache=1085096960280.9801.1529748776594; ULV=1529748776600:25:11:7:1085096960280.9801.1529748776594:1529578582094; WBtopGlobal_register_version=d927b74c35516a8c; YF-Page-G0=280e58c5ca896750f16dcc47ceb234ed; wb_view_log=1366*7681; SCF=AkRZq_51q64R85BHqHNwSzoSZN5rIQvWSvwS-M36iGlqKCWjOgIMChObthA8ZgM28VvSu_JIdlGfwG6XYCJFRcQ.; SUB=_2A252Kis6DeRhGeBL7FUT9izIzjmIHXVVXhvyrDV8PUNbmtANLUrekW9NRswYWG76aZ_cB2E61zdI9CG_CnTAeJFt; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.vc7Vo1ivC4E2GS0dONcJ5JpX5K2hUgL.FoqfS0MESozXSK-2dJLoI7DKMsL.9Pz7So2R; SUHB=0WGMfKhZWTB-ZJ; ALF=1561300714; SSOLoginState=1529764714; wvr=6; UOR=,,my.sina.com.cn; wb_timefeed_6577262455=1'
cookie_list = cookies_str.split(';')
cookie_dic = {}
for s in cookie_list:
    z = s.split('=')
    cookie_dic[z[0]] = z[1]
# print(cookie_dic)


my_cookie ={'sso_info': 'v02m6alo5qztZOchqWkmZeIsI2jhLiJp5WpmYO0to2TnLeMo5iyjYOUtQ==', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.vc7Vo1ivC4E2GS0dONcJ5NHD95QcSKMNeoqESh-fWs4DqcjZ-NWD9sHEehqp15tt', 'ALF': '1561542387', 'SCF': 'Al0eiEy9SUqWzFL_oCD1odTosWqe-vXM6kpWGwMDmrtJ6G61tKsqI9FipCqTRbxS8I93TtJ5RGzuzpDWJzZ8m78.', 'Apache': '124.200.185.74_1530006385.766404', 'SUB': '_2A252NnsjDeRhGeBL7FUT9izIzjmIHXVVQuvrrDV_PUNbm9BeLRb7kW9NRswYWDgapweIpndfSxi3CUVcSMmrdv1a', 'SINAGLOBAL': '124.200.185.74_1530006385.766400', 'ULV': '1530006387018:1:1:1:124.200.185.74_1530006385.766404:', 'UOR': ',my.sina.com.cn,', 'WEB2': '73ecfc2809683ca916c781f2d0b4c73a', 'U_TRS2': '0000004a.fb054e0.5b320b70.96a70213', 'U_TRS1': '0000004a.fafa4e0.5b320b70.ebeb7ca6'}
print(type(my_cookie))



a = json.dumps(my_cookie)
print(type(a))
website_name = 'weibo_cookies'
r = redis_client()
# print(r.get('weibo_account'))
r.lpush(website_name, a)
cookies_list = r.lrange(website_name,0,10)
random.sample(cookie_list, 1)





# b = json.loads(a)
# print(type(b))

# new_cookies = {}
# print('len(a)',len(a))
# num = 0
# for i in a:
#     print("len(i)",len(i),type(i))
#     num +=len(i)
#     for k,v in i.items():
#         new_cookies[k] = v
#
# print(len(new_cookies),new_cookies)
# cookies = json.dumps(new_cookies)
# print(num,cookies)
url = 'https://weibo.cn'


# response = requests.post(url, cookies=cookie_dic)
# print(response.status_code)
# if response.status_code == 200:
#     print('ok')
#     # html = response.text
    # soup = BeautifulSoup(html, 'html')
    # title = soup.title.string
    # if title == '我的首页':
    #     print("ok")
    # else:
    #     print("失效")