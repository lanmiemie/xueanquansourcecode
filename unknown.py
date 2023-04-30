import re
from tkinter import *
import tkinter.ttk
import os
import io
from PIL import Image, ImageTk
import tkinter.messagebox
import webbrowser
import requests
import sys
import subprocess
import base64
import time
from MissedYyang import png1
from lanmiemie import png
from lxml import etree
from xueanquanicon import img
import tkinter.filedialog
import ctypes
import random
#import threading
import logging
from tkinter import scrolledtext
from fake_useragent import FakeUserAgent
import hashlib

topunknown = Tk()
#root.attributes("-alpha", 0.8)
#ver = "1.4.4"
title="Unknown Program ???"
topunknown.title(title)
tmp = open("xueanquan.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
global tmpico
tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
topunknown.iconphoto(False ,tmpico)
os.remove("xueanquan.ico")
#root.iconbitmap(".\\backup_user\du.ico")
winWidth = 250
winHeight = 100
screenWidth = topunknown.winfo_screenwidth()
screenHeight = topunknown.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
topunknown.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
topunknown.resizable(0,0)
pointcode = 0
passwordcodetrue = 0
Label(topunknown, text="Password:").place(x=10,y=30)
inp1 = Entry(root, relief=GROOVE)
inp1.place(x=80,y=30)

def gettext():
    global pointcode
    global passwordcodetrue
    getpassword = inp1.get().replace("\n", "").replace("\x20", "")
    code = 'TOMATO'
    if code == getpassword:
        passwordcodetrue = passwordcodetrue + 1
        if passwordcodetrue == 4:
            tkinter.messagebox.showinfo(title='Alesha', message="Who are You :(")
            tkinter.messagebox.showinfo(title='Alesha', message="Do you already know my plan? :((")
            tkinter.messagebox.showinfo(title='Alesha', message="Anyone who knows about this plan has to die :(((")
            tkinter.messagebox.showinfo(title='Alesha', message="So.... :((((")
            tkinter.messagebox.showinfo(title='Alesha', message="I WILL EXIT THIS PROGRAM AND RESTART YOUR COMPUTER :)")
            tkinter.messagebox.showinfo(title='Alesha', message="SO SAY GOODBAY :)")
            os._exit(0)
        else:
            tkinter.messagebox.showinfo(title='Alesha', message="There is nothing here :)")
    else:
        pointcode = pointcode + 1
        if pointcode == 4:
            tkinter.messagebox.showinfo(title='Unknown', message="The tOMatoes And poTatOes are indeed delicious :)")
            pointcode = 0
        else:
            tkinter.messagebox.showerror(title='Error', message="You don't have access to the core :(")
    #print(str(getpassword))


tkinter.ttk.Button(topunknown,text="?!", command = gettext).place(x=80,y=70)
topunknown.mainloop()
#inp1.place(x=120, y=30)
