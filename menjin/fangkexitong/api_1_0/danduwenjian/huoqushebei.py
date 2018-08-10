# -*- coding: utf-8 -*-
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')
# # -*- coding: utf-8 -*-
import requests
import json,datetime,time,hashlib


json_data = {
    "appkey": "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ",
    "time": int(time.time() * 1000),
    "USERNAME": "13793801038", #主键不能重复
    "PASSWORD": "123456",
    "NAME": "zhenyan".encode(),
    "STATUS": "0",
    "EMAIL":"",
    "PHONE":"13761953033"
}

url = "http://office.600654tz.com/"
static = "static/hardware/v2/adduser"
screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"


data = static + str(json_data) + screct
new_temp = data[0:len(data)-1]

m = hashlib.md5()
m.update(new_temp.encode())
sign = m.hexdigest().upper()
headers = {'Content-Type': 'application/x-www-form-urlencoded',}
response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson={}".format(json_data))
parkid = response.text
# parkid = eval(parkid)["data"]
print (parkid)
