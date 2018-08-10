# -*- coding: utf-8 -*-
import sys
import requests
import re
import json,datetime,time,hashlib,_md5
# url = "http://office.600654tz.com/"            # 请求的url
# static = "static/hardware/v2/getPassQRCodeWithLift"  # 静态的url
# appkey =  "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ"
# screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"      # 唯一识别密码

def huoquerweima(username):
    url = "http://office.600654tz.com/"  # 请求的url
    static = "static/hardware/v2/getPassQRCodeWithLift"  # 静态的url
    appkey = "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ"
    screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"





    json_data = {
               "appkey": appkey, # appkey 必须
                "time": int((time.time() * 1000)),       #  13位的时间戳
                "businessId": "{}".format(int(time.time())),  #  二维码 null后的数字
                "UserName": "{}".format(username),                    # 手机号位用户名
                "AccessDate": "{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),    # 生成的时间
                "CodeType": "0"            # 固定用户
            }
    data = static + str(json_data) + screct       # 加密准备
    # print(data)
    new_temp = data[0:len(data) - 1]
    m = hashlib.md5()                           # 加密对象
    m.update(new_temp.encode())
    sign = m.hexdigest().upper()                # 完成加密
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}      # 请求头
    response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson={}".format(json_data))
       # 发送请求获得返回的对象
    # print(response.content["data"])
    resp = eval(response.text)["JsonResult"]
    resp = eval(resp)["data"]
    print(resp)
    return resp

# start = time.time()
# resp = huoquerweima(18616841413)
# end = time.time()



# print(resp)
# # # resp = huoquerweima(13761953033)
# # # resp = huoquerweima(13564109035)
# import qrcode
# img = qrcode.make("{18616841413.1533204577|000001b7080000852953A2DC93058D77A428393213277FCAE897FF6D9830F0A308CF5BF0CBBCFFF6EA8B}")
# img.save('./simpleqrcode.jpg')
# img.show()


def huoqusign(username):
    url = "http://office.600654tz.com/"            # 请求的url
    static = "static/hardware/v2/getPassQRCodeWithLift"  # 静态的url
    appkey =  "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ"
    screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"      # 唯一识别密码
    json_data = {
               "appkey": appkey, # appkey 必须
                "time": int((time.time() * 1000)),       #  13位的时间戳
                "businessId": "{}0".format(int(time.time())),  #  二维码 null后的数字
                "UserName": "{}".format(username),                    # 手机号位用户名
                "AccessDate": "{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),    # 生成的时间
                "CodeType": "0"            # 固定用户
            }

    data = static + str(json_data) + screct       # 加密准备
    # print(data)
    new_temp = data[0:len(data) - 1]
    m = hashlib.md5()                           # 加密对象
    m.update(new_temp.encode())
    sign = m.hexdigest().upper()                # 完成加密
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}      # 请求头
    response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson={}".format(json_data))
       # 发送请求获得返回的对象
    # print(response.content["data"])
    resp = eval(response.text)["JsonResult"]
    resp = eval(resp)["data"]
    return resp

def fangkeerweima(visitor_time):
    url = "http://office.600654tz.com/"            # 请求的url
    static = "static/hardware/v2/getPassQRCodeWithLift"  # 静态的url
    appkey =  "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ"
    screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"      # 唯一识别密码
    json_data = {
               "appkey": appkey, # appkey 必须
                "time": int((time.time() * 1000)),       #  13位的时间戳
                "businessId": "{}0".format(int(time.time())),  #  二维码 null后的数字
                "UserName": "13793801038",                    # 手机号位用户名
                "AccessDate": "{}".format(visitor_time),    # 生成的时间
                "CodeType": "1"            # 固定用户
            }

    data = static + str(json_data) + screct       # 加密准备
    # print(data)
    new_temp = data[0:len(data) - 1]
    m = hashlib.md5()                           # 加密对象
    m.update(new_temp.encode())
    sign = m.hexdigest().upper()                # 完成加密
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}      # 请求头
    response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson={}".format(json_data))
       # 发送请求获得返回的对象
    # print(response.content["data"])
    resp = eval(response.text)["JsonResult"]
    resp = eval(resp)["data"]
    return resp
a = fangkeerweima("2018-08-10 08:00")
#
#
import qrcode
img = qrcode.make("{}".format(a))
img.save('./simpleqrcode.jpg')
img.show()