#!/usr/bin/python
# -*- coding: utf-8 -*-
from WebScan import *
from BackDoorClass import *
from Repair import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def run(urls,thread,islog,session):#所有模块都必须定义该函数，该函数为入口函数

    if islog:#是否记录日志，可以把islog作为参数传递给对应的类，作为私有变量
        log.write("BackDoor", "BackDoor System boot")
    backdoor=BackDoor()
    output.printf("[*]Start testing the site:"+urls[0],"green")
    for i in range(0,5):
        output.printf("[*]Start the "+str(i)+" round of testing", "white","bblue")
        backdoor.CheckBack(urls[0],i,session,thread)
    output.printf("[*]Scanning is complete!" , "blue")

    if backdoor.find :
        output.printf("[*]These are potentially vulnerable urls:", "red")

        for url in backdoor.find:
            output.printf("    [URL]=>" + url, "blue")
        output.printf("[*]Restoration proposal:","green")
        output.printf("[+]"+repair(), "red")
    else:
        output.printf("[-]No suspicious shell has been scanned yet", "white", "bred")


