from tkinter import *
import tkinter.ttk
import requests
import os
from lxml import etree
import re
from xueanquanapi import teacher_get_special_list
 
root = Tk()

cookie = 'ServerSide=https://guangdong.xueanquan.com/;UserID=6B0A87E07EB878EC437CABB6803CBC17'

def treeview_teacher_get_special_list():
    top = Toplevel()
        
    tree1 = tkinter.ttk.Treeview(top, columns=('ztm', 'jzsj', 'wcrs', 'ywcrs', 'wcbfb', 'ztzt'),show='headings') 

    tree1.heading('ztm', text='专题名')
    tree1.heading('jzsj', text='截止时间')
    tree1.heading('wcrs', text='完成人数')
    tree1.heading('ywcrs', text='应完成人数')
    tree1.heading('wcbfb', text='完成百分比')
    tree1.heading('ztzt', text='专题状态')

    tree1.column('ztm',anchor='center')
    tree1.column('jzsj',anchor='center')
    tree1.column('wcrs',anchor='center')
    tree1.column('ywcrs',anchor='center')
    tree1.column('wcbfb',anchor='center')
    tree1.column('ztzt',anchor='center')

    get_all_list = teacher_get_special_list(cookie)

    for all_list in get_all_list:
        #print(all_list)
        tree1.insert('', END, values=all_list)

    def adbc(a):
        id_list = tree1.selection()
        for item in id_list:
            specialname,endtime,completepeople,shouldcompletepeople,completerate,specailstatus = tree1.item(item)["values"]
            print(specialname,endtime,completepeople,shouldcompletepeople,completerate,specailstatus)

    tree1.bind('<ButtonRelease-1>', adbc)

    tree1.pack()

def get_treeview_students_information():
    treeview_info = Toplevel()
    treeview_info.title('提示')
    winWidth = 400
    winHeight = 200
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    treeview_info.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    treeview_info.resizable(0, 0)
    lf_show_student_information = tkinter.ttk.LabelFrame(treeview_info,text="学生信息")
    lf_show_student_information.place(x=100, y=8,width=200,height=100)
    Label(lf_show_student_information,text='姓名:').place(x=10,y=2)
    Label(lf_show_student_information,text='账号:').place(x=110,y=2)
    Label(lf_show_student_information,text='班级:').place(x=10,y=120)
    Label(lf_show_student_information,text='学生ID:').place(x=50,y=120)

get_treeview_students_information()
treeview_teacher_get_special_list()

root.mainloop()