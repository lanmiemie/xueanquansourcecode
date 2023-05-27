import time

import requests


def download(name, url, cookies, header={'Connection': 'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}, interval=0.5):
    def MB(byte):
        return byte / 1024 / 1024
    #print(name)
    if len(cookies) == 0:
        try:
            res = requests.get(url,headers=header)
        except Exception as e:
            print('下载失败')
            return 0
    else:
        headera = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Connection': 'keep-alive',
                   #'Content-Length': '83',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Cookie': cookies,
                   'Host': 'guangzhou.xueanquan.com',
                   'Origin': 'https://guangzhou.xueanquan.com',
                   'Referer': 'https://guangzhou.xueanquan.com/EduAdmin/Home/Index',
                   #'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                   'sec-ch-ua-mobile': '?0',
                   'sec-ch-ua-platform': 'Windows',
                   'Sec-Fetch-Dest': 'document',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Site': 'same-origin',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'
                   }
        try:
            res = requests.get(url,headers=headera)
        except Exception as e:
            print('连接到远程服务器失败，请再试一次')
            return 0
    f = open(name, 'wb')
    down_size = 0  # 已下载字节数
    old_down_size = 0  # 上一次已下载字节数
    time_ = time.time()
    for chunka in res.iter_content(chunk_size=512):
        if chunka:
            f.write(chunka)
            down_size += len(chunka)
            if time.time() - time_ > interval:
                #rate = down_size / file_size * 100  # 进度  0.01%
                speed = (down_size - old_down_size) / interval  # 速率 0.01B/s
                old_down_size = down_size
                time_ = time.time()
                global print_params
                print_params = [MB(speed), MB(down_size)]
                #sys.stdout.write("\r[%s%s] %d%%" % ('>' * done, ' ' * (50 - done), 100 * down_size / file_size))
                #sys.stdout.flush()
                print('\r{:.1f}MB/s -已下载 {:.1f}MB  '.format(*print_params))
                #print('\r{:.1f}MB/s -已下载 {:.1f}MB，共 {:.1f}MB 已下载百分之:{:.2%} 还剩 {:.0f} 秒   '.format(*print_params))
    f.close()

download('./a.exe','https://gitee.com/archerfish/xueanquanhelperdownload/raw/master/xueanquanhelperforteacher.exe',cookies = '')