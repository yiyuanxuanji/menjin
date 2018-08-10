# coding=utf-8
from .erweimatupian import huoquerweima
# 导入蓝图对象
from . import api
# 导入flask内置的对象
from flask import current_app, jsonify, request
from fangkexitong import db
# 导入自定义状态码
from fangkexitong.utils.response_code import RET
# 导入模型类
from fangkexitong.models import Users, Invitation, InvitingPerson, Applicant, Visitors, PersonOpen, Limit_visitor
# 导入json模块
import json, re
# 导入日期模块
import datetime, time
import os
from flask import make_response
import hashlib



@api.route('/users/login', methods=['GET'])
def login_open_id():
    """用户登陆
        """
    open_id = request.args.get('open_id')
    if open_id:
        user = Users.query.filter(Users.open_id==open_id).first()
        if user:
            username = user.username
            password = user.password
            data = {
                "username":username,
                "password":password
            }
            return jsonify(success=RET.OK, data=data)
        else:
            return jsonify(success=RET.OK, data="")
    else:
        return jsonify(success=RET.OK, data="")



@api.route('/users/login1', methods=['GET'])
def login():
    """
    用户登陆
    """
    open_id = request.args.get('open_id')
    username = request.args.get('username')
    password = request.args.get('password')

    # 检查参数的完整性
    if not all([username, password]):
        return jsonify(success=RET.WRONG, data='数据缺失!')
    # 查询数据库
    try:
        user = Users.query.filter_by(username=username).first()  # 这个库不再我这可能有问题  # 用户名
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='账号密码不正确!')
    # 判断查询结果,对密码进行检查
    if user is None or user.password != password:
        return jsonify(success=0, data='账号密码不正确!')
    # 返回正确的用户名
    # resp = huoquerweima(username)
    if user.open_id == "":
        user.open_id = open_id
        db.session.commit()
    return jsonify(success=RET.OK, id = user.id, username=username)



@api.route('/users/invitemo', methods=['GET'])
def list_invite_mo():
    """
    访客邀请默认
    :return:
    """

    user_id = request.args.get('user_id')

    try:
        invitation = Invitation.query.filter(Invitation.user_id==user_id).order_by(
                Invitation.id.desc()).first()
        # user = Users.query.filter_by(id=user_id).first()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.DBERR, data='查询数据异常')
    if invitation:
        data = {"idx": invitation.id,
                "visit_time": invitation.visit_time.strftime('%Y-%m-%d %H-%M'),
                "position": invitation.position,
                "company":invitation.company,
                "full_name": invitation.full_name,
                "visitor_count": invitation.visitor_count,
                "reason": invitation.reason,
                "phone": invitation.phone,
                "check_in": invitation.check_in,
                "user_name":invitation.user_fullname,
                "user_phone":invitation.user_phone,
                "time":invitation.create_time.strftime('%Y-%m-%d'),
                }
        return jsonify(success=RET.OK, data=data)
    else:
        return jsonify(success=RET.OK, data="")


@api.route('/users/invite1', methods=['GET'])
def get_invite():
    """
    邀请函生成,
    :return:
    """
    # # 获取post请求的json字符串
    # invite_data = request.get_json()
    # # 检查参数的存在
    # if not invite_data:
    #     return jsonify(jsonify(success=RET.WRONG, data='参数缺失'))
    # 获取详细的参数信息
    user_id = request.args.get('user_id')   # 用户名
    full_name = request.args.get('full_name')
    phone = request.args.get('phone')
    visitor_count = request.args.get('visitor_count')
    visit_time = request.args.get('visit_time')
    leaver_data = request.args.get('leaver_data')
    position = request.args.get('position')
    reason = request.args.get('reason')
    # image_url = request.args.get('image_url')
    company = request.args.get("company")
    check_in = request.args.get("check_in")
    jinzhi = ["过道", "前室", "女卫", "女卫生间", "男卫生间", "回收间", "电梯厅", "茶水间", "无障碍卫生间"]
    if position in jinzhi:
        return jsonify(success=RET.WRONG, data='地点不合适，已被限制')
    # 检查参数的完整性
    if not all([user_id,visit_time, check_in]):  # 此处没有写图片,图片可以为空
        return jsonify(success=RET.WRONG, data='用户信息不完整')
    # 保存用户实名信息到sqlserver数据库中
    # 时间处理，判断地点限制
    t = time.strptime(visit_time, "%Y-%m-%d %H:%M")
    y, m, d, h, s = t[0:5]
    visit_time = datetime.datetime(y, m, d, h, s)
    xingqi = t.tm_wday + 1 # 邀请的日子星期几
    limitzhou = Limit_visitor.query.filter(Limit_visitor.position == position, Limit_visitor.check_in == check_in).first()
    if limitzhou:
        t = time.strptime("1900-01-01", "%Y-%m-%d")
        y, m, d, = t[0:3]
        visit_time = datetime.datetime(y, m, d, h, s)
        if limitzhou.start_time <= visit_time and limitzhou.over_time >= visit_time and xingqi in limitzhou.zhouriqi:
            return jsonify(success=RET.WRONG, data='时间或者地点不合适，已被限制')
    limit = Limit_visitor.query.filter(Limit_visitor.position == position, Limit_visitor.check_in == check_in, Limit_visitor.start_time <= visit_time, Limit_visitor.over_time >= visit_time).first()
    if limit:
        return jsonify(success=RET.WRONG, data='时间或者地点不合适，已被限制')
    # invit = Invitation.query.filter(Invitation.visit_time == visit_time,Invitation.position==position).first()
    # if invit:
    #     return jsonify(success=RET.WRONG, data='地点已经被别人使用')

    try:
        user = Users.query.filter_by(id=user_id).first()

        # 构造模型类对象,准备保存用户信息
        invitation = Invitation()
        invitation.full_name = full_name
        invitation.phone = phone
        invitation.visitor_count = visitor_count
        invitation.visit_time = visit_time
        invitation.leave_data = leaver_data
        invitation.position = position
        invitation.reason = reason
        invitation.check_in = check_in
        invitation.user_id = user_id
        invitation.company = company
        invitation.state = "待接受".decode('utf-8')
        # 提交数据到数据库中
        invitation.user_fullname = user.name
        invitation.user_phone = user.mobile
        invitation.user_company = user.company_id
        # company    # 邀请人的公司没做
        db.session.add(invitation)
        db.session.commit()
        # g.invit_id = invitation.id
    except Exception as e:
        current_app.logger.error(e)
        # 写入如果发生异常,需要进行回滚
        db.session.rollback()
        return jsonify(success=RET.WRONG, data='保存用户信息失败')

    # 返回结果
    return jsonify(success=RET.OK, data={"auth_code": invitation.inviting_infomation()})


@api.route('/users/search/<int:sal>', methods=['GET'])
def list_visitor(sal):
    """
    访客邀请列表
    :return:
    """

    page = request.args.get("page")
    page = int(page)
    user_id = request.args.get('user_id')   # 获取发邀人的id

    rs_dict_list = []
    if 1 == sal:
        try:
            invits = Invitation.query.filter(Invitation.user_id == user_id).order_by(
                Invitation.create_time.desc()).paginate(page, 120, False)

            # 获取每一页的数据
            rs_list = invits.items
            #  获取一共多少页
            total_page = invits.pages
            # 定义容器,容器内字典
            for row in rs_list:
                rs_dict_list.append(row.inviting_object())
            # data ={"total_page":total_page,"data":rs_dict_list}
            return jsonify(success=RET.OK, total_page=total_page,data=rs_dict_list)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(success=RET.WRONG, data='查询数据异常')
    else:
        try:
            #  通过id查询的申请人的表
            applicant = Applicant.query.filter(Applicant.user_id == user_id).order_by(Applicant.create_time.desc()).paginate(page, 120, False)
            rs_page = applicant
            #  获取分页后的数据
            rs_list = rs_page.items
            #  获取一共多少页
            total_page = rs_page.pages
            # 定义容器,容器内字典
            for row in rs_list:
                rs_dict_list.append(row.inviting_object())
            return jsonify(success=RET.OK, data=rs_dict_list, total_page=total_page)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(success=RET.DBERR, data='查询数据异常')


@api.route('/users/invite', methods=['GET'])
def list_invite():
    """
    访客邀请展示
    :return:
    """
    invite_id = request.args.get('invit_id')
    # user_id = request.args.get('user_id')

    try:
        invitation = Invitation.query.filter_by(id=invite_id).first()
        # user = Users.query.filter_by(id=user_id).first()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.DBERR, data='查询数据异常')
    if not invitation:
        return jsonify(success=RET.WRONG, data='没有这张邀请函')


    data = {"idx": invitation.id,
            "visit_time": invitation.visit_time.strftime('%Y-%m-%d %H-%M'),
            "position": invitation.position,
            "full_name": invitation.full_name,
            "visitor_count": invitation.visitor_count,
            "reason": invitation.reason,
            "phone": invitation.phone,
            "check_in": invitation.check_in,
            "user_name":invitation.user_fullname,
            "user_phone":invitation.user_phone,
            "time":invitation.create_time.strftime('%Y-%m-%d'),
            "info_data":invitation.info_data
            }

    return jsonify(success=RET.OK, data=data)


@api.route('/users/push1', methods=['GET'])
def post_image():
    """
    后端下载图片
    :return:
    """
    #  获取json中的数据
    # info_data = request.get_json()
    # invite_id = request.args.get('invite_id')
    open_id = request.args.get('open_id')
    #  获取请求中的文件数据
    f = request.files['file']
    filename = open_id + ".jpg"
    f.save(os.path.join('fangkexitong/photo', filename))
    # f.save('app/static/' + str(filename))
    url = "fangkexitong/photo/" + filename
    return jsonify(success=RET.OK, data=url)


@api.route('/users/pull', methods=['GET'])
def poll_image():
    """
    前端请求图片
    :return:
    """
    #  获取json中的数据
    # info_data = request.get_json()
    open_id = request.args.get('open_id')
    filename = open_id + ".jpg"
    if os.path.isfile(os.path.join("fangkexitong/photo/", filename)):
        # url = "fangkexitong/photo/" + filename
        # return jsonify(success=RET.OK, data=url)

        image_data = open(os.path.join("fangkexitong/photo/" , filename), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return jsonify(success=RET.WRONG, data='没有图片')


@api.route('/users/menjin', methods=['GET'])
def get_menjin():
    """生成租户的二维码信息"""
    user_name = request.args.get('user_name')
    if user_name is None:
        return jsonify(success=RET.WRONG, data='没接收到参数')
    try:
        user = Users.query.filter(Users.mobile == user_name).first()
    except:
        return jsonify(success=RET.WRONG, data='查询数据失败')
    return jsonify(success=RET.OK, data=user.info)




# @api.route('/users/yanmenjin', methods=['GET'])
# def get_yanmenjin():
#     data = request.args.get("data")


