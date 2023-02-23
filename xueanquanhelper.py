# !! - pip install fake_useragent pillow lxml requests
import re
from tkinter import *
import tkinter.ttk
import os
import io
from PIL import Image, ImageTk
import tkinter.messagebox
import webbrowser
import requests
import sys
import subprocess
import base64
import time
from MissedYyang import png1
from lanmiemie import png
from lxml import etree
from xueanquanicon import img
import tkinter.filedialog
import ctypes
import random
#import threading
#import logging
from tkinter import scrolledtext
from fake_useragent import FakeUserAgent
import hashlib

root = Tk()
#root.attributes("-alpha", 0.8)
ver = "1.4.1"
title='安全教育平台助手 - 学生版 '+ver
root.title(title)
tmp = open("xueanquan.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
global tmpico
tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
root.iconphoto(False ,tmpico)
os.remove("xueanquan.ico")
#root.iconbitmap(".\\backup_user\du.ico")
winWidth = 700
winHeight = 350
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
root.resizable(0,0)
port = StringVar()

main_menu = Menu(root)
root.config (menu=main_menu)

class myStdout():	# 重定向类
    def __init__(self):
    	# 将其备份
        self.stdoutbak = sys.stdout		
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        t.insert('end', info)	# 在多行文本控件最后一行插入print信息
        t.update()	# 更新显示的文本，不加这句插入的信息无法显示
        t.see(tkinter.END)	# 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

def download(name, url, header={'Connection': 'keep-alive','Accept-Encoding': 'gzip, deflate, br','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}, interval=0.5):
    def MB(byte):
        return byte / 1024 / 1024
    #print(name)
    try:
        res = requests.get(url,stream=True,headers=header)
    except Exception as e:
        tkinter.messagebox.showerror(title='下载失败',message='连接到远程服务器失败，请再试一次')
        return 0
    try:
        file_size = int(res.headers['content-length'])  # 文件大小 Byte
    except Exception as e:
        tkinter.messagebox.showerror(title='下载失败',message='未知错误，请再试一次')
        return 0
    f = open(name, 'wb')
    down_size = 0  # 已下载字节数
    old_down_size = 0  # 上一次已下载字节数
    time_ = time.time()
    for chunk in res.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            down_size += len(chunk)
            if time.time() - time_ > interval:
                #rate = down_size / file_size * 100  # 进度  0.01%
                speed = (down_size - old_down_size) / interval  # 速率 0.01B/s
                
                old_down_size = down_size
                time_ = time.time()
                print_params = [MB(speed), MB(down_size), MB(file_size), down_size / file_size, (file_size - down_size) / speed]
                done = int(50 * down_size / file_size)
                #sys.stdout.write("\r[%s%s] %d%%" % ('>' * done, ' ' * (50 - done), 100 * down_size / file_size))
                #sys.stdout.flush()
                t.config(state=NORMAL)
                t.delete("2.0","end")
                t.insert("end", '\n'+'\r{:.1f}MB/s -已下载 {:.1f}MB，共 {:.1f}MB 已下载百分之:{:.2%} 还剩 {:.0f} 秒   '.format(*print_params))
                t.update()
                t.see(tkinter.END)
                t.delete("2.0","end")
                #print('\r{:.1f}MB/s -已下载 {:.1f}MB，共 {:.1f}MB 已下载百分之:{:.2%} 还剩 {:.0f} 秒   '.format(*print_params))
    f.close()
    t.config(state=DISABLED)

def login(username, password):
    '''
    登陆
    '''
    accesstoken = ''
    serverside = ''
    userid = ''
    name = ''
    plainUserId = ''
    url = 'https://appapi.xueanquan.com/usercenter/api/v1/account/PostLogin'
    headers = {'Host': 'appapi.xueanquan.com',
               'Content-Type': 'application/json',
               'Content-Length': '102',
               #'X-TrackingId':'4e1389ae-51e3-427d-962e-459ff40b44d0',
               'Connection': 'keep-alive',
               #'X-EquipmentId': '22CBB69F-D6E4-42F5-B615-F4297D54AE93',
               'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
               'Accept-Language': 'zh-Hans-HK;q=1',
               'Authorization': '',
               'Accept-Encoding': 'gzip, deflate, br'}

    json = {
        "Password": password,
        "EquipmentId": "22CBB69F-D6E4-42F5-B615-F4297D54AE93",
        "Username": username}

    res = requests.post(url=url, headers=headers, json=json)
    # print(res.text)
    data = re.findall('"data":(.*?),', res.text)[0]
    if data == 'null':
        pass
    else:
        # tip=findall("err_desc":"()", res.text)[0]
        userid = re.findall('"accessCookie":"(.*?)"', res.text)[0]
        serverside = re.findall('"webUrl":"(.*?)"', res.text)[0]
        name = re.findall('"nickName":"(.*?)"', res.text)[0]
        accesstoken = re.findall('"accessToken":"(.*?)"', res.text)[0]
        plainUserId = re.findall('"plainUserId":(.*?),', res.text)[0]
        # print(accesstoken, serverside, userid, name)
    return accesstoken, serverside, userid, name, plainUserId


def get_message(userid, accesstoken, plainUserId):
    '''
    获取假期安全提醒阅读
    '''
    title_all = []
    messageid_all = []
    url = 'https://guangdong.xueanquan.com/safeapph5/api/noticeService/getMyReceive?userId={0}&parentSortId=2&beginIndex=0&pageSize=20'.format(
        userid)
    # print(url)
    headers = {'Host': 'guangdong.xueanquan.com',
               'X-UserId': plainUserId,
               'Accept-Encoding': 'gzip, deflate, br',
               'X-TrackingId': '3eb4eae5-d97f-45e0-aedb-3d2c949d3424',
               'Connection': 'keep-alive',
               'X-EquipmentId': '22CBB69F-D6E4-42F5-B615-F4297D54AE93',
               'Accept': '*/*',
               'Accept-Language': 'zh-Hans-HK;q=1',
               'Authorization': 'Bearer ' + accesstoken,
               'X-Comefrom': '20227',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6'}
    # print(headers)
    res = requests.get(url=url, headers=headers)
    # print(res.text)
    res1 = res.text.replace('\n', '')
    message = re.findall('({.*?"messageID":.*?})', res1)
    # print(message)

    for m in message:
        if '"isRead": true,' in m:
            pass
        else:
            title = re.findall('"title": "(.*?)",', m)[0]
            messageid = re.findall('"messageID": (.*?),', m)[0]
            title_all.append(title)
            messageid_all.append(messageid)
    # print(title_all,messageid_all)
    return title_all, messageid_all


def do_message(accesstoken, userid, messageId, num):
    '''
    阅读提醒,messageId以实现自动取更换
    '''
    try:
        cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserID=' + userid
        Authorization = 'Bearer ' + accesstoken
        url = 'https://guangdong.xueanquan.com/safeapph5/api/noticeService/setRead?userId={0}&messageId={1}'.format(
            userid, messageId)
        # print(url)
        headers = {'Host': 'guangdong.xueanquan.com',
                   'X-TrackingId': 'f480c826-f766-4e14-afa7-52d0e2bf7443',
                   'Authorization': Authorization,
                   'X-Comefrom': '20227',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-Hans-HK;q=1',
                   'Accept': '*/*',
                   #'X-UserId':'61570657',
                   'Content-Length': '0',
                   #'X-EquipmentId':'22CBB69F-D6E4-42F5-B615-F4297D54AE93',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6'}
        res = requests.post(url=url, headers=headers)
        print(res.text)
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            do_message(userid, specialId, step, num)
        else:
            pass


def get_homework(userid, accesstoken):
    '''
    获取学期任务 and 专题任务
    学生账号，不分专题任务和学期任务接口，可怕
    '''
    title_all = []
    url_all = []
    cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserID=' + userid
    Authorization = 'Bearer ' + accesstoken
    url = 'https://applet.xueanquan.com/pt/guangdong/safeapph5/api/v1/homework/homeworklist'
    headers = {'Host': 'applet.xueanquan.com',
               'Origin': 'https://safeh5.xueanquan.com',
               'Accept-Encoding': 'gzip, deflate, br',
               'Cookie': cookies,
               'Connection': 'keep-alive',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
               'Authorization': Authorization,
               'Referer': 'https://safeh5.xueanquan.com/safeedu/homeworkList'}
    res = requests.get(url=url, headers=headers)
    # print(res.text)
    res1 = res.text.replace('\n', '').replace('  ', '')
    # print(res1)
    work_all = re.findall('("linkUrl":.*?),"publishDateTime"', res1)
    # print(work_all)
    # 这里安全➕专题都这里、下面运行需要想个办法，分开去do
    return work_all


def do_homework(courseid, gradeid, userid, num):
    '''
    学期安全任务
    '''
    try:
        print(courseid, gradeid)
        cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserID=' + userid
        # 下面全部新加、来源于无可奈何
        # 这是获取活动视频
        url2 = 'https://yyapi.xueanquan.com/guangdong/api/v1/StudentHomeWork/VideoInfoGet?courseId={}'.format(
            courseid)
        headers2 = {'Host': 'yyapi.xueanquan.com',
                    'Content-Type': 'application/json',
                    'Origin': 'https://guangdong.xueanquan.com',
                    'Cookie': cookies,
                    'Connection': 'keep-alive',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
                    'Referer': 'https://guangdong.xueanquan.com/html/platform/student/skilltrain.html?gid=485&li=696&externalUrl=https%3A%2F%2Fsafeh5.xueanquan.com%2Fsafeedu%2FhomeworkList&page_id=121',
                    'Accept-Language': 'zh-cn',
                    'Accept-Encoding': 'gzip, deflate, br'}
        res2 = requests.get(url=url2, headers=headers2)
        videoid = re.findall('"contentId": (.*?),', res2.text)
        workid = re.findall('"workId": (.*?),', res2.text)
        fid = re.findall('"fid": (.*?),', res2.text)
       # print('videoid: ',videoid)
        # print('workId: ',workid)
        # print('fid: ', fid)
        # print(res2.text)

        # 这是观看视频
        url1 = 'https://guangzhou.xueanquan.com/JiaTing/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=SkillCheckName&_session=rw'
        headers1 = {'Host': 'guangzhou.xueanquan.com',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://guangdong.xueanquan.com',
                    'Cookie': cookies,
                    'Content-Length': '38',
                    'Connection': 'keep-alive',
                    'Accept': 'application/json, text/javascript, */*',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
                    #'Referer': 'https://guangdong.xueanquan.com/html/platform/student/skilltrain.html?gid=485&li=544&externalUrl=https%3A%2F%2Fsafeh5.xueanquan.com%2Fsafeedu%2FhomeworkList&page_id=121',
                    'Accept-Language': 'zh-cn',
                    'Accept-Encoding': 'gzip, deflate, br'}
        data1 = 'videoid={}\r\ngradeid={}\r\ncourseid={}'.format(
            videoid[0], courseid, gradeid)
        # requests.options(url=url1, headers=headers1)
        # print(data1)
        res1 = requests.post(url=url1, headers=headers1, data=data1)
        print(res1.text, '\n')

        # 保存视频进度
        url3 = 'https://yyapi.xueanquan.com/guangdong/api/v1/StudentHomeWork/VideoPlayRecordSave?courseId={}&gradeId={}'.format(
            courseid, gradeid)
        headers3 = {'Host': 'yyapi.xueanquan.com',
                    'Content-Type': 'application/json',
                    'Origin': 'https://guangdong.xueanquan.com',
                    'Cookie': cookies,
                    'Content-Length': '0',
                    'Connection': 'keep-alive',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6)',
                    #'Referer': 'https://guangdong.xueanquan.com/html/platform/student/skilltrain.html?gid=485&li=696&externalUrl=https%3A%2F%2Fsafeh5.xueanquan.com%2Fsafeedu%2FhomeworkList&page_id=121',
                    'Accept-Language': 'zh-cn',
                    'Accept-Encoding': 'gzip, deflate, br'}
        res3 = requests.post(url=url3, headers=headers3)
        print(res3.text)

        # 答题
        url4 = 'https://yyapi.xueanquan.com/guangdong/api/v1/StudentHomeWork/HomeWorkSign'
        headers4 = {'Host': 'yyapi.xueanquan.com',
                    'Content-Type': 'application/json;charset=utf-8',
                    'Origin': 'https://guangdong.xueanquan.com',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cookie': cookies,
                    'Connection': 'keep-alive',
                    'Accept': '*/*',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
                    #'Referer': 'https://guangdong.xueanquan.com/html/platform/student/skilltrain.html?gid=485&li=696&externalUrl=https%3A%2F%2Fsafeh5.xueanquan.com%2Fsafeedu%2FhomeworkList&page_id=121',
                    'Content-Length': '213',
                    'Accept-Language': 'zh-cn'}
        json4 = {"testinfo": "已掌握技能",
                 "testResult": 1,
                 #"schoolId" : 332427225,
                 "workId": workid[0],
                 "fid": fid[0],
                 "testanswer": "0|0|0",
                 #"comefrom" : 20227,
                 "courseId": courseid,
                 #"cityCode" : 120023,
                 #"classroom" : 533964015,
                 "grade": 1,
                 "testMark": 100}
        res4 = requests.post(url=url4, headers=headers4, json=json4)
        print(res4.text)
        
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            doit_course(courseid, gradeid, cookies, num)
        else:
            pass


def get_special(url, userid):
    '''
    获取专题任务id信息
    '''
    try:
        print('正在获取安全专题信息..........')
        value1 = ''
        print('链接1:', url)
        # cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserI=' + userid
        headers = {'User-Agent': FakeUserAgent().random,
                   #'Cookie': cookies
                   }
        res = requests.get(url=url, headers=headers, allow_redirects=True)
        # res.encoding='utf-8'
        # print(res.text)
        value = re.findall("location.replace(.*?);", res.text)[0]
        # print(value)
        value1 = value.split("'")[1]

    except Exception as e:
        print(e)
        value1 = value.split('"')[1]
        
    finally:
        # print(value1)
        url1 = url.replace('index.html', value1)
        print('链接2:', url1)
        res1 = requests.get(url=url1, headers=headers)
        # print(res1.text)
        # data-specialId ="732"
        # 处理一下，避免出错
        res2 = res1.text.replace(' ', '')
        # print(res2)
        id_all = re.findall('data-specialId="(.*?)"', res2)[0]

    print('专题id:  ', id_all)
    return id_all

def do_special(userid, specialId, step, num):
    '''
    干活,完成专题任务
    '''
    try:
        cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserID=' + userid
        url = 'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/sign'
        headers = {'Host': 'huodongapi.xueanquan.com',
                   'Content-Type': 'application/json',
                   'Origin': 'https://huodong.xueanquan.com',
                   #'Accept-Encoding': 'gzip, deflate, br',
                   'Cookie': cookies,
                   'Connection': 'keep-alive',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'User-Agent': FakeUserAgent().random
                   }
        # json = {"specialId": specialId, "step": step}
        specialIdtest = int(specialId)
        #print (specialId)
        if specialIdtest != 0:           
            json = {"specialId": specialId, "step": step}
            # print (json)
            res = requests.post(url=url, headers=headers, json=json)
            print(res.text)
            time.sleep(0.5)
        else:
            t.insert('end', 'ERROR: 无效的 specialId \n出现错误 \n请登陆官网执行任务 \n', "tag_red")
            return False
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            do_special(userid, specialId, step, num)
        else:
            pass


def do_holiday(userid, schoolYear, semester, step):
    '''
    完成寒暑假任务专题
    '''
    
    try:
        url = 'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/holiday/sign'
        cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserID=' + userid
        headers = {'Host': 'huodongapi.xueanquan.com',
                   'Content-Type': 'application/json',
                   'Origin': 'https://huodong.xueanquan.com',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Cookie': cookies,
                   'Connection': 'keep-alive',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
                   #'Referer: https://huodong.xueanquan.com/summer2022/summer_one.html',
                   'Content-Length': '41',
                   'Accept-Language': 'zh-cn'}
        json = {
            "semester": semester,
            "step": step,
            "schoolYear": schoolYear}
        res = requests.post(url=url, headers=headers, json=json)
        print(res.text)
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            do_special(userid, specialId, step, num)
        else:
            num = 1
            pass

def main(username, password):

    num = 1
    error = 0
    #global t
    # 登陆账号，获取信息
    accesstoken, serverside, userid, name, plainUserId = login(
        username, password)
    # 获取安全提醒任务
    title_all, messageid_all = get_message(userid, accesstoken, plainUserId)
    # print(title_all,messageid_all)

    # 阅读安全短信提醒
    if len(title_all) != 0:
        for t in range(len(title_all)):
            print('YES-正在运行，安全阅读提醒：{}'.format(title_all[t]))
            messageId = messageid_all[t]
            do_message(accesstoken, userid, messageId, num)
    else:
        print('OK--假期安全提醒,已经全部完成的了，无需执行！！。')

    # 获取学期任务和专题任务
    work_all = get_homework(userid, accesstoken)
    # print(work_all)
    for w in work_all:
        # print(w)
        # print(re.findall('"linkUrl": "(.*?)"',w)[0])
        # 判断任务完成与否
        if 'workStatus": "Finished"' in w:
            # 已完成,无需处理
            title = re.findall('"title": "(.*?)",', w)[0]
            print('OK--{}===已经完成了。。'.format(title))
        elif '"workStatus": "Expired"' in w:
            # 活动已过期
            title = re.findall('"title": "(.*?)",', w)[0]
            #t.insert("end",'WARNING:{}===未完成，完成时间已过。。'.format(title) + '\n', "tag_yellow")
            print('WARNING:{}===未完成，完成时间已过。。'.format(title))
        else:
            # 未完成的任务
            # 判断任务的类型
            if '"subTitle": "安全学习",' in w:
                # 学期安全任务
                title = re.findall('"title": "(.*?)",', w)[0]
                # 学期安全任务
                # gid=485,gradeid
                # li=558,courseid
                gradeid = re.findall('gid=(.*?)&', w)[0]
                courseid = re.findall('&li=(.*?)"', w)[0]
                print('YES-正在运行---.完成安全学习任务:{}'.format(title))
                # print(gradeid,courseid)
                # 未进行测试___没有账号测试
                do_homework(courseid, gradeid, userid, num)

            else:
                # 安全专题任务
                title = re.findall('"title": "(.*?)",', w)[0]
                url = re.findall('"linkUrl": "(.*?)"', w)[0]

                print('YES-正在运行---完成专题学习任务:{}'.format(title))
                # print(url)

                if 'summer' in url:
                    schoolYear = re.findall('summer(.*?)/', url)[0]
                    # print(schoolYear)
                    # 暑假是，学期为2
                    semester = 2
                    do_holiday(userid, schoolYear, semester, step=1)
                    do_holiday(userid, schoolYear, semester, step=2)
                elif 'winter' in url:
                    schoolYear = re.findall('winter(.*?)/', url)[0]
                    semester = 1
                    do_holiday(userid, schoolYear, semester, step=1)
                    do_holiday(userid, schoolYear, semester, step=2)
                else:
                    # 获取id
                    # 完成专题任务

                    id_all = get_special(url, userid)
                    specialId = id_all
                    do_special(userid, specialId, step=1, num=num)
                    do_special(userid, specialId, step=2, num=num)



def startmain():
        mystd = myStdout()
        t.config(state=NORMAL)
        t.tag_config("tag_1", backgroun="yellow", foreground="red")
        t.tag_config("tag_3", foreground="green")
        tkinter.messagebox.showinfo(title='安全教育助手平台（学生版）', message="防沉迷助手提醒您：为了尽可能保障每个活动任务能够顺利完成，速度会慢点哦！")
        if len(inp1.get()) == 0 and len(inp2.get()) == 0: 
            tkinter.messagebox.showerror(title='错误', message="哦吼！！您似乎啥也没输入？，请再试一次")
            return 0
        if len(inp1.get()) == 0: 
            tkinter.messagebox.showerror(title='错误', message="哦吼！！您似乎没输入账户？，请再试一次")
            return 0
        if len(inp2.get()) == 0: 
            tkinter.messagebox.showerror(title='错误', message="哦吼！！您似乎没输入密码？，请再试一次")
            return 0
        username = inp1.get().replace("\n", "").replace("\x20", "")
        password = inp2.get().replace("\n", "").replace("\x20", "")
        root.title(username + ' ，正在获取此账号的信息-----')
        # 登陆账号，获取信息
        accesstoken, serverside, userid, name, plainUserId = login(
            username, password)
        # 判断是否登录成功
        if name != '':
            root.title(name + ' 欢迎您， 程序正在运行，请不要关闭此界面。。。。。。。。。。。')
            t.delete("2.0","end")
            t.insert("end", "\n")
            t.insert("end", "当前执行的用户为 " + name + "\n", "tag_1")
            #t.insert("end", "\n")
            main(username, password)
            #time.sleep(5)
            root.title(title)
            t.insert("end", name + " 该账号下的所有任务已完成 " + "\n", "tag_3")
            t.config(state=DISABLED)
            tkinter.messagebox.showinfo(title='提示', message="全部任务都完成啦！\n如恁不相信本助手的完成能力\n恁可以上账号后台观看记录")
            mystd.restoreStd()
            # sys.exit()
        else:
            t.config(state=DISABLED)
            tkinter.messagebox.showerror(title='提示', message="哦吼！！账号或密码输入错误，请再试一次")
            mystd.restoreStd()
            root.title(title)

def updataprogram():
    try:
        html = requests.get("https://file-fatdeadpanda.netlify.app/stuupdatalog")
    except:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败，请检查网络环境后再试')
        return 0
    url = 'https://file-fatdeadpanda.netlify.app/stuupdatalog'
    ver_url = 'https://file-fatdeadpanda.netlify.app/stuver'
    hashcheck_url = 'https://file-fatdeadpanda.netlify.app/hashcheck.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    a = requests.get(url, headers = header).text
    b = requests.get(ver_url, headers = header).text.replace("\n", "")
    c = requests.get(hashcheck_url, headers = header).text.replace("\n", "")
    if b > ver:
        y = tkinter.messagebox.askyesno(title='喵呜~~ 检测到新版本!!!',message='目前版本为 '+ver +'\n\n最新版本为 '+b +'\n\n'+a)
        if y == False:
            return 0
        Download_a1='https://xueanquan-fatdeadpanda.netlify.app/getprogram/latest-program.exe'
        #a2=requests.get(Download_a1,headers=header,stream=True)
        #with open("./version-"+b +".exe","wb+") as code:
        #    code.write(a2.content)
        path="./version-"+b +".exe"
        #t.config(state=NORMAL)
        #t.insert("end", "开始下载更新")
        try:
            download(path, Download_a1)
        except Exception as e:
            tkinter.messagebox.showerror(title='下载失败',message='连接到远程服务器失败，请再试一次')
            return 0
        #    tkinter.messagebox.showerror(title='下载失败',message='未知错误，请再试一次')
        #t.delete("2.0","end")
        #t.config(state=DISABLED)
        with open("./version-"+b +".exe","rb") as hashjiaoyan:
            bytes = hashjiaoyan.read() # read file as bytes
            readable_hash = hashlib.md5(bytes).hexdigest();
            hashjiaoyan.close()
            print(readable_hash)
            if c == str(readable_hash):
                tkinter.messagebox.showinfo(title='提示',message="下载完成\n\n请退出软件并运行 version-"+b +'.exe')
                return 0
            else:
                tkinter.messagebox.showerror(title='提示', message="下载失败\n\n原因:\n\nMD5 hash 校验不通过\n\n官网校验信息\n"+c + "\n\n本地校验信息\n" + str(readable_hash))
                os.remove("./version-"+b +".exe")
                
        #tkinter.messagebox.showinfo(title='提示',message="这只是测试版！！！！请尝试向开发者获取最新版本。。。")
    else:
        tkinter.messagebox.showinfo(title='提示', message="你已是最新版本")

main_menu.add_command (label="检查更新", command = updataprogram)

def about():
    top = Toplevel()
    top.title('关于')
    tmp = open("xueanquan.ico","wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    global tmpico
    tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
    top.iconphoto(False ,tmpico)
    os.remove("xueanquan.ico")
    winWidth = 700
    winHeight = 350
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    top.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    top.resizable(0, 0)
    CREATE_NO_WINDOW = 0x08000000

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'}
    about = 'https://file-fatdeadpanda.netlify.app/about.html'
    aboutme = requests.get(about, headers = header).text


    # txt12 = Text(top,width = 48,height = 10)
    # txt12.place(x=320,y=110)
    # scroll = tkinter.Scrollbar()
    # scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    # scroll.config(command=txt12.yview)
    # txt12.config(yscrollcommand=scroll.set)
    # txt12.pack()
    # txt12.configure(font='SimHei')
    txt12 = scrolledtext.ScrolledText(top, width=48, height=18, font=("SimHei", 10))
    txt12.place(x=320, y=110)
    txt12.insert(END, aboutme)
    txt12.configure(state='disabled')
    yyangtmp = open("tmp.png", "wb+")
    yyangtmp.write(base64.b64decode(png1))
    yyangtmp.close()
    width =119
    height =119
    mytmp = open("atmp.png", "wb+")
    mytmp.write(base64.b64decode(png))
    mytmp.close()
    global photo
    global photo2
    photo = PhotoImage(file="tmp.png")
    os.remove("tmp.png")
    photo2 = PhotoImage(file="atmp.png")
    os.remove("atmp.png")


    def webb():
         webb = webbrowser.open("https://github.com/lanmiemie")


    def webb1():
         webb = webbrowser.open("https://github.com/MissedYyang")
        
    Button(top,borderwidth = 2 ,image=photo ,relief="ridge",command=webb1).place(x=20, y=150)
    Button(top,borderwidth = 2 ,image=photo2 ,relief="ridge",command=webb).place(x=165, y=150)
    Button(top,borderwidth = 2,text = "★★★★★★★★★★★★" + title + "★★★★★★★★★★★★",relief="flat",state=DISABLED).place(x=120, y=20)
    Label(top, text="@ MissedYyang ↓",fg = 'green').place(x=25 ,y=120)
    Label(top, text="@ Lanmiemie ↓",fg = 'green').place(x=175 ,y=120)
    
main_menu.add_command (label="关于作者", command = about)

def in_start():
    root.title('开始检测网络连通性...')
    try:
        html = requests.get("https://guangdong.xueanquan.com")
    except:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败，请检查网络环境后再试')
        os._exit ()
    root.title('开始检测最新版本...')
    try:
        updataprogram()
    except:
        root.title(title)
        tkinter.messagebox.showerror(title='失败',message='无法检测最新版本')
        return 0
    root.title(title)
    

lf1 = tkinter.ttk.LabelFrame(root,text="登录信息")
lf1.place(x=8, y=8,width=330,height=150)
Label(lf1, text="学生账号").place(x=40,y=30)
inp1 = Entry(lf1, relief=GROOVE)
inp1.place(x=120, y=30)
Label(lf1, text="密码").place(x=50,y=80)
inp2 = Entry(lf1, relief=GROOVE,textvariable = port)
port.set('123456')
inp2.place(x=120, y=80)
tkinter.ttk.Button(root,text="登录", command = startmain).place(x=120,y=200)
t = Text(root, font=('Consolas', 8))	
t.place(x=340, y=20,width=355,height=325)
t.tag_config("tag_blue", foreground="blue")
t.tag_config("tag_red", foreground="red")
t.tag_config("tag_yellow", backgroun="green", foreground="yellow")
t.insert('end', 'LOG输出\n', "tag_blue")
in_start()
t.config(state=DISABLED)
root.mainloop()
