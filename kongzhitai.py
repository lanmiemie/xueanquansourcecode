import re
from tkinter import *
import tkinter.ttk
from socket import *
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
from lxml import etree
from xueanquanicon import img
import tkinter.filedialog
import ctypes
import random
import threading
import logging
import markdown
from tkinter import scrolledtext
from fake_useragent import FakeUserAgent

from tkhtmlview import HTMLLabel

# Create Object
root = Tk()

# Set Geometry
root.geometry("400x400")

url = 'https://github.com/SimpleJony/SimpleJony/raw/main/README.md'
ver_url = 'https://file-fatdeadpanda.netlify.app/ver'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'}
a = requests.get(url, headers = header).text
aa = markdown.markdown(a)

# Add label
my_label = HTMLLabel(root, html=aa)

# Adjust label
my_label.pack()

# Execute Tkinter
root.mainloop()

