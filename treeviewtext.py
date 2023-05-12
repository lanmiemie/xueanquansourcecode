from tkinter import *
from tkinter.ttk import *
import requests
import os
from lxml import etree
import re
from xueanquanapi import get_schoolid, get_studentlist
 
cookies = 'ServerSide=https://guangdong.xueanquan.com/;UserID=6B0A87E07EB878EC437CABB6803CBC17'

def importtreeview(cookie):
    top = Toplevel()
    
    tree1 = Treeview(top, columns=('xm', 'zh', 'stuclass', 'stuid'),show='headings') 

    tree1.heading('xm', text='姓名')
    tree1.heading('zh', text='账号')
    tree1.heading('stuclass', text='所在班级')
    tree1.heading('stuid', text='学生ID')

    Schoolidtext, Gradeidtext, Classroomidtext, Semesteridtext, UserTypeidtext, OrderColumnidtext, CurrentPageidtext = get_schoolid(cookie)

    get_all_list = get_studentlist(cookie, Schoolidtext, Gradeidtext, Classroomidtext, Semesteridtext, UserTypeidtext, OrderColumnidtext, CurrentPageidtext)

    for all_list in get_all_list:
        #print(all_list)
        tree1.insert('', END, values=all_list)

    def adbc(a):
        id_list = tree1.selection()
        for item in id_list:
            name,id1,classroomname1,studentid1 = tree1.item(item)["values"]
            print(name,id1,classroomname1,studentid1)

    tree1.bind('<ButtonRelease-1>', adbc)

    tree1.pack()
    
    top.mainloop()
