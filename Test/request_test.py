# 引入库
import requests,json,time
def postLoing():
    # url = "http://127.0.0.1:5000/User/Login"
    url2 = "http://127.0.0.1:5000/User/GetCaptcha"
    # 请求接口
    data = json.dumps({"email":"admin@qq.com","password":"123456"})
    # res = requests.post(url, data)
    res2 = requests.get(url2)
    print(res2.content.decode('utf-8'))
    #对返回的内容进行编码
    # content = res.content.decode('utf-8')
    content = res2.content.decode('utf-8')
    #将json字符串反序列化
    # tokenJson = json.loads(content)
    # access_token = tokenJson['access_token']
    # print(json.loads(content))
    print(content)


i=1
while 1:
    try:
        postLoing()
        print(i)
        time.sleep(1)
        i = i + 1
    except:
     pass