import requests
from lxml import etree

def get_schoolid(cookies):
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
    
    getCurrentPageid = xpathhtml.xpath("//input[@id='CurrentPage']/@value")
    CurrentPageid = str(getCurrentPageid).replace("'", '').replace("[", '').replace("]", '')
    
    return Schoolid, Gradeid, Classroomid, Semesterid, UserTypeid, OrderColumnid, CurrentPageid

