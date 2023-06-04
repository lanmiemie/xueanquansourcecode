import re
import threading
import time
import requests
import webbrowser

def get_login_qrcode():

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
    
    webbrowser.open(relativeUrl)
    print(relativeUrl)
    get_scan_result(Encodesceneid)
    return relativeUrl,Encodesceneid

def get_scan_user_info(cookie):

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
        usertype = '教师'
    elif  usertype == 'Users':
        usertype = '学生'
    else:
        return 0

    return userid,username,usertype,name,schoolname,grade,classname


def get_scan_result(EncodeSceneId):

    url = 'https://appapi.xueanquan.com/usercenter/api/v5/wx/scan-result?encodeSceneId={0}'.format(EncodeSceneId)

    headers = { 'Accept': '*//*',
                'Accept-Encoding': 'gzip',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'appapi.xueanquan.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                #'X-Requested-With': 'XMLHttpRequest'
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
            print('扫码已过期，正在重新获取')
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

relativeUrl,encodeid = get_login_qrcode()
#get_scan_user_info()
