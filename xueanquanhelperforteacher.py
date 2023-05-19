# !! - pip install fake_useragent pillow lxml requests
import re
from tkinter import *
import tkinter.ttk
import os
from PIL import Image, ImageTk
import tkinter.messagebox
import webbrowser
import requests
import sys
import base64
import time
from MissedYyang import png1
from lanmiemie import png
from lxml import etree
from xueanquanicon import img
import tkinter.filedialog
from tkinter import scrolledtext
from fake_useragent import FakeUserAgent
import hashlib
from xueanquanapi import get_schoolid, get_studentlist, login, get_students, get_students_xlsx, get_message, get_homework, get_special 

root = Tk()
#root.attributes("-alpha", 0.8)
ver = "1.3.0"
title='安全教育平台助手 - 教师版 '+ver
root.title(title)
tmp = open("xueanquan.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
global tmpico
tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
root.iconphoto(False ,tmpico)
os.remove("xueanquan.ico")
#root.iconbitmap(".\\backup_user\du.ico")
winWidth = 344
winHeight = 310
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
root.resizable(0,0)
port = StringVar()

errorcodehas = 0
pointcode = 0
passwordcodetrue = 0
student_all = 0
teacher_cookies = 0
teacher_name = 0
num = 0
classroomname = 0

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
        root.update()
        t.see(tkinter.END)	# 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

def back_window_size():
    winWidth = 344
    winHeight = 310
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    root.resizable(0,0)

def download(name, url, cookies, header={'Connection': 'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}, interval=0.5):
    def MB(byte):
        return byte / 1024 / 1024
    #print(name)
    if len(cookies) == 0:
        try:
            res = requests.get(url,stream=True,headers=header)
        except Exception as e:
            tkinter.messagebox.showerror(title='下载失败',message='连接到远程服务器失败，请再试一次')
            return 0
    else:
        headera = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Connection': 'keep-alive',
                   #'Content-Length': '83',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': cookies,
                   'Host': 'guangzhou.xueanquan.com',
                   'Origin': 'https://guangzhou.xueanquan.com',
                   'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
                   #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                   'sec-ch-ua-mobile': '?0',
                   'sec-ch-ua-platform': 'Windows',
                   'Sec-Fetch-Dest': 'document',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Site': 'same-origin',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'
                   }
        try:
            res = requests.get(url,headers=headera)
        except Exception as e:
            tkinter.messagebox.showerror(title='下载失败',message='连接到远程服务器失败，请再试一次')
            return 0
    try:
        file_size = int(res.headers['content-length'])  # 文件大小 Byte
    except Exception as e:
        tkinter.messagebox.showerror(title='下载失败',message='无法获取文件大小，请再试一次')
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
                global print_params
                print_params = [MB(speed), MB(down_size), MB(file_size), down_size / file_size, (file_size - down_size) / speed]
                done = int(50 * down_size / file_size)
                #sys.stdout.write("\r[%s%s] %d%%" % ('>' * done, ' ' * (50 - done), 100 * down_size / file_size))
                #sys.stdout.flush()
                t.config(state=NORMAL)
                t.delete("1.0","end")
                t.insert("end", '\n'+'\r{:.1f}MB/s -已下载 {:.1f}MB，共 {:.1f}MB 已下载百分之:{:.2%} 还剩 {:.0f} 秒   '.format(*print_params))
                t.update()
                t.see(tkinter.END)
                t.delete("1.0","end")
                #print('\r{:.1f}MB/s -已下载 {:.1f}MB，共 {:.1f}MB 已下载百分之:{:.2%} 还剩 {:.0f} 秒   '.format(*print_params))
    f.close()
    t.config(state=DISABLED)

def log_out():
    global errorcodehas
    global passwordcodetrue
    global pointcode
    global student_all
    global teacher_cookies
    global teacher_name
    global num
    global classroomname
    
    errorcodehas = 0
    pointcode = 0
    passwordcodetrue = 0
    student_all = 0
    teacher_cookies = 0
    teacher_name = 0
    num = 0
    classroomname = 0

    reset_allstudents_password_button.place_forget()
    logoutbutton.place_forget()
    do_students_work_button.place_forget()
    showteacherinfo.place_forget()
    download_students_xlsx_button.place_forget()
    t.config(state=NORMAL)
    t.delete("1.0","end")
    tree1.delete(*tree1.get_children())
    lf_for_students.place_forget()
    lf_for_text.place_forget()
    t.config(state=DISABLED)
    back_window_size()
    lf1.place(x=8, y=8,width=330,height=150)
    loginbutton.place(x=120,y=200)
    root.title(title)
    
def reset_passward(cookie, studentid, num):
    '''
    重置密码，避免学生密码不是原始密码
    '''
    try:
        url = 'https://guangzhou.xueanquan.com/eduadmin/ClassManagement/StudentPassWordReset?studentid={}'.format(
            studentid)
        # print(url)
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   #'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cache-Control': 'no-cache',
                   'Connection': 'keep-alive',
                   'Content-Length': '0',
                   'Cookie': cookie,  # 此处cookies为教师账号cookies
                   'Host': 'guangzhou.xueanquan.com',
                   'Origin': 'https://guangzhou.xueanquan.com',
                   'Pragma': 'no-cache',
                   'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
                   'Sec-Fetch-Dest': 'empty',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Site': 'same-origin',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}

        param = {'studentid': studentid}
        res = requests.post(url=url, headers=headers, params=param)
        # print(res.text)
        #statuscode = re.findall('"statusCode":"(.*?)"', res.text)[0]
        message = re.findall('"message":"(.*?)"', res.text)[0]
        if str('"statusCode":"200"') in res.text:
            t.insert('end', 'YES: '+ message + '\n', "tag_green")
        else:
            t.insert('end', 'ERROR: '+ message + '\n', "tag_red")
        # 提示重置密码成功
        #print(message)
    except Exception as e:
        print(e)
        if num < 4:
            print('Tip:  第{0}次重试，事不过三！'.format(num))
            num = num + 1
            reset_passward(cookie, studentid, num)
        else:
            pass

def do_message(accesstoken, userid, messageId, TitleText, num):
    '''
    阅读提醒,messageId以实现自动取更换
    '''
    global errorcodehas
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
        #print(res.text)
        if str('"success": true') in res.text:
            t.insert('end', 'OK-- ' + str(TitleText) +' 已完成！！' +' \n', "tag_green")
        else:
            t.insert('end', 'ERROR-- ' + str(TitleText) +' 无法完成该任务' +' \n', "tag_red")
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            do_message(accesstoken, userid, messageId, TitleText, num)
        else:
            errorcodehas = errorcodehas + 1
            pass

def do_homework(courseid, gradeid, userid, num):
    '''
    学期安全任务
    '''
    global errorcodehas
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
            do_homework(courseid, gradeid, cookies, num)
        else:
            errorcodehas = errorcodehas + 1
            pass

def do_special(userid, specialId, sparespecialId, step, num):
    '''
    干活,完成专题任务
    '''
    global errorcodehas
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
        #specialIdtest = str(specialId)
        #print(step)
        #print (specialIdtest)
        if str(specialId) == '0':
            t.insert('end', 'ERROR: 无效的 specialId \n出现错误 \n', "tag_red")
            t.insert('end', 'WARNING: 正在尝试使用备用ID \n', "tag_yellow")
            json = {"specialId": sparespecialId, "step": step}
                # print (json)
            res = requests.post(url=url, headers=headers, json=json)
            if str('"httpCode":200') in res.text:
                t.insert('end', 'YES: 已完成步骤 '+str(step) +' \n', "tag_green")
            elif  str('"httpCode":0') in res.text:
                t.insert('end', 'WARNING:: 您已完成步骤 '+str(step) +' \n无需重复提交\n', "tag_yellow")
            else:
                t.insert('end', 'ERROR: 无法完成当前任务，您可尝试更新到最新版本或将以下日志发给 Archerfish 本Fish将在1周内或更久解决问题\n邮箱为 : Archerfish1114@163.com\n' , "tag_red")
                print(res.text)
                if str(step) == '1':
                    errorcodehas = errorcodehas+1
                    return False
                else:
                    return False
        else:
            json = {"specialId": specialId, "step": step}
            # print (json)
            res = requests.post(url=url, headers=headers, json=json)
            print(res.text)
            time.sleep(0.5)
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            do_special(userid, specialId, step, num)
        else:
            errorcodehas = errorcodehas+1
            pass

def do_holiday(userid, schoolYear, semester, step):
    '''
    完成寒暑假任务专题
    '''
    global errorcodehas
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
        #print(res.text)
        if str('"httpCode":200') in res.text:
            t.insert('end', 'YES: 已完成步骤 '+str(step) +' \n', "tag_green")
        elif  str('"httpCode":0') in res.text:
            t.insert('end', 'WARNING:: 您已完成步骤 '+str(step) +' \n无需重复提交\n', "tag_yellow")
        else:
            t.insert('end', 'ERROR: 无法完成当前任务，您可尝试更新到最新版本或将以下日志发给 Archerfish 本Fish将在1周内或更久解决问题\n邮箱为 : Archerfish1114@163.com \n', "tag_red")
            print(res.text)
    except Exception as e:
        print(e)
        if num < 4:
            t.insert('end', 'ERROR:  第{0}次重试，事不过三！'.format(num), "tag_red")
            num = num + 1
            do_holiday(userid, schoolYear, semester, step)
        else:
            errorcodehas = errorcodehas+1
            pass

def main(username, password):
    num = 1
    global errorcodehas
    #global t
    # 登陆账号，获取信息
    accesstoken, serverside, userid, name, plainUserId, studentorteacher, tip, classroomname, schoolname = login(
        username, password)
    # 获取安全提醒任务
    title_all, messageid_all = get_message(userid, accesstoken, plainUserId)
    # print(title_all,messageid_all)

    # 阅读安全短信提醒
    if len(title_all) != 0:
        for t in range(len(title_all)):
            print('YES-正在运行，安全阅读提醒：{}'.format(title_all[t]))
            #print(str(title_all[t]))
            TitleText = title_all[t]
            messageId = messageid_all[t]
            do_message(accesstoken, userid, messageId, TitleText, num)
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

                    id_all,getsparesdtext = get_special(url, userid)
                    specialId = id_all
                    sparespecialId = getsparesdtext
                    do_special(userid, specialId, sparespecialId, step=1, num=num)
                    do_special(userid, specialId, sparespecialId, step=2, num=num)

def do_students_work(student_all, teacher_cookies, num, teacher_name):
    yes_or_no = tkinter.messagebox.askokcancel('你需要了解的事','使用该功能会将所有学生账号密码修改为默认密码\n您是否继续进行该操作?')
    if yes_or_no == False:
        return 0
    global errorcodehas
    students_len = len(student_all)
    do_students_num = 0
    mystd = myStdout()
    do_students_work_button['state'] = DISABLED
    reset_allstudents_password_button['state'] = DISABLED
    logoutbutton['state'] = DISABLED
    t.config(state=NORMAL)
    t.delete("1.0","end")
    t.insert("end", "开始检测网络连通性..."+ "\n", "tag_3")
    try:
        html = requests.get("https://guangdong.xueanquan.com")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败，请检查网络环境后再试')
        t.delete("1.0","end")
        return 0
    for studen in student_all:
        # 获取学生名字，学生ID
        do_students_num = do_students_num + 1
        student_name = studen.split('/')[1]
        student_id = studen.split('/')[0]
        #students_label = Label(root, text='该账号有 '+str(students_len)+' 个学生, 正在执行第 ' + str(do_students_num) + ' 个')
        #students_label.place(x=90,y=220)
        t.insert("end", "\n")
        print('该账号有 '+str(students_len)+' 个学生, 正在执行第 ' + str(do_students_num) + ' 个')
        t.insert("end", '正在运行,账号：{}-----'.format(student_name) + "\n", "tag_1")
        print('正在运行,重置学生密码-----')
        reset_passward(teacher_cookies, student_id, num)
        #t.insert("end", "\n")
        main(username=student_name, password="Aa6666"+student_name)
        #time.sleep(5)
    if errorcodehas == 0:
        t.insert("end", str(teacher_name) + " 该老师账号下的所有任务已完成 " + "\n", "tag_3")
        t.config(state=DISABLED)
        tkinter.messagebox.showinfo(title='提示', message="全部任务都完成啦！\n如恁不相信本助手的完成能力\n恁可以上账号后台观看记录")
        #loginbutton.place(x=120,y=200)
        mystd.restoreStd()
    else:
        t.insert("end", teacher_name + " 该账号有 " +str(errorcodehas) + ' 个任务未完成'+ "\n", "tag_red")
        tkinter.messagebox.showerror(title='提示', message='教师 ' + teacher_name + " 有 " +str(errorcodehas) + ' 个任务未完成'+ "\n")
        errorcodehas = 0
        t.config(state=DISABLED)
        mystd.restoreStd()
    do_students_work_button['state'] = NORMAL
    reset_allstudents_password_button['state'] = NORMAL
    logoutbutton['state'] = NORMAL
    root.title(title)

def reset_allstudents_password(student_all, teacher_cookies, num, teacher_name):
    yes_or_no = tkinter.messagebox.askokcancel('你需要了解的事','使用该功能会将所有学生账号密码修改为默认密码\n该操作将不可逆\n您是否继续进行该操作?')
    if yes_or_no == False:
        return 0
    global errorcodehas
    #print(len(student_all))
    students_len = len(student_all)
    #reset_allstudents_password_button.place_forget()
    #logoutbutton.place_forget()
    #students_label = Label(root, text='该账号有 '+str(students_len)+' 个学生')
    #students_label.place(x=90,y=220)
    #do_students_num = 0
    mystd = myStdout()
    do_students_work_button['state'] = DISABLED
    reset_allstudents_password_button['state'] = DISABLED
    logoutbutton['state'] = DISABLED
    t.config(state=NORMAL)
    t.delete("1.0","end")
    t.insert("end", "开始检测网络连通性..."+ "\n", "tag_3")
    reset_students_password_num = 0
    for studen in student_all:
        reset_students_password_num = reset_students_password_num + 1
        student_name = studen.split('/')[1]
        student_id = studen.split('/')[0]
        #students_label = Label(root, text='该账号有 '+str(students_len)+' 个学生, 正在重置第 ' + str(reset_students_password_num) + ' 个')
        #students_label.place(x=90,y=220)
        t.insert("end", "\n")
        #t.insert("end", '正在重置密码,账号：{}-----'.format(student_name) + "\n", "tag_1")
        print('该账号有 '+str(students_len)+' 个学生, 正在重置第 ' + str(reset_students_password_num) + ' 个')
        print('正在重置密码,账号：{}-----'.format(student_name) + "\n")
        reset_passward(teacher_cookies, student_id, num)
        #t.insert("end", "\n")
        #main(username=student_name, password="Aa6666"+student_name)
        #time.sleep(5)
    if errorcodehas == 0:
        t.insert("end", str(teacher_name) + " 该老师账号下的所有学生密码已重置成功 " + "\n", "tag_3")
        t.config(state=DISABLED)
        #students_label.place_forget()
        tkinter.messagebox.showinfo(title='提示', message="该老师账号下的所有学生密码已重置成功\n原始密码为\nAa6666+Username (学生账号)")
        #loginbutton.place(x=120,y=200)
        mystd.restoreStd()
    else:
        t.insert("end", teacher_name + " 该账号有 " +str(errorcodehas) + ' 个任务未完成'+ "\n", "tag_red")
        tkinter.messagebox.showerror(title='提示', message='教师 ' + teacher_name + " 有 " +str(errorcodehas) + ' 个任务未完成'+ "\n")
        errorcodehas = 0
        t.config(state=DISABLED)
        mystd.restoreStd()
    do_students_work_button['state'] = NORMAL
    reset_allstudents_password_button['state'] = NORMAL
    logoutbutton['state'] = NORMAL
    #students_label.place_forget()
    root.update()
    root.title(title)

def startmain():
        mystd = myStdout()
        t.config(state=NORMAL)
        t.tag_config("tag_1", backgroun="yellow", foreground="red")
        t.tag_config("tag_3", foreground="green")
        global errorcodehas
        global teacher_cookies
        global student_all
        global teacher_name
        global classroomname
        #tkinter.messagebox.showinfo(title='安全教育助手平台（学生版）', message="防沉迷助手提醒您：为了尽可能保障每个活动任务能够顺利完成，速度会慢点哦！")
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
        t.delete("1.0","end")
        #t.insert("end", "\n")
        t.insert("end", "开始检测网络连通性..."+ "\n", "tag_3")
        try:
            html = requests.get("https://guangdong.xueanquan.com")
        except Exception as e:
            tkinter.messagebox.showerror(title='失败',message='网络连接失败，请检查网络环境后再试')
            t.delete("1.0","end")
            return 0
        root.title(username + ' ，正在获取此账号的信息-----')
        # 登陆账号，获取信息
        accesstoken, serverside, userid, name, plainUserId, studentorteacher, tip, classroomname, schoolname = login(
            username, password)
        # 判断是否登录成功
        if name != '':
            if studentorteacher == '"班主任"':
                #root.title('尊敬的 ' + name + ' 老师 欢迎您!!!!!')
                root.title(title)
                #t.delete("1.0","end")
                #t.insert("end", "\n")
                loginbutton.place_forget()
                lf1.place_forget()
                t.insert("end", "正在获取该账号的信息-----" + "\n", "tag_1")
                teacher_cookies = 'ServerSide={0};UserID={1}'.format(serverside, userid)
                teacher_name = name
                num = 1
                winWidth = 1100
                winHeight = 350
                screenWidth = root.winfo_screenwidth()
                screenHeight = root.winfo_screenheight()
                x = int((screenWidth - winWidth) / 2)
                y = int((screenHeight - winHeight) / 2)
                root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
                student_all = get_students(teacher_cookies)
                showteacherinfo.place(x=8, y=8,width=330,height=150)
                Label(showteacherinfo, text='教师姓名: '+str(teacher_name)).place(x=40,y=10)
                Label(showteacherinfo, text='所在学校: '+str(schoolname)).place(x=40,y=35)
                Label(showteacherinfo, text='所在班级: '+str(classroomname)).place(x=40,y=60)
                Label(showteacherinfo, text='学生总数: '+str(len(student_all))).place(x=40,y=85)
                reset_allstudents_password_button.place(x=30,y=180)
                do_students_work_button.place(x=30,y=210)
                download_students_xlsx_button.place(x=30,y=240)
                lf_for_students.place(x=340, y=8,width=403,height=340)
                lf_for_text.place(x=745, y=8,width=353,height=340)
                logoutbutton.place(x=230,y=210)
                Schoolidtext, Gradeidtext, Classroomidtext, Semesteridtext, UserTypeidtext, OrderColumnidtext = get_schoolid(teacher_cookies)
                get_all_list = get_studentlist(teacher_cookies, Schoolidtext, Gradeidtext, Classroomidtext, Semesteridtext, UserTypeidtext, OrderColumnidtext)
                for all_list in get_all_list:
                    tree1.insert('', END, values=all_list)
                #t.insert("end", name + " 该账号下的所有任务已完成 " + "\n", "tag_3")
                #t.config(state=DISABLED)
                #tkinter.messagebox.showinfo(title='提示', message="全部任务都完成啦！\n如恁不相信本助手的完成能力\n恁可以上账号后台观看记录")
                tree1.bind('<ButtonRelease-1>', adbc)
                t.insert("end", "获取完毕" + "\n", "tag_1")
                mystd.restoreStd()
                # sys.exit()
            else:
                t.delete("1.0","end")
                t.config(state=DISABLED)
                tkinter.messagebox.showinfo(title='提示', message="你好 " + name +" 同学!\n\n您输入的不是教师账号,请核对后再试!!!")
                mystd.restoreStd()
                root.title(title)
                pass
        else:
            t.delete("1.0","end")
            t.config(state=DISABLED)
            tkinter.messagebox.showerror(title='无法登录', message=str(tip))
            mystd.restoreStd()
            root.title(title)

def get_treeview_students_information():
    treeview_info = Toplevel()
    treeview_info.title('提示')
    tmp = open("xueanquan.ico","wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    global tmpico
    tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
    treeview_info.iconphoto(False ,tmpico)
    os.remove("xueanquan.ico")
    winWidth = 500
    winHeight = 500
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    treeview_info.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    treeview_info.resizable(0, 0)
    id_list = tree1.selection()
    for item in id_list:
        name,id1,classroomname1,studentid1 = tree1.item(item)["values"]
        show_name = Label()


def updataprogram():
    try:
        html = requests.get("https://xueanquan-fatdeadpanda.netlify.app/getprogram/teaupdatalog")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败，请检查网络环境后再试')
        return 0
    url = 'https://xueanquan-fatdeadpanda.netlify.app/getprogram/teaupdatalog'
    ver_url = 'https://xueanquan-fatdeadpanda.netlify.app/getprogram/teaver'
    hashcheck_url = 'https://xueanquan-fatdeadpanda.netlify.app/getprogram/hashcheckforteacher'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    a = requests.get(url, headers = header).text
    b = requests.get(ver_url, headers = header).text.replace("\n", "")
    c = requests.get(hashcheck_url, headers = header).text.replace("\n", "")
    if b > ver:
        y = tkinter.messagebox.askyesno(title='喵呜~~ 检测到新版本!!!',message='目前版本为 '+ver +'\n\n最新版本为 '+b +'\n\n'+a)
        if y == False:
            return 0
        Download_a1='https://xueanquan-fatdeadpanda.netlify.app/getprogram/xueanquanhelperforteacher.exe'
        #a2=requests.get(Download_a1,headers=header,stream=True)
        #with open("./version-"+b +".exe","wb+") as code:
        #    code.write(a2.content)
        path="./version-"+b +".exe"
        #t.config(state=NORMAL)
        #t.insert("end", "开始下载更新")
        cookies = ''
        try:
            download(path, Download_a1,cookies)
        except Exception as e:
            root.withdraw()
            tkinter.messagebox.showerror(title='下载失败',message='连接到远程服务器失败，请再试一次')
            return 0
        #    tkinter.messagebox.showerror(title='下载失败',message='未知错误，请再试一次')
        #t.delete("1.0","end")
        #t.config(state=DISABLED)
        with open("./version-"+b +".exe","rb") as hashjiaoyan:
            bytes = hashjiaoyan.read()
            readable_hash = hashlib.sha256(bytes).hexdigest();
            hashjiaoyan.close()
            print(readable_hash)
            if c == str(readable_hash):
                tkinter.messagebox.showinfo(title='提示',message="下载完成\n\n请退出软件并运行 "+ "./version-"+b +".exe" +"\n\n文件路径为\n\n"+ os.path.abspath("./version-"+b +".exe"))
                os._exit(0)
                #return 0            
            else:
                tkinter.messagebox.showerror(title='提示', message="下载失败\n\n原因:\n\nSha256 校验不通过\n\n官网校验信息\n"+c + "\n\n本地校验信息\n" + str(readable_hash))
                os.remove("./version-"+b +".exe")
        #tkinter.messagebox.showinfo(title='提示',message="这只是测试版！！！！请尝试向开发者获取最新版本。。。")
    else:
        tkinter.messagebox.showinfo(title='提示', message="你已是最新版本")

main_menu.add_command (label="检查更新", command = updataprogram)

def download_xlsx(cookies,classroomname):
    yes_or_no = tkinter.messagebox.askyesno(title='提示',message='确定要下载学生账号表格吗?')
    if yes_or_no == False:
        return 0
    gettime = time.strftime('%Y-%m-%d--%H-%M-%S',time.localtime())
    path="./"+str(classroomname)+"-学生信息-"+str(gettime) +".xls"
    xlsxurl = get_students_xlsx(teacher_cookies)
    try:
        download(path, xlsxurl ,cookies)
    except Exception as e:
        root.withdraw()
        tkinter.messagebox.showerror(title='下载失败',message='连接到远程服务器失败，请再试一次')
        return 0
    try:
        f =open(path)
        f.close()
    except FileNotFoundError:
        tkinter.messagebox.showerror(title='下载失败',message='File is not found.')
        #print "File is not found."
        return 0
    openfile = tkinter.messagebox.askyesno(title='提示',message='下载完成\n\n文件路径为\n'+os.path.abspath(path)+'\n\n或者你可以按 "确定" 来打开表格')
    if openfile == False:
        return 0
    os.startfile(os.path.abspath(path))  
    
def about():
    try:
        html = requests.get("https://xueanquan-fatdeadpanda.netlify.app/getprogram/about")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败，请检查网络环境后再试')
        return 0
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
    #CREATE_NO_WINDOW = 0x08000000

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'}
    about = 'https://xueanquan-fatdeadpanda.netlify.app/getprogram/about'
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

    def caidan():
        topunknown = Toplevel()
        #root.attributes("-alpha", 0.8)
        #ver = "1.4.4"
        title="Unknown Program ???"
        topunknown.title(title)
        tmp = open("xueanquan.ico","wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        global tmpico
        tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
        topunknown.iconphoto(False ,tmpico)
        os.remove("xueanquan.ico")
        #root.iconbitmap(".\\backup_user\du.ico")
        winWidth = 250
        winHeight = 100
        screenWidth = topunknown.winfo_screenwidth()
        screenHeight = topunknown.winfo_screenheight()
        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        topunknown.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        topunknown.resizable(0,0)
        Label(topunknown, text="FOOD:").place(x=10,y=30)
        inp1 = Entry(topunknown, relief=GROOVE)
        inp1.place(x=80,y=30)
        

        def gettext():
            global pointcode
            global passwordcodetrue
            getpassword = inp1.get().replace("\n", "").replace("\x20", "")
            code = 'TOMATO'
            if code == getpassword:
                passwordcodetrue = passwordcodetrue + 1
                if passwordcodetrue == 4:
                    tkinter.messagebox.showinfo(title='Alesha', message="Who are You :(")
                    tkinter.messagebox.showinfo(title='Alesha', message="Do you already know my plan? :((")
                    tkinter.messagebox.showinfo(title='Alesha', message="Anyone who knows about this plan will not end well :(((")
                    tkinter.messagebox.showinfo(title='Alesha', message="So.... :((((")
                    tkinter.messagebox.showwarning(title='Alesha', message="I WILL EXIT THIS PROGRAM AND RESTART YOUR COMPUTER :)")
                    tkinter.messagebox.showwarning(title='Alesha', message="SO SAY GOODBAY :)")
                    os._exit(0)
                else:
                    tkinter.messagebox.showinfo(title='Alesha', message="There is nothing here :)")
            else:
                pointcode = pointcode + 1
                if pointcode == 4:
                    tkinter.messagebox.showinfo(title='Unknown', message="The tOMatoes And poTatOes are indeed delicious :)")
                    pointcode = 0
                else:
                    tkinter.messagebox.showerror(title='Error', message="You don't have access to the core :(")
            #print(str(getpassword))
            #topunknown.attributes("-toolwindow", 1)
            #top.wm_attributes('-topmost','false')
            #topunknown.wm_attributes('-topmost','true')
            
        tkinter.ttk.Button(topunknown,text="?!", command = gettext).place(x=80,y=70)


    caidanbotton = Button(top,borderwidth = 2,text = "★★★★★★★★★★★★" + title + "★★★★★★★★★★★★",relief="ridge",state=DISABLED,command=caidan)
    caidanbotton.place(x=150, y=20)
    #top.attributes("-toolwindow", 1)
    #top.wm_attributes('-topmost','true')

    def webb1():
         webb = webbrowser.open("https://github.com/MissedYyang")
         caidanbotton['state'] = NORMAL

    def webb():
         webb = webbrowser.open("https://github.com/lanmiemie")
         caidanbotton['state'] = NORMAL
        
    Button(top,borderwidth = 2 ,image=photo ,relief="ridge",command=webb1).place(x=20, y=150)
    Button(top,borderwidth = 2 ,image=photo2 ,relief="ridge",command=webb).place(x=165, y=150)
    
    Label(top, text="@ MissedYyang ↓",fg = 'green').place(x=25 ,y=120)
    Label(top, text="@ Archerfish ↓",fg = 'green').place(x=175 ,y=120)
    
main_menu.add_command (label="关于作者", command = about)

def in_start():
    root.title('开始检测网络连通性...')
    try:
        html = requests.get("https://guangdong.xueanquan.com")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败\n您可以通过以下操作来帮助您排除网络问题\n\n1. 如果您打开了代理（Clash,Socks), 请将它关闭.\n2.检查网络是否通畅.\n3.检查路由器等设施是否正确连接到互联网.\n4.您压根没有连接到互联网.')
        os._exit(0)
    root.title('开始检测最新版本...')
    try:
        updataprogram()
    except Exception as e:
        root.title(title)
        tkinter.messagebox.showerror(title='失败',message='无法检测最新版本')
        return 0
    root.title(title)
    

lf1 = tkinter.ttk.LabelFrame(root,text="登录信息")
showteacherinfo = tkinter.ttk.LabelFrame(root,text="教师信息")
lf_for_students = tkinter.ttk.LabelFrame(root,text="学生信息")
lf_for_text = tkinter.ttk.LabelFrame(root,text="LOG输出")
tree1 = tkinter.ttk.Treeview(lf_for_students, columns=('xm', 'zh', 'stuclass', 'stuid'),show='headings') 
tree1.heading('xm', text='姓名')
tree1.heading('zh', text='账号')
tree1.heading('stuclass', text='所在班级')
tree1.heading('stuid', text='学生ID')
tree1.column('xm', width=60,anchor='center')
tree1.column('zh', width=130,anchor='center')
tree1.column('stuclass', width=80,anchor='center')
tree1.column('stuid', width=90,anchor='center')
tree1.pack(fill=BOTH, expand='yes')
lf1.place(x=8, y=8,width=330,height=150)
Label(lf1, text="教师账号").place(x=40,y=30)
inp1 = Entry(lf1, relief=GROOVE)
inp1.place(x=120, y=30)
Label(lf1, text="密码").place(x=50,y=80)
inp2 = Entry(lf1, relief=GROOVE,textvariable = port)
port.set('Aa6666')
inp2.place(x=120, y=80)
loginbutton = tkinter.ttk.Button(root,text="登录", command = startmain)
loginbutton.place(x=125,y=200)
logoutbutton = tkinter.ttk.Button(root,text="注销", command = log_out)
do_students_work_button = tkinter.ttk.Button(root,text="完成该账号下所有学生任务", command = lambda:do_students_work(student_all, teacher_cookies, num, teacher_name))
download_students_xlsx_button = tkinter.ttk.Button(root,text="下载所有学生账号", command = lambda:download_xlsx(teacher_cookies,classroomname))
reset_allstudents_password_button = tkinter.ttk.Button(root,text="重置该账号下所有学生密码", command = lambda:reset_allstudents_password(student_all, teacher_cookies, num, teacher_name))
t = scrolledtext.ScrolledText(lf_for_text, font=('Consolas', 8))	
t.pack(fill=BOTH, expand='yes')
t.tag_config("tag_blue", foreground="blue")
t.tag_config("tag_red", foreground="red")
t.tag_config("tag_yellow", backgroun="yellow", foreground="red")
t.tag_config("tag_green", foreground="green")
#lf_for_text.place(relx = 1,anchor = NE,width=355,height=350)
#t.insert('end', 'LOG输出\n', "tag_blue")

def callback1(event=None):
    global root
    t.event_generate('<<Copy>>')
    
menufortext = Menu(root,
            tearoff=False,
            #bg="black",
            )
menufortext.add_command(label="复制", command=callback1)

def popup(event):
    menufortext.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单
t.bind("<Button-3>", popup)  

#in_start()
t.config(state=DISABLED)

#root.wm_attributes('-topmost','true')
root.mainloop()