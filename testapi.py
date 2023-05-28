import re
import threading
import time
import requests

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

    print(relativeUrl)

    get_scan_result(Encodesceneid)

    return Encodesceneid


def get_scan_result(EncodeSceneId):

    url = 'https://appapi.xueanquan.com/usercenter/api/v5/wx/scan-result?encodeSceneId=' + EncodeSceneId

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
    
    data = {' '}

    def checkstatus():
        res = requests.post(url=url, headers=headers, data=data)
        #print(res.text)
        global timer
        timer = threading.Timer(0.5,checkstatus)
        getstatuscode = re.findall('"status":"(.*?)",', res.text)
        statuscode = str(getstatuscode).replace("'",'').replace(']','').replace('[','')
        if statuscode == 'Error':
            print('扫码已过期，正在重新获取')
            encodeid = get_login_qrcode()
            return 0
        elif  statuscode == 'Success':
            print("扫码成功,正在获取cookie")
            userid = re.findall('UserID=(.*?);', str(res.headers['Set-Cookie']))
            print(userid)
            timer.cancel()
            return 0
        elif  statuscode == 'Wait':
            print("等待扫码")
        else:
            print('失败')

        timer = threading.Timer(0.5,checkstatus)
        timer.start()

    timer = threading.Timer(0.5,checkstatus)
    timer.start()

encodeid = get_login_qrcode()