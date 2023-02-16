import time
import re
import base64

icon = open("favicon.ico", 'rb').read()
b64str = base64.b64encode(icon)
write_data = "img=%s" % b64str
f = open("xueanquanicon.py", "wb")
f.write(str(write_data))
f.close()
