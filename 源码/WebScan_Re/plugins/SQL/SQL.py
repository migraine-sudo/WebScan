#coding:utf-8

from WebScan import *
from SQLClass import *
from Repair import *
from time import *
import thread
import datetime


def run(urls,Thread,islog,session):#所有模块都必须定义该函数，该函数为入口函数
    if islog:#是否记录日志，可以把islog作为参数传递给对应的类，作为私有变量
        log.write("SQL", "SQL System boot")
    #Developer_API(urls,islog,session)
    if Thread==1:#单线程
        SQLInsert_Check(urls,islog,session,1,Thread,start_time)
    else:#多线程模式
        start_time=datetime.datetime.now()
        output.printf( "Scan Start AT "+str(start_time),'purple')
        if Thread>len(urls):
            output.printf ("The number of Thread is beyond the urls,please release it!",'red')
            return 0
        url_each_thread=len(urls)/Thread
        url_remain=len(urls)%Thread
        output.printf ("[+]thread_num="+str(Thread),"yellow")
        #print "url_num="+str(len(urls))
        # 分配一定url数量给每个线程
        for i in range(0,Thread):
            url_new = []
            #print "list "+str(i)
            for j in range((i)*url_each_thread,(i+1)*url_each_thread):
                url_new.append(urls[j])
                # 将余下的url添加到最后一个线程
                if i==Thread-1:
                    for x in range((i+1)*url_each_thread+1,(i+1)*url_each_thread+url_remain):
                        url_new.append(urls[x])
                        #print urls[x]
                #print urls[j]
                lists=[]
                url_lists=[]
            try:
                output.printf("[+]Starting Thread "+str(i+1)+"...")
                thread.start_new_thread(SQLInsert_Check,(url_new,islog,session,i,Thread,start_time))
                sleep(1)
            except:
                print "Error: unable to start thread"
    sleep(10)
    raw_input()


def SQLInsert_Repair(list,islog):

    r = repair()
    if list:
        for j in list:
            output.printf("\tFound SQL injection point" + "=>" + j["url"], 'red')
            r.repair_suggest(j["id"], islog)


def SQLInsert_Check(url,islog,session,thread_num,Thread,start_time):
    Sql=SQL(islog=islog,session=session) #call Insert_Function
    payload = Payload_store.payload #payload is define as a nset list
    url_list=[]
    for i in range(0,len(url)): #Traversal ALL URL
        dict=Sql.SQL_INSERT(url[i], payload)
        #print "list2="+str(dict['url'])
        if dict['url'] is not '0':###Default
            url_list.append(dict)

    # 结束判断
    if thread_num==Thread-1:#  判断最后一个线程扫描结束
        output.printf("Scan Compelte！",'red')
        end_time = datetime.datetime.now()
        output.printf("Thread= "+str(Thread),'yellow')
        output.printf("Scan Start AT " + str(start_time), 'purple')
        output.printf("Scan ENDS AT " + str(end_time), 'purple')
    sleep(10)
    #print "url_liset=" + str(url_list)
    #output.printf("[*]Connecting the Fix script..", "purple")
    SQLInsert_Repair(url_list,islog)

#开发者模式，便于调试模块
def Developer_API(urls,islog,session):
    URL='http://120.79.174.75/DVWA-master/vulnerabilities/sqli/index.php'
    #URL='http://120.79.174.75/DVWA-master/vulnerabilities/sqli/index.php?id=1&Submit=Submit&user_token=94c81a8023b240558d08f8e4fe3f6601#'
    payload=["1","1 and 1=1", "1 and 1=2"]
    params = {'id': payload[2], "Submit": "Submit"}
    r=session.get(URL)
    #print "GET1="+r.content
    g = session.get(URL,params=params)
    print g.url
    print "GET2="+g.text
