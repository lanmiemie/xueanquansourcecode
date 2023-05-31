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
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Host': 'appapi.xueanquan.com',
               'Origin': 'https://login.xueanquan.com',
               'Referer': 'https://login.xueanquan.com/login?type=codeLogin',
               #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': 'Windows',
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    
    res = requests.get(url=url, headers=headers)

    get_encodesceneid = re.findall('"encodeSceneId":"(.*?)"', res.text)
    Encodesceneid = str(get_encodesceneid).replace("'",'').replace(']','').replace('[','')
    get_relativeUrl = re.findall('"relativeUrl":"(.*?)",', res.text)
    relativeUrl = str(get_relativeUrl).replace("'",'').replace(']','').replace('[','')
    
    webbrowser.open(relativeUrl)
    print(relativeUrl)
    get_scan_result(Encodesceneid)
    return Encodesceneid

def get_scan_result(EncodeSceneId):

    url = 'https://appapi.xueanquan.com/usercenter/api/v5/wx/scan-result?encodeSceneId={0}'.format(EncodeSceneId)

    headers = { 'Accept': '*//*',
                'Accept-Encoding': 'gzip',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'appapi.xueanquan.com',
                'Origin': 'https://login.xueanquan.com',
                'Referer': 'https://login.xueanquan.com/login?type=codeLogin',
                #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                #'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
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
            userid = str(re.findall('"userId":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
            username = str(re.findall('"userName":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
            name = str(re.findall('"trueName":"(.*?)",', res.text)).replace("'",'').replace(']','').replace('[','')
            print("扫码成功\n"+"姓名: " + name + ", 用户ID : " + userid + ", 用户名: " + username +"\n正在获取cookie")
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

encodeid = get_login_qrcode()