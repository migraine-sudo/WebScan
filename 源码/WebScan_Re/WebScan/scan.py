#!/usr/bin/python
# -*- coding: utf-8 -*-
import log
import output
import re
import requests
import urllib


# 扫描类
class scan:
    def __init__(self, url="http://127.0.0.1", threads=3, islog=True, depth=3, timeout=5, session=requests.session()):
        self.threads = threads
        # 默认三线程
        self.islog = islog
        # 默认记录log
        self.url = url
        # 默认本地url
        self.depth = depth
        # 默认三层深度
        self.timeout = timeout
        # 访问超时
        self.needcheck = []
        # 需要检查的url列表为空
        self.session = session

    def scan(self):
        self.run(self.url, 1)
        return self.needcheck

    def run(self, url, depth):

        if depth - 1 >= self.depth:  # 高于初始设置
            # printf("[-]End scan <" + str(depth) + "> " + url, "yellow")
            return False  # 过深不挖
        else:
            output.printf("[*]Start scan <" + str(depth) + "> " + url, "green")

        s = self.session

        if url not in self.needcheck:
            res = s.get(url,  timeout=self.timeout)
            #print res.content
            if res.status_code == 200:
                self.needcheck.append(url)
                urlList = self.findUrl(res.content,url)
                if self.islog:
                    log.write("WebScan", "Found Url:" + url)
                # self.needcheck += urlList
                # self.needcheck = list(set(self.needcheck))
                for v in urlList:
                    # self.depth=depth+1
                    self.run(v, depth + 1)

    def domain(self, url):
        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        return "unkonw" if not res else res

    def filter(self, url):  # 过滤花里胡哨的东西,略有不足
        reg = ['.html', '.txt', '/']
        for v in reg:
            if url.rfind(v) + len(v) == len(url):
                return True
        if url.find(".php") != -1:
            return True
        return False

    def findUrl(self, page,url):

        pattern = re.compile(ur'href="(.*?)"')
        result = pattern.findall(page)

        if not result:
            output.printf("[-]Found nothing ...", "yellow")
            return result

        a = []
        output.printf("[+]Found some thing ...", "red")
        u = url.rfind("/")

        if u!=len(url)-1:
           url=url[0:u]
        domain= self.domain(url)
        #print result
        for v in result:

            if not self.filter(v):
                continue
            elif v.find('//') == 0:
                v = "http:" + v
            elif v.find('index.php') != -1:
                v = v.replace("index.php", "")
            elif v.find("http")==-1:#没有前缀的
                v = url + v

            if v.find(domain) != -1:#只要该域的
                v=v.replace("../","")
                output.printf("    " + v, "blue")
                a.append(v)
        return a
