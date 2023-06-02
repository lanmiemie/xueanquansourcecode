import threading
import webbrowser
import requests
from lxml import etree
import re
from fake_useragent import FakeUserAgent
import datetime

def login(username, password):
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

def teacher_get_schoolid(cookies):
    '''
    获取教师各类ID, 例: Schoolid, Gradeid, Classroomid.等.....
    '''
    url = 'https://guangdong.xueanquan.com/safeapph5/accountSituation/_ClassTeacher'
    headers = {'Accept': '*//*',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': cookies,
               'Host': 'guangzhou.xueanquan.com',
               'Origin': 'https://guangzhou.xueanquan.com',
               #'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
               #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': 'Windows',
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    res = requests.get(url=url, headers=headers)
    xpathhtml = etree.HTML(res.text)
    
    getSchoolid = xpathhtml.xpath("//input[@id='SchoolId']/@value")
    Schoolid = str(getSchoolid).replace("'", '').replace("[", '').replace("]", '')
    
    getGradeid = xpathhtml.xpath("//input[@id='Grade']/@value")
    Gradeid = str(getGradeid).replace("'", '').replace("[", '').replace("]", '')
    
    getClassroomid = xpathhtml.xpath("//input[@id='Classroom']/@value")
    Classroomid = str(getClassroomid).replace("'", '').replace("[", '').replace("]", '')
    
    getSemesterid = xpathhtml.xpath("//input[@id='Semester']/@value")
    Semesterid = str(getSemesterid).replace("'", '').replace("[", '').replace("]", '')
    
    getUserTypeid = xpathhtml.xpath("//input[@id='UserType']/@value")
    UserTypeid = str(getUserTypeid).replace("'", '').replace("[", '').replace("]", '')
    
    getOrderColumnid = xpathhtml.xpath("//input[@id='OrderColumn']/@value")
    OrderColumnid = str(getOrderColumnid).replace("'", '').replace("[", '').replace("]", '')
    
    return Schoolid, Gradeid, Classroomid, Semesterid, UserTypeid, OrderColumnid

def teacher_get_studentlist(cookies, Schoolid, Gradeid, Classroomid, Semesterid, UserTypeid, OrderColumnid):
    '''
    教师获取学生姓名和账号, ID
    以 List 的形式输出
    {'姓名', '账号', '班别', '学生ID'}
    '''
    url = 'https://guangdong.xueanquan.com/safeapph5/api/safeEduCardinalData/getAppUserlist'

    headers = {'Accept': '*//*',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': cookies,
               'Host': 'guangzhou.xueanquan.com',
               'Origin': 'https://guangzhou.xueanquan.com',
               #'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
               #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': 'Windows',
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }

    data1 = 'SchoolId='+ Schoolid + '&Grade='+ Gradeid + '&Classroom='+ Classroomid +'&Semester='+ Semesterid +'&UserType='+ UserTypeid +'&OrderColumn='+ OrderColumnid + '&CurrentPage=1&ItemsPerPage=2000&IsPage=True'
        
    res = requests.post(url=url, headers=headers, data=data1)

    #print(res.text)

    all_list = list()

    userid_all = re.findall('"userID": (.*?),', res.text)
    studentname_all = re.findall('"trueName": "(.*?)",', res.text)
    studentid_all = re.findall('"userName": "(.*?)",', res.text)
    totalitems = re.findall('"totalItems": (.*?),', res.text)
    classroomname = re.findall('"className": "(.*?)",', res.text)
    grade = re.findall('"grade": (.*?),', res.text)

    for stu_name,stu_id,stu_user_id,stu_classroomname,stu_grade in zip(studentname_all,studentid_all,userid_all,classroomname,grade):
        totallist = "list%s"%len(totalitems)
        stu_grade_and_classroom = str(stu_grade) +'年级'+ str(stu_classroomname)
        totallist = [stu_name,stu_id,stu_grade_and_classroom,stu_user_id]
        all_list.append(totallist)
        #print(totallist)
        #len(totallist)

    return all_list


def teacher_get_students(cookies):
    '''
    教师单独学生账号，studentid
    （只返回学生账号）
    来自 MissedYyang
    以 List 的形式返回
    '''
    url = 'https://guangzhou.xueanquan.com/eduadmin/ClassManagement/ClassManagement'
    headers = {'Accept': '*//*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Length': '83',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': cookies,
               'Host': 'guangzhou.xueanquan.com',
               'Origin': 'https://guangzhou.xueanquan.com',
               'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
               #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': 'Windows',
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    data = {'status': '',
            'keywords': '',
            'pageNum': '1',
            'numPerPage': '100',
            'orderField': '',
            'orderDirection': 'DESC',
            'TrueName': ''}
    res = requests.post(url=url, headers=headers, data=data)
    # print(res.text)
    student_all = re.findall('target="dbl" rel="(.*?)"', res.text)
    # print(len(student_all))
    # print(student_all)
    # 保存到本地---取消
    # file_path = './student.txt'
    # f = open(file_path, 'w')
    # f.write(str(student_all))
    # f.close()
    return student_all

def teacher_get_students_xlsx(cookies):
    '''
    教师获取学生账号表格下载地址
    '''
    url = 'https://guangzhou.xueanquan.com/eduadmin/ClassManagement/ClassManagement'
    headers = {'Accept': '*//*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': cookies,
               'Host': 'guangzhou.xueanquan.com',
               'Origin': 'https://guangzhou.xueanquan.com',
               'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
               #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': 'Windows',
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    data = {'status': '',
            'keywords': '',
            'pageNum': '1',
            'numPerPage': '2000',
            'orderField': '',
            'orderDirection': 'DESC',
            'TrueName': ''}
    res = requests.post(url=url, headers=headers, data=data)
    getxlsxdata = etree.HTML(res.text)
    getsparexlsx = getxlsxdata.xpath("//a[@class='icon']/@href")
    getsparexlsxa = str(getsparexlsx)
    getsparexlsxtext = getsparexlsxa.replace("'", '').replace("[", '').replace("]", '')
    urlfinally = url.replace('/eduadmin/ClassManagement/ClassManagement', getsparexlsxtext)

    return urlfinally
    
def get_message(userid, accesstoken, plainUserId):
    '''
    获取假期安全提醒阅读
    来自 MissedYyang
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
    
    return title_all, messageid_all

def get_homework(userid, accesstoken):
    '''
    获取学期任务 and 专题任务
    学生账号，不分专题任务和学期任务接口，可怕
    来自 MissedYyang
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

def get_special(url, userid):
    '''
    获取专题任务id信息
    来自 MissedYyang
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
        # ↓ 获取留言列表
        url2 = url.replace('index.html', 'message.html').replace('?require-un=true', '' )
        getsd= requests.get(url=url2, headers=headers)
        getsddata = etree.HTML(getsd.text)
        # 使用留言列表来获取 备用 Special ID 
        getsparesd = getsddata.xpath("//title[normalize-space()]/text()")
        getsparesda = str(getsparesd)
        getsparesdtext = getsparesda.replace("'", '').replace("[", '').replace("]", '')
        
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
        res2 = res1.text.replace(' ', '')
        # print(res2)
        id_all = re.findall('data-specialId="(.*?)"', res2)[0]

    print('专题id:  ', id_all)
    print('备用专题id:  ',getsparesdtext)

    return id_all, getsparesdtext

def teacher_get_special_list(cookie):
    '''
    教师获取专题任务信息
    以 List 的形式输出
    {'专题名', '截止时间', '完成人数', '应完成人数', '完成百分比', '专题状态'}
    '''
    all_special_list = list()
    get_today = datetime.date.today()
    url = 'https://applet.xueanquan.com/pt/guangdong/safeapph5/api/safeEduScore/getSpecailProgress?semester=3&schoolYear='+str(get_today.year)
    headers = {'Host': 'applet.xueanquan.com',
               'Origin': 'https://safeh5.xueanquan.com',
               'Accept-Encoding': 'gzip, deflate, br',
               'Cookie': cookie,
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
        finally_specialname = str(specialname).replace('"','')
        finally_endtime = re.findall('\d{4}-\d{2}-\d{2}',endtime)
        if specailstatus == '1':
            finally_specailstatus = '未截止'
            totallist = [finally_specialname,finally_endtime,completepeople,shouldcompletepeople,completerate,finally_specailstatus]
            all_special_list.append(totallist)
        else:
            finally_specailstatus = '已截止'
            totallist = [finally_specialname,finally_endtime,completepeople,shouldcompletepeople,completerate,finally_specailstatus]
            all_special_list.append(totallist)

    return all_special_list

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
    return Encodesceneid

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