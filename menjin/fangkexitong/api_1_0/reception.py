# coding=utf-8
# 导入蓝图对象
from . import api
# 导入flask内置的对象
from flask import current_app, jsonify, g, request, session
from fangkexitong import db
# 导入自定义状态码
from fangkexitong.utils.response_code import RET
# 导入模型类
from fangkexitong.models import Invitation, InvitingPerson, PersonOpen, Visitors, Applicant, Users, Limit_visitor, Blacklist, Yanzheng

# 导入日期模块
import datetime,time
from sqlalchemy import extract
from dateutil import parser



@api.route('/recepost/index', methods=['GET'])
def get_reception_index():
    """
        后台首页
        :return:
        """
    yuefen = time.localtime().tm_mon
    nianfen = time.localtime().tm_year
    rizi = time.localtime().tm_mday
    yuefen = int(yuefen)+1
    list_data = []
    for i in range(5):
        yuefen = yuefen-1
        if yuefen == 0:
            yuefen =12
            nianfen = int(nianfen)-1

        xus = Invitation.query.filter(extract('month', Invitation.visit_time) <= yuefen,
                                          extract('year', Invitation.visit_time) == nianfen,extract('day', Invitation.visit_time) < rizi,
                                          Invitation.state == "进行中".decode()).all()
        for xu in xus:
            xu.state = "已过期".decode('utf-8')
        db.session.commit()



        # 受邀访客的数目
        zong = Invitation.query.filter(extract('month', Invitation.visit_time) == yuefen, extract('year', Invitation.visit_time) == nianfen).all()
        # 实际预防
        shiji = Invitation.query.filter(extract('month', Invitation.visit_time) == yuefen, extract('year', Invitation.visit_time) == nianfen,
                                        Invitation.state == "已生效".decode('utf-8')).all()
        # 再访访客
        zaifang = Invitation.query.filter(extract('month', Invitation.visit_time) == yuefen, extract('year', Invitation.visit_time) == nianfen,
                                          Invitation.state == "进行中".decode('utf-8')).all()
        # 离开
        likai = Invitation.query.filter(extract('month', Invitation.visit_time) == yuefen, extract('year', Invitation.visit_time) == nianfen,
                                        Invitation.state == "已过期".decode('utf-8')).all()
        data = {
            'yuefen':yuefen,
            'zong':len(zong),
            'shiji':len(shiji),
            'zaifang':len(zaifang),
            'likai':len(likai)
        }
        list_data.append(data)
    # 列表中最近的是最近月份的
    return jsonify(success=RET.OK, data=list_data)

@api.route('/recepost/info', methods=['GET'])
def get_reception_info():
    """
        前台查询到访人员,查询邀请函的具体信息
        :return:
        """
    datetime_struct = parser.parse("1900-01-01 00:00:00")
    page = request.args.get("page")
    page = int(page)
    # 今天的日子
    tmday = time.localtime().tm_mday
    yuefen = time.localtime().tm_mon
    nianfen = time.localtime().tm_year
    # 今天的访客
    zong = Invitation.query.filter(extract('year', Invitation.visit_time) == nianfen, extract('month', Invitation.visit_time) == yuefen,extract('day', Invitation.visit_time) == tmday, Invitation.state != "待接受".decode('utf-8')).all()
    data_jin = []
    for fang in zong:
        fangke = {
            "id" : fang.id,
            "visit_time": fang.visit_time.strftime('%Y-%m-%d %H:%M'),
            "position": fang.position,
            "visitor_count": fang.visitor_count,
            "check_in": fang.check_in,
            "user_company": fang.company,
        }
        data_jin.append(fangke)


    # 所有访客
    invits = Invitation.query.filter(Invitation.visit_time != datetime_struct, Invitation.state != "待接受".decode('utf-8')).order_by(Invitation.create_time.desc()).paginate(page, 120, False)
    # 获取每一页的数据
    rs_list = invits.items
    #  获取一共多少页
    total_page = invits.pages
    rs_dict_list = []
    for row in rs_list:
        rs_dict_list.append(row.inviting_infomation())
    return jsonify(success=RET.OK, data=rs_dict_list, total_page=total_page,data_jin = data_jin)


@api.route('/recepost/invitdel', methods=['GET'])
def get_reception_invitdel():
    """
        邀请函删除
        :return:
        """
    invit_id = request.args.get("invit_id")
    invit = Invitation.query.filter(Invitation.id == invit_id).first()
    yan = Yanzheng.query.filter(Yanzheng.info_data==invit.info_data).all()
    if invit:
        db.session.delete(invit)
    if len(yan) != 0:
        for i in yan:
            db.session.delete(i)
    db.session.commit()
    return jsonify(success=RET.OK, data="删除成功")













@api.route('/recepost/limit', methods=['GET'])
def get_reception_limit():
    """
        后台限制显示
        :return:
        """
    page = request.args.get("page")
    page = int(page)
    black_fangzhou = Limit_visitor.query.filter(Limit_visitor.leixing == "1").order_by(Limit_visitor.id.desc()).all()
    zhou_list = []
    for famg in black_fangzhou:
        # a = eval(famg.zhouriqi)
        # print a,type(a)
        zhouqi = []
        a = list(famg.zhouriqi.encode())
        for i in a:
            if i in ["0","1","2","3","4","5","6"]:
                zhouqi.append(int(i))
        riqi = zhouqi

        xingqi = ""
        if len(riqi)==7:
            xingqi = "每天"
        elif len(riqi)==5 and riqi[0]==1 and riqi[4]==5:
            xingqi = "每周工作日"
        else:
            for rizi in riqi:
                if rizi == 1:
                    rizi = "星期一 "
                elif rizi == 2:
                    rizi = "星期二 "
                elif rizi == 3:
                    rizi = "星期三 "
                elif rizi == 4:
                    rizi = "星期四 "
                elif rizi == 5:
                    rizi = "星期五 "
                elif rizi == 6:
                    rizi = "星期六 "
                elif rizi == 0:
                    rizi = "星期天 "
                xingqi += rizi
        xianshizhou = {
            "id": famg.id,
            "zhouriqi": xingqi,
            "start_time": famg.start_time.strftime('%H:%M'),
            "over_time": famg.over_time.strftime('%H:%M'),
            "position": famg.position,
            "check_in": famg.check_in,
            "cishu":famg.cishu,
            "leixing": "周期性限制"
        }
        zhou_list.append(xianshizhou)
    black_fang = Limit_visitor.query.filter(Limit_visitor.leixing == "2").order_by(Limit_visitor.id.desc()).paginate(page, 120, False)
    # 获取每一页的数据
    rs_list = black_fang.items
    #  获取一共多少页
    total_page = black_fang.pages
    rs_dict_list = []
    for row in rs_list:
        xianshi = {
            "id": row.id,
            "riqi": time.mktime(row.riqi.timetuple()),
            "start_time": row.start_time.strftime('%H:%M'),
            "over_time": row.over_time.strftime('%H:%M'),
            "position": row.position,
            "check_in": row.check_in,
            "cishu":row.cishu,
            "leixing": "临时性限制"
        }
        rs_dict_list.append(xianshi)
    return jsonify(success=RET.OK, datazhou = zhou_list ,data=rs_dict_list, total_page=total_page)

@api.route('/recepost/limitdel', methods=['GET'])
def get_reception_limitdel():
    """
        后台限制显示删除
        :return:
        """
    id = request.args.get("id")
    black_fang = Limit_visitor.query.filter(Limit_visitor.id == id).first()
    if black_fang:
        db.session.delete(black_fang)
        db.session.commit()
    return jsonify(success=RET.OK, data="删除成功")

@api.route('/recepost/xianzhi', methods=['GET'])
def get_reception_xianzhi():
    """
        后台限制添加
        :return:
        """
    riqi = request.args.get('riqi')
    start_time = request.args.get('start_time')
    over_time = request.args.get('over_time')
    position = request.args.get('position')
    check_in = request.args.get('check_in')
    cishu = request.args.get('cishu')
    cishu = str(cishu)
    if start_time == "":
        start_time = '00:00'
    if over_time == "":
        over_time = "23:59"

    try:
        t = time.strptime(riqi, "%Y-%m-%d")
        y, m, d, = t[0:3]
        riqi = datetime.datetime(y, m, d)
        leixing = "2"
        zhouriqi = ""
    except:
        zhouriqi = riqi
        zhouriqi = str(zhouriqi)
        t = time.strptime("1900-01-01", "%Y-%m-%d")
        y, m, d, = t[0:3]
        leixing = "1"
        riqi = ""
    t = time.strptime(start_time, "%H:%M")
    start_time = datetime.datetime(y, m, d, t.tm_hour, t.tm_min)
    t = time.strptime(over_time, "%H:%M")
    over_time = datetime.datetime(y, m, d, t.tm_hour, t.tm_min)

    # 需要专门写入一个表
    try:
        limit = Limit_visitor.query.filter(Limit_visitor.riqi == riqi, Limit_visitor.start_time == start_time, Limit_visitor.over_time == over_time, Limit_visitor.position == position, Limit_visitor.check_in == check_in, Limit_visitor.zhouriqi == zhouriqi).first()
        # limit = Limit_visitor.query.filter(Limit_visitor.position == position, Limit_visitor.check_in == check_in).all()
        # if riqi:
        #     if limit.riqi == riqi and limit.start_time == start_time and limit.over_time == over_time:
        #         return jsonify(success=RET.OK, data="地点限制已存在")
        # if zhouriqi:
        #     for ri in zhouriqi:
        #         riqi1 = []
        #         a = list(limit.zhouriqi.encode())
        #         for i in a:
        #             if i in ["0", "1", "2", "3", "4", "5", "6"]:
        #                 print i
        #                 riqi1.append(i)
        #         if ri in riqi1:
        #             return jsonify(success=RET.OK, data="地点限制有部分重复")
        if limit:
            return jsonify(success=RET.OK, data="地点限制已存在")
        limit = Limit_visitor()
        # print limit
        limit.riqi = riqi
        limit.zhouriqi = zhouriqi
        limit.start_time = start_time
        limit.over_time = over_time
        limit.position = position
        limit.check_in = check_in
        limit.leixing = leixing
        limit.cishu = cishu
        db.session.add(limit)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 写入如果发生异常,需要进行回滚
        db.session.rollback()
        return jsonify(success=RET.WRONG, data='保存用户信息失败')

    return jsonify(success=RET.OK, data="记录成功")


@api.route('/recepost/chaxun', methods=['GET'])
def get_reception_chaxun():
    """
        查询显示
        :return:
        """
    page = request.args.get("page")
    page = int(page)
    datetime_struct = parser.parse("1900-01-01 00:00:00")
    zong = Invitation.query.filter(Invitation.visit_time != datetime_struct).order_by(Invitation.create_time.desc()).paginate(page, 120, False)
    # 获取每一页的数据
    rs_list = zong.items
    #  获取一共多少页
    total_page = zong.pages
    rs_dict_list = []
    for row in rs_list:
        po = PersonOpen.query.filter(PersonOpen.invit_id == row.id).first()

        if po is None:
            continue
        invitson = InvitingPerson.query.filter(InvitingPerson.full_name == po.inperson_name, InvitingPerson.black == 0).first()
        if invitson is None:
            continue
        data = {
            "id" : row.id,
            "visit_time": row.visit_time.strftime('%Y-%m-%d %H:%M'),
            "user_company": row.company,
            "full_name":invitson.full_name,
            "phone": invitson.phone,
            "email": invitson.email,
            "shenfenhao":invitson.id_num,
            "weizhi":row.position,
            "renshu": row.visitor_count
        }
        rs_dict_list.append(data)
    return jsonify(success=RET.OK, data=rs_dict_list, total_page=total_page)


@api.route('/recepost/chaxun1', methods=['GET'])
def get_reception_chapost():
    """
        查询人名
        :return:
        """
    # data =request.get_json()
    # xingming = data['xingming']
    # shijian = data['shijian']
    xingming = request.args.get("xingming")
    shijian = request.args.get("shijian")
    overtime = request.args.get("overtime")
    list_cha = []

    datetime_struct = parser.parse("1900-01-01 00:00:00")
    if not all([xingming,shijian]):
        if xingming != "":

            shouyaoren = InvitingPerson.query.filter(InvitingPerson.full_name==xingming).first()
            yaoqing = PersonOpen.query.filter(PersonOpen.inperson_name==xingming, PersonOpen.visit_time != datetime_struct).all()
            for i in yaoqing:

                yaoqinghan = Invitation.query.filter(Invitation.id==i.invit_id, Invitation.visit_time != datetime_struct).first()
                if yaoqinghan:
                    dict_cha = {}
                    dict_cha['visit_time'] = yaoqinghan.visit_time.strftime('%Y-%m-%d %H:%M')
                    dict_cha['user_company'] = yaoqinghan.company
                    dict_cha['full_name'] = shouyaoren.full_name
                    dict_cha['phone'] = shouyaoren.phone
                    dict_cha['email'] = shouyaoren.email
                    dict_cha["shenfenhao"] = shouyaoren.id_num
                    dict_cha["id"] = yaoqinghan.id
                    dict_cha["weizhi"] = yaoqinghan.position
                    dict_cha["renshu"] = yaoqinghan.visitor_count
                    list_cha.append(dict_cha)
            return jsonify(success=RET.OK, data=list_cha)
        if shijian != "":
            a = []
            # 时间的处理
            t = time.strptime(shijian, "%Y-%m-%d")
            s = time.strptime(overtime, "%Y-%m-%d")
            y, m, d = t[0:3]
            y2,m2,d2 = s[0:3]
            if m == m2:
                yaoqinghan = Invitation.query.filter(extract('year', Invitation.visit_time) >= y,extract('month', Invitation.visit_time) >= m,extract('day', Invitation.visit_time) >= d, extract('year', Invitation.visit_time) <= y2,extract('month', Invitation.visit_time) <= m2,extract('day', Invitation.visit_time) <= d2).all()
            else:
                yaoqinghan1 = Invitation.query.filter(extract('year', Invitation.visit_time) >= y,
                                                     extract('month', Invitation.visit_time) >= m,extract('month', Invitation.visit_time) <= m2,extract('day', Invitation.visit_time) >= d,
                                                     ).all()
                yaoqinghan2 = Invitation.query.filter(extract('year', Invitation.visit_time) <= y2,extract('month', Invitation.visit_time) >= m,extract('month', Invitation.visit_time) <= m2,extract('day', Invitation.visit_time) <= d2,).all()
                yaoqinghan = yaoqinghan1+yaoqinghan2
            for i in yaoqinghan:
                guanxi = PersonOpen.query.filter(PersonOpen.invit_id == i.id, PersonOpen.visit_time != datetime_struct).first()
                if guanxi is None:
                    continue
                shouyaoren = InvitingPerson.query.filter(InvitingPerson.full_name==guanxi.inperson_name).first()
                if shouyaoren is None:
                    continue
                dict_cha = {}
                dict_cha['visit_time'] = i.visit_time.strftime('%Y-%m-%d %H:%M')
                dict_cha['user_company'] = i.company
                dict_cha['full_name'] = shouyaoren.full_name
                dict_cha['phone'] = shouyaoren.phone
                dict_cha['email'] = shouyaoren.email
                dict_cha["shenfenhao"] = shouyaoren.id_num
                dict_cha['id'] = i.id
                dict_cha["weizhi"] = i.position
                dict_cha["renshu"] = i.visitor_count
                # print dict_cha
                list_cha.append(dict_cha)
            return jsonify(success=RET.OK, data=list_cha)
        else:
            return jsonify(success=RET.WRONG, data='没有查到数据')

    else:
        t = time.strptime(shijian, "%Y-%m-%d")
        y, m, d = t[0:3]
        yaoqing = PersonOpen.query.filter(PersonOpen.inperson_name == xingming, extract('month', PersonOpen.visit_time) == m, extract('day', PersonOpen.visit_time) == d).all()
        shouyaoren = InvitingPerson.query.filter(InvitingPerson.full_name == xingming).first()
        for i in yaoqing:
            yaoqinghan = Invitation.query.filter(Invitation.id == i.invit_id, Invitation.visit_time != datetime_struct).first()
            if yaoqinghan:
                dict_cha = {}
                dict_cha['shijian'] = yaoqinghan.visit_time.strftime('%Y-%m-%d %H:%M')
                dict_cha['gongsi'] = yaoqinghan.company
                dict_cha['lianxiren'] = shouyaoren.full_name
                dict_cha['dianhua'] = shouyaoren.phone
                dict_cha['youxiang'] = shouyaoren.email
                dict_cha["shenfenhao"] = shouyaoren.id_num
                dict_cha['id'] = yaoqinghan.id
                dict_cha["weizhi"] = yaoqinghan.position
                dict_cha["renshu"] = yaoqinghan.visitor_count
                list_cha.append(dict_cha)
            else:
                continue
    return jsonify(success=RET.OK, data=list_cha)

@api.route('/recepost/shanchu', methods=['GET'])
def get_reception_shan():
    """
        删除操作
        :return:
        """
    invit_id = request.args.get("invit_id")
    inperson_name = request.args.get("inperson_name")
    yaoqing = PersonOpen.query.filter(PersonOpen.inperson_name == inperson_name,PersonOpen.invit_id==invit_id
                                      ).first()
    shouyaoren = InvitingPerson.query.filter(InvitingPerson.full_name == inperson_name).first()
    open_id =shouyaoren.open_id
    invit = Invitation.query.filter(Invitation.id == invit_id).first()

    info_data = invit.info_data
    yanzheng = Yanzheng.query.filter(Yanzheng.info_data == info_data, Yanzheng.open_id == open_id).first()
    try:
        db.session.delete(yanzheng)
        db.session.delete(yaoqing)
        db.session.commit()
        db.session.commit()
    except:
        return jsonify(success=RET.WRONG, data="删除失败")
    return jsonify(success=RET.OK, data="删除成功")


# @api.route("recepost/download", methods=['GET'])
# def download_file():
#     """
#     导出操作
#             :return:
#             """
#
#     return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
#                                           file_name=u"中文文件名")




@api.route('/recepost/update', methods=['GET'])
def get_reception_up():
    """
        更新操作
        :return:
        """

    yaoqingid = request.args.get('invit_id')
    shijian = request.args.get('shijian')
    t = time.strptime(shijian, "%Y-%m-%d %H:%M")
    y, m, d, h, s = t[0:5]
    visit_time = datetime.datetime(y, m, d, h, s)
    yaoqinghan = Invitation.query.filter(Invitation.id == yaoqingid).first()
    yaoqinghan.visit_time = visit_time
    yaoqingshijian = PersonOpen.query.filter(PersonOpen.invit_id == yaoqingid).first()
    yaoqingshijian.visit_time = visit_time
    db.session.commit()
    return jsonify(success=RET.OK, data="修改成功")





@api.route('/recepost/heimingdan', methods=['GET'])
def get_reception_heilie():
    """黑名单显示"""
    page = request.args.get("page")
    page = int(page)
    black_fang = Blacklist.query.filter().order_by(Blacklist.id.desc()).paginate(page, 120, False)
    # 获取每一页的数据
    rs_list = black_fang.items
    #  获取一共多少页
    total_page = black_fang.pages
    rs_dict_list = []
    for row in rs_list:
        dict_hei = {
            "id": row.id,
            "full_name": row.full_name,
            "id_num" : row.id_num,
            "company" : row.company,
            "phone" : row.phone
        }
        rs_dict_list.append(dict_hei)
    return jsonify(success=RET.OK, data=rs_dict_list, total_page=total_page)




@api.route('/recepost/heimingdan1', methods=['GET'])
def get_reception_heimingdan():
    """
        黑名单
        :return:
        """
    # data = request.get_json()
    # full_name = data['full_name']
    # id_num = data['id_num']
    # company = data['company']
    # phone = data['phone']
    full_name = request.args.get('full_name')
    id_num = request.args.get('id_num')
    company = request.args.get('company')
    phone = request.args.get('phone')
    try:
        invit_open = InvitingPerson.query.filter(InvitingPerson.full_name==full_name, InvitingPerson.id_num==id_num).first()
        open_id = invit_open.open_id
    except:
        return jsonify(success=RET.WRONG, data='此用户不在受邀访客里')

    try:
        black_fang = Blacklist.query.filter(Blacklist.full_name==full_name, Blacklist.id_num==id_num).first()
        if black_fang:
            return jsonify(success=RET.OK, data="已经添加过黑名单")
        black_fang = Blacklist()
        black_fang.full_name = full_name
        black_fang.id_num = id_num
        black_fang.company = company
        black_fang.phone = phone
        black_fang.open_id = open_id
        invit_open.black = 1
        db.session.add(black_fang)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 写入如果发生异常,需要进行回滚
        db.session.rollback()
        return jsonify(success=RET.WRONG, data='保存用户信息失败')
    return jsonify(success=RET.OK, data="记录成功")



@api.route('/recepost/heimingdel', methods=['GET'])
def get_reception_heimingdel():
    """
        删除黑名单
        :return:
        """
    id = request.args.get("id")
    black_fang = Blacklist.query.filter(Blacklist.id == id).first()
    invit_open = InvitingPerson.query.filter(InvitingPerson.open_id == Blacklist.open_id).first()
    if invit_open:
        invit_open.black = 0
    if black_fang:
        db.session.delete(black_fang)
        db.session.commit()
    return jsonify(success=RET.OK, data="删除成功")


