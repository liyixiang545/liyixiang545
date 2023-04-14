import time
import requests
import pymysql
from lxml import etree
import os
from threading import Thread


def get_response(url):
    '''
        得到网页的相应
    '''
    try:
        r = requests.get(url=url)
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

        # print(page_info)
    except:
        print("the function is faild !")
    return page_info


def deal_pageinfo(page_url, page_url_all):
    '''
    得到图片地址，将图片信息存放到一个list中...
    '''
    try:
        page_url_status = 0
        for res in page_url:
            page_res = requests.get(res)
            page_url_status = page_url_status + 1
            if page_res.status_code != 200:
                # print(str("第" + page_url_status + " 张图片获取失败 ！"))
                print(str("request the {1} picture url {0} is faild ,could be download faild !".format(res,page_url_status)))
                continue
            else:
                page_res.encoding = 'utf-8'
                page_name = []
                page_html = etree.HTML(page_res.text)
                photo_address = page_html.xpath("//img[@id='wallpaper']/@src")
                photo_name = page_html.xpath("//img[@id='wallpaper']/@alt")
                page_url_all.extend(photo_address)
                page_name.extend(photo_name)
                print(page_name)
    except Exception as e:
        print("deal_pageinfo exits error",e)
    return page_url_all


def save_photo(page_url_all, save_path, i):
    '''
    通过requests的get请求图片的网址，通过2进制写入到文件中...
    '''
    a = 1
    print("总共{0}张照片".format(len(page_url_all)))
    try:
        for x in page_url_all:
            img = requests.get(x)
            if img.status_code != 200:
                print("{0}不能获取...".format(x))
                continue
            if int(len(page_url_all)/a) == 2 :
                print("已经完成50%...")
            print("正在下载第{0}张照片...".format(a))
            with open(save_path+str("picture_")+str(a)+'.jpg', 'wb') as f:
                f.write(img.content)
            a += 1
        print("图片下载完成...")
        f.close
    except Exception as e :
        print('图片获取失败...由于{0}'.format(e))


def connection_sql():
    '''
    连接数据库的的函数
    '''
    conn = pymysql.connect(host='localhost', user='root', password='1qazCDE#5tgb', database='lywz')
    cur = conn.cursor()
    sql = "SELECT Population, Name FROM city\
            WHERE Population > 2000000;"
    result = cur.execute(sql)
    print(result)
    for t in cur.fetchall():
        print(t)
    conn.close()


def main():
    '''
    主函数，定义全局变量，调用函数...
    '''
    time_1 = time.time()
    save_path = '../capture_img/img/' #方法3
    # save_path = '\\capture_img\\' #方法1
    # save_path = '..\\capture_img\\img\\' #方法2
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)

    # 保存地址可自定义
    print("注意：若输入较大的数值可能会使得最终结果失败，会耗费较大的电脑性能和网络，请合理选择数值...")
    page_end = int(input("请输入想要爬取的页数："))
    print("开始爬取...")
    page_url_all = []
    for i in range(1, page_end+2):
        url = "https://wallhaven.cc/toplist?page=" + str(i)
        url_text = get_response(url)
        page_url = getpage_html(url_text)
        page_url_all = deal_pageinfo(page_url, page_url_all=page_url_all)
    # 把带图片链接的list 传入save_photo方法中 去保存图片
    # t = Thread(target=save_photo(page_url_all, save_path, i))
    # t.start()
    # t.join()
    # save_photo(page_url_all, save_path, i)
    time_2 = time.time() - time_1
    print("时长为：{0}".format(int(time_2)))


if __name__ == "__main__":
    main()

