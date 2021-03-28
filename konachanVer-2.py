import requests
import re
import os
import time

def kogetli(page):
    print('开始获取第', page, '页的图片')
    url = 'https://konachan.net/post?page=' + str(page)
    body = requests.get(url)
    imgulstart = body.text.find('''<ul id="post-list-posts">''')
    imgulendbody = body.text[imgulstart:9999999]
    imgulend = imgulendbody.find('''</ul>''')
    # 获取li
    imglistli = body.text[imgulstart + 25:imgulend + imgulstart]
    # print(imglistli)
    return imglistli


def get_konachanpic():
    page = 1
    picnum = 1
    html = kogetli(page)
    while True:
        pic_url = re.findall('class="directlink largeimg" href="(.*?)"', html, re.S)
        for key in pic_url:
            # print(key+'\n')
            print('开始获取第', picnum, '张图片')
            picname_ = str(key)[26:999999].replace('/', '')
            picname = picname_[0:picname_.find('Konachan')]
            if not os.path.exists(os.getcwd() + '\\' + picname + '.jpg'):
                seve_pic(key,os.getcwd() + '\\' + picname + '.jpg')
            else:
                print("文件已存已跳过下载")
            picnum = picnum + 1
        page = page + 1
        html = kogetli(page)


def seve_pic(url,path):
     start = time.time() #下载开始时间
     response = requests.get(url, stream=True)
     size = 0 #初始化已下载大小
     chunk_size = 1024 # 每次下载的数据大小
     content_size = int(response.headers['content-length']) # 下载文件总大小
     try:
         if response.status_code == 200: #判断是否响应成功
          print('开始下载,[文件大小]:{size:.2f} MB'.format(size = content_size / chunk_size /1024)) #开始下载，显示下载文件大小
          filepath = path
          with open(filepath,'wb') as file: #显示进度条
              for data in response.iter_content(chunk_size = chunk_size):
               file.write(data)
               size +=len(data)
               print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size), float(size / content_size * 100)) ,end=' ')
         end = time.time() #下载结束时间
         print('下载完成！耗时: %.2f秒' % (end - start)) #输出下载用时时间
     except:
         print('Error!')

if __name__ == '__main__':
    print("开始获取图片")
    get_konachanpic()
