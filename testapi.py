from itertools import chain, zip_longest
import requests
from lxml import etree
import re
from fake_useragent import FakeUserAgent
import datetime


cookies = 'ServerSide=https://guangdong.xueanquan.com/;UserID=6B0A87E07EB878EC437CABB6803CBC17'

def teacher_get_special_list(cookie):
    '''
    教师获取专题任务信息
    以 List 的形式输出
    {'专题名', '截止时间', '完成人数', '应完成人数', '完成百分比', '专题状态'}
    学生账号，不分专题任务和学期任务接口，可怕
    '''
    all_special_list = list()
    get_today = datetime.date.today()
    url = 'https://applet.xueanquan.com/pt/guangdong/safeapph5/api/safeEduScore/getSpecailProgress?semester=3&schoolYear='+str(get_today.year)
    headers = {'Host': 'applet.xueanquan.com',
               'Origin': 'https://safeh5.xueanquan.com',
               'Accept-Encoding': 'gzip, deflate, br',
               'Cookie': cookies,
               'Connection': 'keep-alive',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
               'Referer': 'https://safeh5.xueanquan.com'}
    res = requests.get(url=url, headers=headers)
    #print(res.text)

    specialName_all = re.findall('"specialName": (.*?),', res.text)
    endTime_all = re.findall('"endTime": (.*?),', res.text)
    completePeople_all = re.findall('"completePeople": (.*?),', res.text)
    shouldCompletePeople_all = re.findall('"shouldCompletePeople": (.*?),', res.text)
    completeRate_all = re.findall('"completeRate": (.*?),', res.text)
    specailStatus_all = re.findall('"specailStatus": (\d)', res.text)

    for specialname,endtime,completepeople,shouldcompletepeople,completerate,specailstatus in zip(specialName_all,endTime_all,completePeople_all,shouldCompletePeople_all,completeRate_all,specailStatus_all):
        totallist = "list%s"%len(specialName_all)
        if specailstatus == '1':
            finally_specailstatus = '未截止'
            totallist = [specialname,endtime,completepeople,shouldcompletepeople,completerate,finally_specailstatus]
            all_special_list.append(totallist)
        else:
            finally_specailstatus = '已截止'
            totallist = [specialname,endtime,completepeople,shouldcompletepeople,completerate,finally_specailstatus]
            all_special_list.append(totallist)

    return all_special_list



