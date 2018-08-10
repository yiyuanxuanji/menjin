# coding=utf-8
# 导入蓝图对象
from . import api
# 导入flask内置的对象
from flask import current_app, jsonify, g, request
from fangkexitong import db
# 导入自定义状态码
from fangkexitong.utils.response_code import RET
# 导入模型类
from fangkexitong.models import Invitation, InvitingPerson, PersonOpen, Visitors, Applicant, Users, Yanzheng, Blacklist
# 导入json模块
import json, re, time, random
# 导入日期模块
import datetime
from .sqlcha import session
from erweimatupian import fangkeerweima

@api.route('/users/carry', methods=['GET'])
def get_infomation():
    """访客登记:以往的访客自动填充
    :return:
    """
    # 获取参数
    open_id = request.args.get("open_id")
    invit_id = request.args.get("invit_id")
    if not all([open_id,invit_id]):
        return jsonify(success=RET.WRONG, data='参数缺失')
    try:
        #  根据open_id查询数据
        invit = Invitation.query.filter(Invitation.id == invit_id).first()
        # yanz = Yanzheng.query.filter(Yanzheng.info_data == invit.info_data).all()
        # if len(yanz) != 0:
        #     if len(yanz) >= int(invit.visitor_count):
        #         return jsonify(success=RET.DBERR, data="邀请函人数已满")
        invitingperson = InvitingPerson.query.filter_by(open_id=open_id).first()
        if not invitingperson:
            data = {
                "full_name": invit.full_name
            }

            return jsonify(success=RET.OK, data=data)
        personopens = PersonOpen.query.filter_by(inperson_id=open_id, invit_id=invit_id, dele=False).filter(PersonOpen.visitor_id != "").all()
        # if not personopens:
        #     return jsonify(success=RET.WRONG, data='没有用户信息')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询数据库失败')
    try:
        blacklist = Blacklist.query.filter_by(open_id=open_id).first()
    except:
        return jsonify(success=RET.WRONG, data='查询数据库失败')
    if blacklist:
        return jsonify(success=RET.DBERR, data="你已被加入黑名单")


    # if invit.state == "已生效":
    #     return jsonify(success=RET.OK, data="邀请函已被使用")
    # if invitingperson is None:
    #     return jsonify(success=RET.WRONG, data='没有用户信息')
    data = [invitingperson.inviting_info()]
    if personopens is None:
        return jsonify(success=RET.OK, data=data)
    else:
        for personopen in personopens:
            visitor = Visitors.query.filter_by(id=personopen.visitor_id).first()
            info = visitor.visitor_info()
            data.append(info)


    return jsonify(success=RET.OK, data=data)


@api.route('/users/carry/<int:idx>', methods=['POST'])
def post_infomationpost(idx):
    """
      访客登记,第一个访客是受邀人,需要保存到受邀人表,后面的需要保存到受访人表
      :return:
      """
    # 获取post请求的json字符串

    carry_data = request.get_json()
    # 检查参数的存在
    if not carry_data:
        return jsonify(success=RET.WRONG, data='携带访客数据录入失败')
    # 获取详细的参数信息
    data = []
    invit_id = carry_data.get('invit_id')
    open_id = carry_data.get("open_id")

    try:
        invit = Invitation.query.filter_by(id=invit_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询邀请函信息失败')
    user_id = invit.user_id  # 用户名
    user = Users.query.filter_by(id=user_id).first()

    user_name = user.name
    user_comp = user.company
    #  访客可能不是一个人,总是列表
    datainfo = carry_data.get("data")
    if 0 == len(datainfo):
        return jsonify(success=RET.WRONG, data='没有接收到填写数据')
    for i in range(0, len(datainfo)):
        # invit_id = carry_data[i].get('invit_id')
        full_name = carry_data[i].get('full_name')
        phone = carry_data[i].get('phone')
        email = carry_data[i].get('email')
        id_type = carry_data[i].get('id_type')
        id_num = carry_data[i].get('id_num')
        company = carry_data[i].get('company')
        if not all([full_name, phone, email, id_num, id_type, company]):
            return jsonify(success=RET.WRONG, data='数据不全')
        if i == 0:  # 查询数据库看是否已经存在  第一个需要添加到受邀人的表

            try:
                invitperon = InvitingPerson.query.filter_by(open_id=open_id,full_name=full_name, phone=phone).first()
                if invitperon is None:
                    invitperon = InvitingPerson()
                    invitperon.full_name = full_name
                    invitperon.phone = phone
                    invitperon.email = email
                    invitperon.id_type = id_type
                    invitperon.id_num = id_num
                    invitperon.company = company
                    db.session.add(invitperon)

                personopen = PersonOpen.query.filter_by(inperson_id=open_id, invit_id=invit_id, user_id=user_id).first()
                if personopen is None:
                    personopen = PersonOpen()
                    personopen.inperson_id = open_id
                    personopen.invit_id = invit_id
                    personopen.inperson_name = full_name
                    personopen.user_id = user_id
                    personopen.user_name = user_name
                    personopen.user_comp = user_comp
                    db.session.add(personopen)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(success=RET.WRONG, data='查询用户信息失败')
            data.append(invitperon.inviting_info())
        if i != 0:  # 查询数据库看是否已经存在     后面的受访人放到受访人的表
            try:
                visitor = Visitors.query.filter_by(full_name=full_name, phone=phone).first()
                if visitor is None:
                    visitor = Visitors()
                    visitor.full_name = full_name
                    visitor.phone = phone
                    visitor.email = email
                    visitor.id_type = id_type
                    visitor.id_num = id_num
                    visitor.company = company
                    visitor.inperson_id = open_id
                    db.session.add(visitor)
                visitor_id = visitor.id
                personopen = PersonOpen.query.filter_by(inperson_id=open_id, invit_id=invit_id, user_id=user_id, visitor_id=visitor_id).first()
                if personopen is None:
                    personopen = PersonOpen()
                    personopen.inperson_id = open_id
                    personopen.invit_id = invit_id
                    personopen.inperson_name = full_name
                    personopen.user_id = user_id
                    personopen.user_name = user_name
                    personopen.user_comp = user_comp
                    personopen.visitor_id = visitor_id
                    db.session.add(personopen)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(success=RET.WRONG, data='查询用户信息失败')
            data.append(visitor.visitor_info())
        try:
            db.session.commit()               # 数据库事务
        except Exception as e:
            current_app.logger.error(e)
            # 写入如果发生异常,需要进行回滚
            db.session.rollback()
            return jsonify(success=RET.WRONG, data='保存用户信息失败')

    if 1 == idx:
        invit = Invitation.query.filter_by(id=invit_id).first()
        count = invit.visitor_count
        # if count > len(datainfo) and not count is None:    # 这里是否需要判断人数问题
        #     return jsonify(success=RET.WRONG, data='人数太多')
        invit.state = "已生效"
        db.session.commit()
        # data.append({"invit_id": invit_id})
        return jsonify(success=RET.OK, data=data)
    else:
        return jsonify(success=RET.OK, inperson_id=open_id, invit_id=invit_id)



@api.route('/users/carry1/<int:idx>', methods=['GET'])
def post_infomation(idx):
    """
      访客登记,第一个访客是受邀人,需要保存到受邀人表,后面的需要保存到受访人表
      :return:
      """

    invit_id = request.args.get('invit_id')
    open_id = request.args.get("open_id")
    open_id = str(open_id)
    if not all([invit_id,open_id]):
        return jsonify(success=RET.WRONG, data='参数缺失')
    try:
        invit = Invitation.query.filter_by(id=invit_id).first()
        # if invit.info_data:
        #     yanzheng = Yanzheng.query.filter(Yanzheng.info_data == invit.info_data).all()
        #     # if invit.visitor_count:
            #     if invit.visitor_count == len(yanzheng):
            #         return jsonify(success=RET.WRONG, data='这张邀请函人数已达上限')


    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询邀请函信息失败')
    user_id = invit.user_id  # 用户名
    user = Users.query.filter_by(id=user_id).first()
    user_name = user.name
    user_comp = user.company_id
    invit_count = invit.visitor_count
    #  访客可能不是一个人,总是列表

    # invit_id = carry_data[i].get('invit_id')
    full_name = request.args.get('full_name')
    phone = request.args.get('phone')
    email = request.args.get('email')
    id_type = request.args.get('id_type')
    id_num = request.args.get('id_num')
    company = request.args.get('company')
    if not all([full_name]):
        return jsonify(success=RET.WRONG, data='用户信息不完整')

    # 查询数据库看是否已经存在  第一个需要添加到受邀人的表
    try:
        # invitperon = InvitingPerson.query.filter_by(open_id=open_id,full_name=full_name, phone=phone).first()
        invitperon = InvitingPerson.query.filter_by(open_id=open_id).first()
        if invitperon is None:
            invitperon = InvitingPerson()
            invitperon.open_id = open_id
            invitperon.full_name = full_name
            invitperon.phone = phone
            invitperon.email = email
            invitperon.id_type = id_type
            invitperon.id_num = id_num
            invitperon.company = company
            db.session.add(invitperon)
        else:
            invitperon.full_name = full_name
            invitperon.phone = phone
            invitperon.email = email
            invitperon.id_type = id_type
            invitperon.id_num = id_num
            invitperon.company = company
            db.session.commit()

        personopen = PersonOpen.query.filter_by(inperson_id=open_id, invit_id=invit_id, user_id=user_id).first()
        if personopen is None:
            personopen = PersonOpen()
            personopen.inperson_id = open_id
            personopen.invit_id = invit_id
            personopen.inperson_name = full_name
            personopen.user_id = user_id
            personopen.user_name = user_name
            personopen.user_comp = user_comp
            personopen.visit_time = invit.visit_time
            db.session.add(personopen)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='写入用户信息失败')

    heiming = Blacklist.query.filter(Blacklist.full_name == full_name,Blacklist.id_num==id_num).first()
    if heiming != None:
        return jsonify(success=RET.WRONG, data="你已被加入黑名单")



    data = {
        "open_id":open_id,
        "company":company,
        "user_name":user_name,
        "check_in":"{}".format(invit.company)+"{}".format(invit.position)+str(invit.check_in),
        "visit_time":invit.visit_time.strftime('%Y-%m-%d %H-%M'),
        "full_name":full_name,
        "id_num":id_num,
    }
        # if i != 0:  # 查询数据库看是否已经存在     后面的受访人放到受访人的表
        #     try:
        #         visitor = Visitors.query.filter_by(full_name=full_name, phone=phone).first()
        #         if visitor is None:
        #             visitor = Visitors()
        #             visitor.full_name = full_name
        #             visitor.phone = phone
        #             visitor.email = email
        #             visitor.id_type = id_type
        #             visitor.id_num = id_num
        #             visitor.company = company
        #             visitor.inperson_id = open_id
        #             db.session.add(visitor)
        #         visitor_id = visitor.id
        #         personopen = PersonOpen.query.filter_by(inperson_id=open_id, invit_id=invit_id, user_id=user_id, visitor_id=visitor_id).first()
        #         if personopen is None:
        #             personopen = PersonOpen()
        #             personopen.inperson_id = open_id
        #             personopen.invit_id = invit_id
        #             personopen.inperson_name = full_name
        #             personopen.user_id = user_id
        #             personopen.user_name = user_name
        #             personopen.user_comp = user_comp
        #             personopen.visitor_id = visitor_id
        #             db.session.add(personopen)
        #     except Exception as e:
        #         current_app.logger.error(e)
        #         return jsonify(success=RET.WRONG, data='查询用户信息失败')
        #     data.append(visitor.visitor_info())


    if 1 == idx:
        try:
            # 数据库事务
            invit.state = "已生效".decode('utf-8')
            if invit.info_data is None:
                # import hashlib
                # m = hashlib.md5()
                time_vi = invit.visit_time.strftime("%Y-%m-%d %H:%M:%S")
                invit.info_data = fangkeerweima(visitor_time=time_vi)
                # a = invit.info_data.encode()
                # m.update(a)
                # invit.info_data = m.hexdigest()
            yanzheng = Yanzheng.query.filter(Yanzheng.info_data == invit.info_data,Yanzheng.open_id==open_id).first()
            if yanzheng is None:
                yanzheng = Yanzheng()
                yanzheng.info = str(data)
                yanzheng.open_id = open_id
                yanzheng.info_data = invit.info_data
                yanzheng.cishu = 999
                db.session.add(yanzheng)
            yanzheng.info = str(data)
            db.session.commit()


        except Exception as e:
            current_app.logger.error(e)
            # 写入如果发生异常,需要进行回滚
            db.session.rollback()
            return jsonify(success=RET.WRONG, data='保存用户信息失败')
        return jsonify(success=RET.OK, data=yanzheng.info_data)
    else:
        return jsonify(success=RET.OK, inperson_id=open_id, invit_id=invit_id)

@api.route('/users/visitor', methods=['POST'])
def post_visitor():
    """
      访客登记,需求受邀人的open_id,  邀请函id
    :return:
      """
    carry_data = request.get_json()
    # 检查参数的存在
    if not carry_data:
        return jsonify(success=RET.WRONG, data='携带访客数据录入失败')
    # 获取详细的参数信息
    open_id = carry_data.get('open_id')        # 其实就是open_id
    invit_id = carry_data.get('invit_id')      # 对应邀请函的id
    info_list = carry_data.get('data')
    try:
        invit = Invitation.query.filter_by(id=invit_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询邀请函信息失败')
    user_id = invit.user_id  # 用户名
    user = Users.query.filter_by(id=user_id).first()
    user_name = user.name
    user_comp = user.company_id
    for i in range(0, len(info_list)):
        # inperson_id = carry_data[i].get('open_id')
        full_name = carry_data[i].get('full_name')
        phone = carry_data[i].get('phone')
        email = carry_data[i].get('email')
        id_type = carry_data[i].get('id_type')
        id_num = carry_data[i].get('id_num')
        company = carry_data[i].get('company')
        if not all([full_name, phone,  id_num, id_type]):
            return jsonify(success=RET.WRONG, data='数据不全')
        try:
            visitor = Visitors.query.filter_by(full_name=full_name, phone=phone).first()
            if visitor is None:
                visitor = Visitors()
                visitor.full_name = full_name
                visitor.phone = phone
                visitor.email = email
                visitor.id_type = id_type
                visitor.id_num = id_num
                visitor.company = company
                visitor.inperson_id = open_id
                db.session.add(visitor)
            visitor_id = visitor.id
            personopen = PersonOpen()
            personopen.inperson_id = open_id
            personopen.invit_id = invit_id
            personopen.inperson_name = full_name
            personopen.user_id = user_id
            personopen.user_name = user_name
            personopen.user_comp = user_comp
            personopen.visitor_id = visitor_id
            db.session.add(personopen)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(success=RET.WRONG, data='保存用户信息失败')
    db.session.commit()
    return jsonify(success=RET.OK, data="保存成功")



@api.route('/users/visitors1', methods=['GET'])
def post_visitors():
    """
      访客登记,需求受邀人的open_id,  邀请函id
    :return:
      """
    # carry_data = request.get_json()
    # # 检查参数的存在
    # if not carry_data:
    #     return jsonify(success=RET.WRONG, data='携带访客数据录入失败')
    # 获取详细的参数信息
    open_id = request.args.get('open_id')   # 其实就是open_id
    invit_id = request.args.get('invit_id')         # 对应邀请函的id

    try:
        invit = Invitation.query.filter_by(id=invit_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询邀请函信息失败')
    user_id = invit.user_id  # 用户名
    user = Users.query.filter_by(id=user_id).first()
    user_name = user.name
    user_comp = user.company_id

    # inperson_id = carry_data[i].get('open_id')
    full_name = request.args.get('full_name')
    phone = request.args.get('phone')
    email = request.args.get('email')
    id_type = request.args.get('id_type')
    id_num = request.args.get('id_num')
    company = request.args.get('company')
    if not all([full_name, phone, id_num, id_type, company]):
        return jsonify(success=RET.WRONG, data='数据不全')
    try:
        visitor = Visitors.query.filter_by(full_name=full_name, phone=phone).first()
        if visitor is None:
            visitor = Visitors()
            visitor.full_name = full_name
            visitor.phone = phone
            visitor.email = email
            visitor.id_type = id_type
            visitor.id_num = id_num
            visitor.company = company
            visitor.inperson_id = open_id
            db.session.add(visitor)
        visitor_id = visitor.id
        personopen = PersonOpen()
        personopen.inperson_id = open_id
        personopen.invit_id = invit_id
        personopen.inperson_name = full_name
        personopen.user_id = user_id
        personopen.user_name = user_name
        personopen.user_comp = user_comp
        personopen.visitor_id = visitor_id
        db.session.add(personopen)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询用户信息失败')
    db.session.commit()
    return jsonify(success=RET.OK, data="保存成功")

@api.route('/users/defect1', methods=['GET'])    # 功能为写入文档
def del_visitors():
    """
      访客删除
    :return:
      """
    # info_data = request.get_json()
    # # 检查参数的存在
    # if not info_data:
    #     return jsonify(success=RET.WRONG, data='携带访客数据录入失败')
    # 获取详细的参数信息
    open_id = request.args.get('open_id')
    invit_id = request.args.get('invit_id')
    visitor_id = request.args.get('id')
    try:
        personopen = PersonOpen.query.filter_by(inperson_id=open_id, invit_id=invit_id, visitor_id=visitor_id).first()
        personopen.dele = True
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(success=RET.WRONG, data='查询用户信息失败')
    return jsonify(success=RET.OK, data="删除成功")
