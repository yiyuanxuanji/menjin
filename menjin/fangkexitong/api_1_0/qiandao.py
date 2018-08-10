# -*- coding: utf-8 -*-
from .erweimatupian import huoquerweima, huoqusign
# 导入蓝图对象
from . import api
# 导入flask内置的对象
from flask import current_app, jsonify, request
from fangkexitong import db
# 导入自定义状态码
from fangkexitong.utils.response_code import RET
# 导入模型类
from fangkexitong.models import Users, Invitation, InvitingPerson, Applicant, Visitors, PersonOpen, Limit_visitor, Waichu, Yanzheng2
# 导入json模块
import json, re
# 导入日期模块
import datetime, time
from sqlalchemy import extract
import os
from flask import make_response
import hashlib



@api.route('/users/sign', methods=['GET'])
def sign_open_id():
    """用户打卡上班
        """
    username = request.args.get('username')
    if username:
        resp = huoquerweima(username)
        return jsonify(success=RET.OK, data=resp)
    else:
        return jsonify(success=RET.WRONG, data="没有接收到手机号")


@api.route('/users/sign_out', methods=['GET'])
def sign_open_out():
    """用户出入
        """
    username = request.args.get('username')
    if username:
        resp = huoqusign(username)
        return jsonify(success=RET.OK, data=resp)
    else:
        return jsonify(success=RET.WRONG, data="没有接收到手机号")


@api.route('/users/sign_qian', methods=['GET'])
def sign_open_qian():
    """用户出入签到
        """
    # data = request.args.get("data")
    # a = data.split("|")[0]
    # b = a.split(".")
    # if len(b[1]) == 11:
    #     localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     ren = Users.query.filter(Users.username == b[0]).first()
    #     if ren:
    #         try:
    #             waichu = Waichu()
    #             waichu.username = b[0]
    #             waichu.create_time = localtime
    #             waichu.full_name = ren.full_name
    #             db.session.add(waichu)
    #             db.session.commit()
    #         except:
    #             return jsonify(success=RET.WRONG, data="录入信息失败")
    #     else:
    #         return jsonify(success=RET.OK, data="查不到此人信息")
    #     data = "{},出入信息已经录入".format(ren.full_name)
    #     return jsonify(success=RET.OK, data=data)
    # else:
    #     localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     t = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    #     y, m, d = t[0:3]
    #     yan = Yanzheng2.query.filter(Yanzheng2.username == str(b[0]),
    #                                           extract('year', Yanzheng2.create_time) == y,
    #                                           extract('month', Yanzheng2.create_time) == m,
    #                                           extract('day', Yanzheng2.create_time) == d).first()
    #     # print ss[0],ss[1]
    #     try:
    #         ren = Users.query.filter(Users.username == b[0]).first()
    #         if yan:
    #             yan.update_time = localtime
    #             db.session.commit()
    #         else:
    #             yan = Yanzheng2()
    #             yan.full_name = ren.full_name
    #             yan.username = b[0]
    #             yan.create_time = localtime
    #             db.session.add(yan)
    #             db.session.commit()
    #         data = "{},路上注意安全".format(ren.full_name)
    #         return jsonify(success=RET.OK, data=data)
    #     except:
    #         return jsonify(success=RET.WRONG, data="录入信息失败")
    data = request.args.get("data")
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ren = Users.query.filter(Users.username == data).first()
    t = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    y, m, d = t[0:3]
    yan = Yanzheng2.query.filter(Yanzheng2.username == str(data),extract('year', Yanzheng2.create_time) == y, extract('month', Yanzheng2.create_time) == m, extract('day', Yanzheng2.create_time) == d).first()
    if ren:
        # try:
        waichu = Waichu()
        waichu.username = data
        waichu.create_time = localtime
        waichu.full_name = ren.name
        if yan:
            yan.update_time = localtime
        db.session.add(waichu)
        db.session.commit()
        # except:
        #     return jsonify(success=RET.WRONG, data="录入信息失败")
    else:
        return jsonify(success=RET.OK, data="查不到此人信息")
    dat = "{},出入信息已经录入".format(ren.name)
    return jsonify(success=RET.OK, data=dat)





@api.route('/users/pw', methods=['GET'])
def password_xiu():
    """用户修改密码
        """
    open_id = request.args.get('open_id')
    username = request.args.get('username')
    password = request.args.get('password')

    user = Users.query.filter(Users.open_id==open_id).first()
    if user.username != username:
        return jsonify(success=RET.WRONG, data="请用自己的微信登陆")
    else:
        user.password = password
    db.session.commit()
    return jsonify(success=RET.OK, data="修改密码成功")