import re
import base64
#将需要使用的storm_24px_1127546_easyicon.net.ico的图片以base64格式读出
openexe = open('student.ico',"rb")
b64str = base64.b64encode(openexe.read())  #以base64的格式读出
openexe.close()
write_data = "img=%s" % b64str
f = open("xueanquanicon.py","w+")   #将上面读出的数据写入到qq.py的img数组中
f.write(write_data)
f.close()
