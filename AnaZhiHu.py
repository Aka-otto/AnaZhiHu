#!/usr/bin/env python
# coding=utf-8
# author=dave.fang@outlook.com
# create=20150520

"""
* A Tool For Analysing Zhihu User.
* GitHub: https://github.com/Captain-D/AnaZhiHu
* Version: 1.0
"""
import datetime
import requests
import BeautifulSoup
import re
import sys
import json
from common.output import *

XSRF = ''
COOKIES = {
    'q_c1': '',
    'z_c0': '',
    '_xsrf': XSRF
}
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Origin': 'http://www.zhihu.com',
    'Referer': 'http://www.zhihu.com/people/dave-9/followees',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}


def update(start_code, uid):
    post_date = {
        'start': start_code,
        '_xsrf': XSRF
    }
    uri = "http://www.zhihu.com/people/" + str(uid) + "/activities"
    try_count = 0
    while True:
        try:
            req = requests.post(uri, data=post_date, cookies=COOKIES, headers=HEADER, timeout=15 * (try_count + 1))
            try_count = 0
            break
        except:
            print "Post Failed! Reposting..."
            try_count += 1
            time.sleep(3)  # sleep 3 seconds to avoid network error.
    data = json.loads(req.content)
    msg_num = int(data["msg"][0])
    msg_content = data["msg"][1]
    content_analyse(msg_content, uid)
    next_time = datetime_analyse(msg_content)
    print "[+] Key: " + next_time
    try:
        if msg_num == 20:
            update(next_time, uid)
    except Exception, e:
        print "[-] Error: %s" % e


def datetime_analyse(content):
    try:
        _Soup = BeautifulSoup.BeautifulSoup(content)
        _pageList = _Soup.findAll(attrs={'class': 'zm-profile-section-item zm-item clearfix'})
        # print _pageList[-1]
        date_time = re.findall('data-time=\"(.*?)\"', str(_pageList[-1]))
        if len(date_time) != 1:
            return -1
        return date_time[0]
    except Exception, e:
        print "[-] datetime_analyse Error: %s" % e
        return -1


def content_analyse(content, uid):
    try:
        _soupTmp = BeautifulSoup.BeautifulSoup(content)
        question_contents = _soupTmp.findAll(attrs={
            'class': 'zm-profile-section-main zm-profile-section-activity-main zm-profile-activity-page-item-main'})
        for question in question_contents:
            tmp = str(question).split("赞同了回答")
            if len(tmp) == 2:
                question_analyse(question, uid)
    except Exception, e:
        print "[-] content_analyse Error: %s" % e
        pass


def question_analyse(question, uid):
    try:
        # print question
        uri = re.findall('target=\"_blank\" href=\"(.*?)\"', str(question))
        pattern = uri[0] + '\">(.*?)</a>'
        name = re.findall(pattern, str(question))
        print "[+]" + uri[0]
        if "target=\"_blank\"" in str(question):
            output_add("http://www.zhihu.com" + uri[0], name[0], uid)
    except Exception, e:
        print "[-] question_analyse Error: %s Q: %s" % (e, question)
        pass


def start_analyse(uid):
    output_init(uid)
    try_count = 0
    uri = "http://www.zhihu.com/people/" + str(uid)
    while True:
        try:
            req = requests.get(uri, cookies=COOKIES, headers=HEADER, timeout=15 * (try_count + 1))
            try_count = 0
            break
        except:
            print "Post Failed! Reposting..."
            try_count += 1
            time.sleep(3)  # sleep 3 seconds to avoid network error.
    content_analyse(req.content, uid)
    next_time = datetime_analyse(req.content)
    print next_time
    if next_time != -1:
        update(next_time, uid)
    output_finished(uid)


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print "[*] AnaUser is hot."
    if len(sys.argv) == 1:
        print "[-] Error! You should input the UID you want to Analyse."
        print "[-] E.g. python AnaZhiHu.py dave-9"
    else:
        uid = sys.argv[1]
        start_analyse(uid)
    end_time = datetime.datetime.now()
    print '[*] Total Time Consumption: ' + \
          str((end_time - start_time).seconds) + 's'
