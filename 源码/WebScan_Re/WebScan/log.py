# coding:utf-8
import time


def write(name, logs):
    with open('./logs/' + name + '.logs', 'a+') as f:
        f.write(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + logs + "\r\n")
