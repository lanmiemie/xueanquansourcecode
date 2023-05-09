from tkinter import *
from tkinter.ttk import *
import requests
import os
from lxml import etree
import re
 
cookie = 'ServerSide=https://guangdong.xueanquan.com/;UserID=6B0A87E07EB878EC437CABB6803CBC17'


root = Tk() # 源码来自wb98.com
 
tree1 = Treeview(root, columns=('xm', 'zh', 'stuclass', 'stuid'),show='headings') 

tree1.heading('xm', text='姓名')
tree1.heading('zh', text='账号')
tree1.heading('stuclass', text='所在班级')
tree1.heading('stuid', text='学生ID')
 
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

Schoolidtext, Gradeidtext, Classroomidtext, Semesteridtext, UserTypeidtext, OrderColumnidtext, CurrentPageidtext = get_schoolid(cookie)

def get_studentlist(cookies, Schoolid, Gradeid, Classroomid, Semesterid, UserTypeid, OrderColumnid, CurrentPageid):
    '''
    获取获取学生姓名和账号, ID
    '''
    url = 'https://guangdong.xueanquan.com/safeapph5/api/safeEduCardinalData/getAppUserlist?r=0.6287044059085791'

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
        tree1.insert('', END, values=totallist)
        #all_list.append(totallist)
        print(totallist)
        #len(totallist)

    #print(all_list)
    #print(str(studentname_all), str(studentid_all), str(userid_all))

get_studentlist(cookie, Schoolidtext, Gradeidtext, Classroomidtext, Semesteridtext, UserTypeidtext, OrderColumnidtext, CurrentPageidtext)

def adbc(a):
    id_list = tree1.selection()
    for item in id_list:
        name,id1,classroomname1,studentid1 = tree1.item(item)["values"]
        print(name,id1,classroomname1,studentid1)

tree1.bind('<ButtonRelease-1>', adbc)

tree1.pack()
 
root.mainloop()
