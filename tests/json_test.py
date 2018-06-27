import json
import requests
form_data = {'username': '123456'}
print(type(json.dumps(form_data)))

cookie_dic = {}
response = requests.get('https://www.baidu.com')
for k, v in response.cookies.items():
    print(k,'',v)
print(cookie_dic)