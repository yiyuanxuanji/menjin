# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')
# # -*- coding: utf-8 -*-
import requests
import json,datetime,time,hashlib
a = []
def shanchu(u):
    json_data = {
        "appkey": "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ",
        "time": int(time.time() * 1000),
        "UserName": "{}".format(u), #主键不能重复
        "deviceId": "zykj001",
        "CanShare": 0
    }

    url = "http://office.600654tz.com/"
    static = "static/hardware/v2/addDevicePermission"
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

shanchu(13761953033)


shanchu(13701940909)
shanchu(18939891535)
shanchu(18017331315)
shanchu(15001929821)
shanchu(17721416426)
shanchu(15901883685)
shanchu(13816532263)
shanchu(17701863188)
shanchu(18151220895)
shanchu(13614039416)
shanchu(13641776660)
shanchu(18642089923)
shanchu(13564109035)
shanchu(13601980334)
shanchu(18158911685)
shanchu(15821707550)
shanchu(13637994002)
shanchu(18121073776)
