'''
# 尝试写一个学生安全教育平台一件完成的助手
需要实现：
1、登陆学生账号密码，密码错误时提示
2、获取并完成学生节假日安全提醒信息
3、获取并完成安全学习任务（包括，学期任务和专题任务）
    全部需要做的任务都OK
4、实现多用户一件完成模式-----因不需要，暂未开发，可直接遍历账号密码即可
-----by.Yyang____2022.06.19
'''
import sys
import os
import re
import time
import requests
from fake_useragent import FakeUserAgent


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
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
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
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6'}
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
                   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6'}
        res = requests.post(url=url, headers=headers)
        print(res.text)
    except Exception as e:
        print(e)
        if num < 4:
            print('Tip:  第{0}次重试，事不过三！'.format(num))
            num = num + 1
            do_message(accesstoken, userid, messageId, num)
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
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
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
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
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
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
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
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6)',
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
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
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
            print('Tip:  第{0}次重试，事不过三！'.format(num))
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
        json = {"specialId": specialId, "step": step}
        res = requests.post(url=url, headers=headers, json=json)
        print(res.text)
        time.sleep(0.5)
    except Exception as e:
        print(e)
        if num < 4:
            print('Tip:  第{0}次重试，事不过三！'.format(num))
            num = num + 1
            do_special(userid, specialId, step, num)
        else:
            pass


def do_holiday(userid, schoolYear, semester, step):
    '''
    完成寒暑假任务专题
    '''
    url = 'https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/holiday/sign'
    cookies = 'ServerSide=https://guangdong.xueanquan.com/;' + 'UserID=' + userid
    headers = {'Host': 'huodongapi.xueanquan.com',
               'Content-Type': 'application/json',
               'Origin': 'https://huodong.xueanquan.com',
               'Accept-Encoding': 'gzip, deflate, br',
               'Cookie': cookies,
               'Connection': 'keep-alive',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 safetreeapp/1.8.6',
               #'Referer: https://huodong.xueanquan.com/summer2022/summer_one.html',
               'Content-Length': '41',
               'Accept-Language': 'zh-cn'}
    json = {
        "semester": semester,
        "step": step,
        "schoolYear": schoolYear}
    res = requests.post(url=url, headers=headers, json=json)
    print(res.text)


def main(username, password):

    num = 1
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
            print('OK--{}===============已经完成了。。'.format(title))
        elif '"workStatus": "Expired"' in w:
            # 活动已过期
            title = re.findall('"title": "(.*?)",', w)[0]
            print('Attention:{}________________未完成，完成时间已过。。'.format(title))
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
                print('YES-正在运行.......完成安全学习任务:{}'.format(title))
                # print(gradeid,courseid)
                # 未进行测试___没有账号测试
                do_homework(courseid, gradeid, userid, num)

            else:
                # 安全专题任务
                title = re.findall('"title": "(.*?)",', w)[0]
                url = re.findall('"linkUrl": "(.*?)"', w)[0]

                print('YES-正在运行........完成专题学习任务:{}'.format(title))
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
                    # print('😭sorry,此功能正在开发。z z z z z z')

                    id_all = get_special(url, userid)
                    specialId = id_all
                    do_special(userid, specialId, step=1, num=num)
                    do_special(userid, specialId, step=2, num=num)


class Logger(object):
    '''
    控制台输出记录到文件
    这个类，看不懂，来自百度拼接
    '''

    def __init__(self, file_name="Default.log", stream=sys.stdout):
        self.terminal = stream
        self.log = open(file_name, "a", buffering=1)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
        # pass

    def close(self):
        self.log.close()


if __name__ == '__main__':

    while True:
        # 自定义目录存放日志文件
        log_path = 'C:/Logs/'
        # 判断文件夹是否存在
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 日志文件名按照程序运行时间设置
        log_file_name = log_path + 'log-' + \
            time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
        # 记录正常的 print 信息
        sys.stdout = Logger(log_file_name)
        # 记录 traceback 异常信息
        sys.stderr = Logger(log_file_name)
        print('''安全教育平台助手是由Yyang 提供的服务，
本服务条款（下称“服务条款”）是您与 Yyang关于您（“您”或“用户”）
访问和使用安全教育平台助手的主要协议。
隐私策略
本程序运行生成日志文件会保存在您的计算机里，本人承诺不收集任何信息。
免责声明
您的任何操作若导致被您所在的市安全教育平台黑名单、问责、罚款，
亦或者被上级领导问话、警告，均与作者无关，作者不承担任何相关责任。
您使用或转发等一切操作行为，均代表您同意本软件免责声明。
使用说明
本网站只需要输入学生的安全教育平台密码，即可。
技术支持
@Yyang''')
        # 进入循环体
        # 计划加入用户选着模式--ok
        # 用户输入
        print('==============安全教育助手平台（学生版）================')
        print('========================================-By.Yyang====')
        print('洋洋提醒您：为了尽可能保障每个活动任务能够顺利完成，速度会慢点哦！')
        print('\n')
        print('请输入账号（学生），并按回车确定：')
        username = input('')
        print('请输入密码（学生），并按回车确定：')
        password = input('') or '123456'
        print(username, '，此账号正在运行中。zzzzz')
        # 登陆账号，获取信息
        accesstoken, serverside, userid, name, plainUserId = login(
            username, password)
        # 判断是否登录成功
        if name != '':
            print('登录成功！！\n程序正在运行，请不要关闭此界面。。。。。。。。。。。。\n')
            main(username, password)
            time.sleep(5)
            Logger(log_file_name)
            print('okokokok,执行完成。。。。。。。。。\n')
            # sys.exit()
        else:
            print('账号、密码输入有误，请再次输入：\n')
