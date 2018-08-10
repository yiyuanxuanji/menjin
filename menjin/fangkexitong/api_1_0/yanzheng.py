# coding=utf-8
# 导入蓝图对象
from . import api
# 导入flask内置的对象
from flask import  jsonify, request
from fangkexitong import db
# 导入自定义状态码
from fangkexitong.utils.response_code import RET
# 导入模型类
from fangkexitong.models import Yanzheng2, Users, Yanzheng, Invitation
# 导入json模块
import json, re
# 导入日期模块
import datetime, time
from sqlalchemy import extract
import requests
import json,datetime,time,hashlib,re
from .huoquyonghu import huoqutime

@api.route('/users/qiandao', methods=['GET'])
def yanzheng():
#     today = datetime.date.today()
#     tomorrow = today + datetime.timedelta(days=1)
#     today = today.strftime('%Y-%m-%d')
#     tomorrow = tomorrow.strftime('%Y-%m-%d')
#     else:
#         return jsonify(success=RET.WRONG, data="对不起你没有权限")
#
#     return jsonify(success=RET.OK, data="请进")

    username = request.args.get("username")
    time.sleep(1)
    shijian = huoqutime(username)
    t = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    y, m, d = t[0:3]
    yan = Yanzheng2.query.filter(Yanzheng2.username==username, extract('year', Yanzheng2.create_time) == y,extract('month', Yanzheng2.create_time) == m,extract('day', Yanzheng2.create_time) == d).first()

    if yan:
        yan.update_time = shijian
        db.session.commit()
        return jsonify(success=RET.OK, data="请进")
    else:
        yan = Yanzheng2()
        yan.username = username
        yan.create_time = shijian
        db.session.add(yan)
        db.session.commit()
        return jsonify(success=RET.OK, data="签到成功")

@api.route('/users/yanzheng', methods=['GET'])
def postg_visitors():
    """
      需求受邀人的open_id,  邀请函id
    :return:
      """
    info_data = request.args.get("info_data")

    datas = Yanzheng.query.filter(Yanzheng.info_data == info_data,Yanzheng.cishu !=0).all()
    invit = Invitation.query.filter_by(info_data=info_data).first()

    # if invit is None:
    #     return jsonify(success=RET.WRONG, data="邀请函没了")
    invit_id = invit.id
    data_list = []
    for data in datas:
        data_info = eval(data.info)
        data_info["id"] = data.id
        data_list.append(data_info)
    # if data is None:
    #     return jsonify(success=RET.WRONG, data="对不起,你没有权限")
    # data_re = {"success":1,"data":data.info}
    # data_res = json.dumps(data_re)
    # return data_res
    invit.state = "进行中".encode("utf-8")
    db.session.commit()
    return jsonify(success=RET.OK, data=data_list, id = invit_id)