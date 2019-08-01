#!/usr/bin/python
# -*- coding: utf-8 -*-
from WebScan import *
import requests
class BackDoor:
    def __init__(self):
        self.find = []#发现的后门路径

    def CheckBack(self,url, Btype,session,thread):
        filename=["PHP.txt","ASP.txt","JSP.txt","ASPX.txt","DIR.txt","MDB.txt"]
        with open("./plugins/BackDoor/directorys/"+filename[Btype], mode="r") as file_obj:
            contents = file_obj.readlines()
        self.count=len(contents)
        i=0
        for line in contents:
            i = i + 1
            line=line.lstrip('/')
            self.CheckTest(url+line.replace('\n', ''),i,session)


    def CheckTest(self,url,i,session):
        try:
            #s = requests.session()
            #s.keep_active = True
            r = session.get(url, timeout=10)

            pecent=round(float(i)/self.count,3)*100

            output.printf("[*]["+str(pecent)+"%]Trying:[" + str(r.status_code) + "]" + url,"green")

            if (r.status_code == 200):
                self.find.append(url)
        except:
            output.printf("[-]System Error!","white","bred")
            return