import io
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
from xueanquanapi import *
 
cookies = 'ServerSide=https://guangdong.xueanquan.com/;UserID=6B0A87E07EB878EC437CABB6803CBC17'

root = Tk()
ver = "1.3.0"
title='安全教育平台助手 Debug'
root.title(title)
tmp = open("xueanquan.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
global tmpico
tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
root.iconphoto(False ,tmpico)
os.remove("xueanquan.ico")
#root.iconbitmap(".\\backup_user\du.ico")
winWidth = 345
winHeight = 310
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
root.resizable(0,0)
varnum = IntVar()
return_text=StringVar()

def get_scan_result_for_tk(EncodeSceneId):

    num = 1

    url = 'https://appapi.xueanquan.com/usercenter/api/v5/wx/scan-result?encodeSceneId={0}'.format(EncodeSceneId)

    headers = { 'Accept': '*//*',
                'Accept-Encoding': 'gzip',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'appapi.xueanquan.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
            }
        
    data = {' '}

    def checkstatus(num):
        res = requests.post(url=url, headers=headers, data=data)
        #print(res.text)
        global timer
        timer = threading.Timer(0.2,checkstatus)
        # 获取登陆状态
        statuscode = str(re.findall('"status":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
        # 判断登陆状态
        if statuscode == 'Error':
            return_text.set('扫码已过期，正在重新获取')
            # 重新调用获取函数
            loading_qrcode()
            return 0
        elif  statuscode == 'Success':
            # 当状态码为登陆成功时获取用户信息
            useridforcookie = str(re.findall('UserID=(.*?);', str(res.headers['Set-Cookie']))).replace("'",'').replace(']','').replace('[','')
            domainforcookie = str(re.findall('ServerSide=(.*?);', str(res.headers['Set-Cookie']))).replace("'",'').replace(']','').replace('[','').replace('%3A',':').replace("%2F",'/')
            cookies = 'ServerSide={0};UserID={1}'.format(domainforcookie, useridforcookie)
            userid,username,usertype,name,schoolname,grade,classname = get_scan_user_info(cookies)
            return_text.set('扫码成功 '+name+' 你好,我将在3秒内为你跳转至主页面')
            # 取消循环
            timer.cancel()
            return 0
        elif  statuscode == 'Wait':
            if num == 1:
                return_text.set('等待扫码')
                num = num + 1
            elif  num == 2:
                return_text.set('等待扫码.')
                num = num + 1
            elif  num == 3:
                return_text.set('等待扫码..')
                num = num + 1
            elif  num == 4:
                return_text.set('等待扫码...')
                num = 1
            else:
                return_text.set('等待扫码')
        else:
            return_text.set('未知状态\n'+ statuscode)

        timer = threading.Timer(0.2,lambda:checkstatus(num))
        timer.start()

    timer = threading.Timer(0.2,lambda:checkstatus(num))
    timer.start()



def loading_qrcode():
    qrcode_url,encodeid = get_login_qrcode()
    image_bytes = requests.get(qrcode_url).content
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    global tk_image
    tk_image = ImageTk.PhotoImage(pil_image)
    label_qrcode.config(image=tk_image)
    label_qrcode.image=tk_image
    get_scan_result_for_tk(encodeid)

lf_qrcode = tkinter.ttk.LabelFrame(root,text="二维码",width=110,height=110)
lf_qrcode.pack(anchor='center',pady=50)
label_qrcode = Label(lf_qrcode, bg='black')
label_qrcode.pack(fill=BOTH, expand='yes')
lb_status = Label(root, textvariable=return_text)
lb_status.pack(anchor='center')

loading_qrcode()

root.mainloop()