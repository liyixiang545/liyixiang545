import calendar
import time
import requests
from lxml import etree
import os
import threading
from threading import Lock
import queue
lock = Lock()
queue = queue.Queue()

# 线程 MyThread(func,args=(params,))
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

# 时间戳
def get_timestamp():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    return time_stamp

# 保存地址可自定义
def save_path():
    save_path = './capture_img/img/'  # 方法3
    # save_path = '\\capture_img\\' #方法1
    # save_path = '..\\capture_img\\img\\' #方法2
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)
    return save_path

def get_response(url):
    '''
        得到网页的相应
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    try:
        r = requests.get(url=url, headers=headers)
        r.status_code == 200
        r.encoding = 'utf-8'
        return r.text
    except:
        print("get error/请求失败！")


def getpage_html(url_text):
    '''
    得到二级网页的信息以及图片的地址信息.....
    '''
    try:
        html = etree.HTML(url_text)
        page_info = html.xpath("//a[@class='preview']/@href")

        print(page_info)
    except:
        print("the function is faild !")
    return page_info


def deal_pageinfo(page_url, page_url_all):
    '''
    得到图片地址，将图片信息存放到一个list中...
    '''
    try:
        page_url_status = 0
        page_name = []
        page_name_list = []
        for res in page_url:
            page_res = requests.get(res)
            page_url_status = page_url_status + 1
            if page_res.status_code != 200:
                print(str("request the {1} picture url {0} is faild ,could be download faild !".format(res,page_url_status)))
                continue
            else:
                page_res.encoding = 'utf-8'
                page_html = etree.HTML(page_res.text)
                photo_address = page_html.xpath("//img[@id='wallpaper']/@src")
                photo_name = page_html.xpath("//img[@id='wallpaper']/@alt")
                page_url_all.extend(photo_address)
                page_name.extend(photo_name)
        # save_photo(page_url_all, save_path(), page_name)
        T1 = MyThread(save_photo, args=(page_url_all, save_path(), page_url_status,))
        # page_name_list.append(T1)
        # for T in page_name_list:
        T1.setName("save")
        T1.start()
        T1.join()
    except Exception as e:
        print("deal_pageinfo exits error ：",e)
    return page_url_all

def save_photo(page_url_all, save_path, page_name):
    '''
    通过requests的get请求图片的网址，通过2进制写入到文件中...
    '''
    a = 1
    print("总共{0}张照片".format(len(page_url_all)))
    try:
        # for x in page_url_all:
        for x in range(len(page_url_all)):
            img = requests.get(page_url_all[x])
            if img.status_code != 200:
                print("{0}不能获取...".format(img))
                continue
            if int(len(page_url_all)/a) == 2 :
                print("已经完成50%...")
            print("正在下载第{0}张照片...".format(a))
            # lock.acquire()
            with open(save_path + str(get_timestamp()) + '.jpg', 'wb') as f:
                f.write(img.content)
                a += 1
            # lock.release()
            print("图片下载完成...")
    except Exception as e :
        print('图片获取失败...由于{0}'.format(e))


def main():
    '''
    主函数，定义全局变量，调用函数...
    '''
    time_1 = time.time()
    print("注意：若输入较大的数值可能会使得最终结果失败，会耗费较大的电脑性能和网络，请合理选择数值...")
    page_start = int(input("输入开始爬取页数："))
    page_end = int(input("输入结束爬取的页数："))
    print("开始爬取...")
    page_url_all = []
    thread_list = []
    for i in range(page_start, page_end+1):
        print("第{0}页".format(i))
        url = "https://wallhaven.cc/toplist?page=" + str(i)
        url_text = get_response(url)
        page_url = getpage_html(url_text)
        # deal_pageinfo(page_url, page_url_all=page_url_all)
        # 把带图片链接的list 传入save_photo方法中 去保存图片
        T = MyThread(deal_pageinfo,args=(page_url, page_url_all,))
        # T1 = threading.Thread(target=deal_pageinfo(page_url, page_url_all))
        # thread_list.append(T)
        # page_1url_all = t.get_result()
        # save_photo(page_url_all, save_path(), i)
        T.setName("deal_picture")
        T.start()
        T.join()
    time_2 = time.time() - time_1
    print("时长为：{0} s".format(int(time_2)))


if __name__ == "__main__":
    main()

