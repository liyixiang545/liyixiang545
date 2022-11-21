import requests

url = "blob:http://127.0.0.1:8080/8499d082-09ca-4c61-a621-99223fd188e2"
data = requests.get(url=url).text
print(data)