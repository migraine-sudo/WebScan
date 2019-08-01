# coding:utf-8
import re
from urlparse import *


# Make sure we have a single URL argument.
def getDomain(url):
    parsed_url = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_url)
    return domain


def CheckUrl(url):
    pattern = re.compile(ur'(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    result = pattern.search(url)
    if result is None:
        return False
    else:
        return True


def CheckThread(num):
    if int(num) < 2 or int(num) > 50:
        return False
    else:
        return True


def CheckDepth(num):
    if int(num) < 1 or int(num) > 10:
        return False
    else:
        return True
