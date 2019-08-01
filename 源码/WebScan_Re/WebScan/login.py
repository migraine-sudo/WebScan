#coding:utf-8
"""
 * Name:login
 * User: dreamn
 * Date: 2019-07-13
 * Time: 14:15
 * Description:用来登录dvwa测试网站
"""
import requests,re
def login(url):
    s = requests.session()
    s.keep_active = True
    f=s.get(url)

    pattern = re.compile(ur"name='user_token' value='(.*?)'")

    usertoken = pattern.findall(f.content)

    #print usertoken

    data={"username":"admin","password":"password","user_token":usertoken[0],"Login":"Login"}

    r=s.post(url+"/login.php",data=data)
    #cookieList=requests.utils.dict_from_cookiejar(s.cookies)
    #print r.content

    return s