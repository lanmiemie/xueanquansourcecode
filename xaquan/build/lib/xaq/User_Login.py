import threading
import webbrowser
import requests
from lxml import etree
import re
from fake_useragent import FakeUserAgent
import datetime

def password_login(username, password):
    '''
    登陆\n
    accesstoken (访问令牌), serverside (地区域名), userid (用户ID), name (姓名), plainUserId, studentorteacher (判断是学生还是教师), tip (登陆失败时获取返回提示), classroomname (班别), schoolname (学校名字)
    \n来自 MissedYyang
    '''
    accesstoken = ''
    serverside = ''
    userid = ''
    name = ''
    plainUserId = ''
    studentorteacher = ''
    tip = ''
    classroomname = ''
    schoolname = ''
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
    data = re.findall('"data":(.*?),', res.text)[0]
    if data == 'null':
        tip=re.findall('"err_desc":"(.*?)"', res.text)[0]
        pass
    else:
        userid = re.findall('"accessCookie":"(.*?)"', res.text)[0]
        serverside = re.findall('"webUrl":"(.*?)"', res.text)[0]
        studentorteacher = re.findall('"regionalName":(.*?),', res.text)[0]
        name = re.findall('"nickName":"(.*?)"', res.text)[0]
        accesstoken = re.findall('"accessToken":"(.*?)"', res.text)[0]
        plainUserId = re.findall('"plainUserId":(.*?),', res.text)[0]
        classroomname = re.findall('"classroomName":"(.*?)"', res.text)[0]
        schoolname = re.findall('"schoolName":"(.*?)"', res.text)[0]
    return accesstoken, serverside, userid, name, plainUserId, studentorteacher, tip, classroomname, schoolname

def get_login_qrcode():
    '''
    获取登录二维码
    （微信扫一扫）
    来自 Archerfish
    '''

    url = 'https://appapi.xueanquan.com/usercenter/api/v5/wx/wx-login-qrcode'

    headers = {'Accept': '*//*',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'appapi.xueanquan.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
               }
    
    res = requests.get(url=url, headers=headers)

    get_encodesceneid = re.findall('"encodeSceneId":"(.*?)"', res.text)
    Encodesceneid = str(get_encodesceneid).replace("'",'').replace(']','').replace('[','')
    get_relativeUrl = re.findall('"relativeUrl":"(.*?)",', res.text)
    relativeUrl = str(get_relativeUrl).replace("'",'').replace(']','').replace('[','')
    
    #webbrowser.open(relativeUrl)
    #print(relativeUrl)
    #get_scan_result(Encodesceneid)
    return relativeUrl,Encodesceneid

def get_scan_user_info(cookie):
    '''
    扫码成功后获取用户信息
    来自 Archerfish
    '''

    url = 'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/users/user-info'

    headers =  {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie':cookie,
                'Host': 'huodongapi.xueanquan.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
               }
    
    res = requests.get(url=url,headers=headers)

    userid = str(re.findall('"userID":(.*?),', res.text)).replace("'",'').replace(']','').replace('[','')
    username = str(re.findall('"userName":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
    usertype = str(re.findall('"userType":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
    name = str(re.findall('"trueName":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
    schoolname = str(re.findall('"schoolName":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
    grade = str(re.findall('"grade":(.*?),', res.text)).replace("'",'').replace(']','').replace('[','')
    classname = str(re.findall('"className":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')

    classname = '{0}年级{1}'.format(grade,classname)

    if usertype == 'Teacher':
        usertype = '班主任'
    elif  usertype == 'Users':
        usertype = '学生'
    else:
        return 0

    return userid,username,usertype,name,schoolname,grade,classname

def get_scan_result(EncodeSceneId):
    '''
    获取二维码状态
    （若是 '等待扫码',将一直循环获取状态）
    （若是 '扫码已过期，正在重新获取',将会重新获取二维码链接并打开）
    来自 Archerfish
    '''

    url = 'https://appapi.xueanquan.com/usercenter/api/v5/wx/scan-result?encodeSceneId={0}'.format(EncodeSceneId)

    headers = { 'Accept': '*//*',
                'Accept-Encoding': 'gzip',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'appapi.xueanquan.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
        
    data = {' '}

    def checkstatus():
        res = requests.post(url=url, headers=headers, data=data)
        #print(res.text)
        global timer
        timer = threading.Timer(0.2,checkstatus)
        # 获取登陆状态
        statuscode = str(re.findall('"status":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
        # 判断登陆状态
        if statuscode == 'Error':
            statustext = '扫码已过期，正在重新获取'
            print(statustext)
            # 重新调用获取函数
            get_login_qrcode()
            return 0
        elif  statuscode == 'Success':
            # 当状态码为登陆成功时获取用户信息
            useridforcookie = str(re.findall('UserID=(.*?);', str(res.headers['Set-Cookie']))).replace("'",'').replace(']','').replace('[','')
            domainforcookie = str(re.findall('ServerSide=(.*?);', str(res.headers['Set-Cookie']))).replace("'",'').replace(']','').replace('[','').replace('%3A',':').replace("%2F",'/')
            cookies = 'ServerSide={0};UserID={1}'.format(domainforcookie, useridforcookie)
            userid,username,usertype,name,schoolname,grade,classname = get_scan_user_info(cookies)
            all_info = "扫码成功\n"+"姓名: {0},用户ID: {1},用户名: {2},班别: {3},账号类型: {4},学校: {5}".format(name,userid,username,classname,usertype,schoolname)
            print(all_info)
            print(cookies)
            # 取消循环
            timer.cancel()
            return 0
        elif  statuscode == 'Wait':
            print("等待扫码")
        else:
            print('未知状态\n'+ statuscode)

        timer = threading.Timer(0.2,checkstatus)
        timer.start()

    timer = threading.Timer(0.2,checkstatus)
    timer.start()

def qrcode_login(mode):
    '''
    二维码登录
    mode 模式 可选 ('OPBWR'(使用浏览器打开二维码), 'SWURL'(仅显示二维码URL))
    来自 Archerfish
    '''
    if str(mode) == 'OPBWR':
        url,encodeid = get_login_qrcode()
        webbrowser.open(url)
        get_scan_result(encodeid)
    elif  str(mode) == 'SWURL':
        url,encodeid = get_login_qrcode()
        print(url)
        get_scan_result(encodeid)
    else:
        print('错误的 mode 指令')