# -*- coding: utf-8 -*-
# import requests
# import json,datetime,time,hashlib
# # 导入蓝图对象
# from . import api
# # 导入flask内置的对象
# from flask import current_app, jsonify, request
# from fangkexitong import db
# # 导入自定义状态码
# from fangkexitong.utils.response_code import RET
# # 导入模型类
# from fangkexitong.models import Users, Yanzheng2
# # 导入json模块
# import json, re
# # 导入日期模块
# import datetime, time
# import os
# from flask import make_response


# @api.route('/users/add', methods=['GET'])
# def add():
#     users = Users.query.filter().all()
#     for user in users:
#         print user.username
#         json_data = {
#             "appkey": "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ",
#             "time": int(time.time() * 1000),
#             "USERNAME": "{}".format(user.username), #主键不能重复
#             "PASSWORD": "123456",
#             "NAME": "{}".format(user.full_name),
#             "STATUS": "0",
#             "EMAIL":"",
#             "PHONE":"{}".format(user.phone)
#         }
#
#         url = "http://office.600654tz.com/"
#         static = "static/hardware/v2/adduser"
#         screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"
#
#
#         data = static + str(json_data) + screct
#         new_temp = data[0:len(data) - 1]
#         m = hashlib.md5()
#         m.update(new_temp.encode())
#         sign = m.hexdigest().upper()
#         headers = {'Content-Type': 'application/x-www-form-urlencoded',}
#         response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson=+{}".format(json_data))
#         # parkid = response.text
#         # parkid = eval(parkid)["data"]
#         # print parkid
#     return jsonify(success=RET.OK, data="tianjiachenggong")


#
# @api.route('/users/add', methods=['GET'])
# def add():
#     users = Users.query.filter().all()
#     for user in users:
#         print user.username
#         json_data = {
#             "appkey": "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ",
#             "time": int(time.time() * 1000),
#             "USERNAME": "{}".format(user.username), #主键不能重复
#             "deviceld":"zykj001"
#
#
#         }
#
#         url = "http://office.600654tz.com/"
#         static = "static/hardware/v2/adduser"
#         screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"
#
#
#         data = static + str(json_data) + screct
#         new_temp = data[0:len(data) - 1]
#         m = hashlib.md5()
#         m.update(new_temp.encode())
#         sign = m.hexdigest().upper()
#         headers = {'Content-Type': 'application/x-www-form-urlencoded',}
#         response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson=+{}".format(json_data))
#         # parkid = response.text
#         # parkid = eval(parkid)["data"]
#         # print parkid
#     return jsonify(success=RET.OK, data="tianjiachenggong")
