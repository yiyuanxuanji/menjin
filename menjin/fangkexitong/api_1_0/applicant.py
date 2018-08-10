# coding=utf-8
# 导入蓝图对象
from . import api
# 导入flask内置的对象
from flask import current_app, jsonify, request
from fangkexitong import db
# 导入自定义状态码
from fangkexitong.utils.response_code import RET
# 导入模型类
from fangkexitong.models import Users, Invitation, InvitingPerson, Applicant, Visitors, PersonOpen
# 导入json模块
import json, re
# 导入日期模块
import datetime


@api.route('/users/applicant', methods=['GET'])
def get_applicant():
    """
    申请拜访界面
    :return:
    """
    try:
        open_id = request.args.get("open_id")
        if open_id is None:
            return jsonify(success=RET.WRONG, data='参数缺失')
        invitingperson = InvitingPerson.query.filter_by(open_id=open_id).first()  # 根据open_id查询数据
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询数据库失败')
    if invitingperson is None:
        return jsonify(success=RET.WRONG, data='你没有拜访权限')
    return jsonify(success=RET.OK, data=invitingperson.inviting_info())


@api.route('/users/applicant1', methods=['GET'])
def post_applicant():
    """
    申请拜访界面
    :return:
    """
    try:
        # 获取post请求的json字符串
        # info_data = request.get_json()
        # # 检查参数的存在
        # if not info_data:
        #     return jsonify(jsonify(success=RET.WRONG, data='没有获取到数据'))
        company = request.args.get("company")
        invit_name = request.args.get("invit_name")
        visit_time = request.args.get("visit_time")
        reason = request.args.get("reason")
        full_name = request.args.get("full_name")
        phone = request.args.get("phone")
        ap_company = request.args.get("ap_company")
        if not all([full_name, phone, company, visit_time, invit_name, reason, ap_company]):  # 此处没有写图片,图片可以为空
            return jsonify(jsonify(success=RET.WRONG, data='数据不完整'))
        personopen = PersonOpen.query.filter_by(user_name=invit_name).first()
        if personopen is None:
            return jsonify(success=RET.WRONG, data='你要拜访的人不存在')
        applicant = Applicant()
        applicant.full_name = full_name
        applicant.phone = phone
        applicant.ap_company = ap_company
        applicant.company = company
        applicant.invit_name = invit_name
        applicant.reason = reason
        applicant.visit_time = visit_time
        applicant.user_id = personopen.user_id
        applicant.state = "待审核"
        db.session.add(applicant)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 写入如果发生异常,需要进行回滚
        db.session.rollback()
        return jsonify(success=RET.WRONG, data='写入数据库失败')
    return jsonify(success=RET.OK, data={"id": applicant.id})


@api.route('/users/authed', methods=['GET'])
def get_auth():
    """
    审核拜访界面
    :return:
    """
    try:
        # 获取post请求的json字符串
        info_data = request.get_json()
        ap_id = info_data.get("id")
        # 检查参数的存在
        if not info_data:
            return jsonify(jsonify(success=RET.WRONG, data='没有获取到数据'))
        applicant = Applicant.query.filter_by(id=ap_id).first()
        if applicant is None:
            return jsonify(success=RET.WRONG, data='没有该访客的审核')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='读取数据库失败')
    return jsonify(success=RET.OK, data=applicant.examine())


@api.route('/users/authed1', methods=['GET'])
def post_auth():
    """
    审核拜访界面
    :return:
    """
    try:
        # # 获取post请求的json字符串
        # info_data = request.get_json()
        # # 检查参数的存在
        # if not info_data:
        #     return jsonify(jsonify(success=RET.WRONG, data='没有获取到数据'))
        auth_id = request.args.get("id")
        applicant = Applicant.query.filter_by(id=auth_id).first()
        if applicant is None:
            return jsonify(success=RET.WRONG, data='没有该访客的审核')
        applicant.state = "已审核"
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='读取数据库失败')
    return jsonify(success=RET.OK, data="审核成功")
