# -*- coding: utf-8 -*-
import requests
import json,datetime,time,hashlib,re
from sqlalchemy import extract
# from fangkexitong.api_1_0.sqlcha import session
# 导入:
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime


# 初始化数据库连接:
engine = create_engine("mssql+pymssql://visitor:12345678@cnspec.myds.me:61433/visitor", encoding='utf-8', echo=True)

# 创建对象的基类:
Base = declarative_base()


class Users(Base):
    """ 用户表"""
    __tablename__ = "mj_users"

    id = Column(Integer, primary_key=True)  # 编号
    username = Column(String(100), unique=True, nullable=False)  # 用户名
    password = Column(String(100), nullable=False)  # 密码
    name = Column(String(100), nullable=False)  # 姓名
    mobile = Column(String(100), nullable=False)  # 手机号
    company_id = Column(String(100), nullable=False)  # 公司的名称
    open_id = Column(String(100), nullable=True)  # open_id


    def info(self):
        info_data = {
            "username": self.username,
            "full_name": self.name,
            "company": self.company
        }
        return info_data

class Yanzheng2(Base):
    """ 用户验证表"""
    __tablename__ = "mj_yanzheng"

    id = Column(Integer, primary_key=True)  # 编号
    username = Column(String(100), unique=True, nullable=False)  # 用户名
    full_name = Column(String(100), nullable=False)  # 姓名
    create_time = Column(DateTime, nullable=True)  # 记录的创建时间
    update_time = Column(DateTime, nullable=True)  # 记录的更新时间

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()



def huoqutime():
    today = datetime.date.today()
    tomorrow  = today + datetime.timedelta(days=1)
    today = today.strftime('%Y-%m-%d')
    tomorrow = tomorrow.strftime('%Y-%m-%d')


    json_data = {
                "appkey": "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ",
                "time": "{}".format(int(time.time() * 1000)),
                "StartDate":"{}".format(today),
                "EndDate":"{}".format(tomorrow),
                "deviceId":"zykj001"
            }

    url = "http://office.600654tz.com/"
    static = "static/hardware/v2/getPassRecord"
    screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"


    data = static + str(json_data) + screct       # 加密准备
    # print(data)
    new_temp = data[0:len(data) - 1]
    m = hashlib.md5()                           # 加密对象
    m.update(new_temp.encode())
    sign = m.hexdigest().upper()                # 完成加密
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}      # 请求头
    response = requests.post(url=url+static+"?token="+sign, headers=headers, data="paramjson={}".format(json_data))
    # a = re.sub(r'\\\"',"'",response.text)
    # print(a)
    # return  a
    resp = eval(response.text)["JsonResult"]
    resps = eval(resp)["data"]
    # print(resps)
    # print (resps)
    s = []
    for res in resps:
        # print(res)
        if "USERNAME" in res:
            if len(res["USERNAME"]) == 11:
                # print(res["USERNAME"],res["BrushTime"])
                s.insert(0,[res["USERNAME"],res["BrushTime"]])

    t = time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    y, m, d = t[0:3]
    for ss in s:
        yan = session.query(Yanzheng2).filter(Yanzheng2.username == str(ss[0]), extract('year', Yanzheng2.create_time) == y,
                                     extract('month', Yanzheng2.create_time) == m,
                                     extract('day', Yanzheng2.create_time) == d).first()
        # print ss[0],ss[1]
        if yan:
            yan.update_time = ss[1]
            jilu = Yanzheng2()
            ren = session.query(Users).filter(Users.username == ss[0]).first()
            jilu.full_name = ren.name
            jilu.username = ss[0]
            jilu.create_time = ss[1]
            session.add(jilu)

            session.commit()
        else:
            yan = Yanzheng2()
            ren = session.query(Users).filter(Users.username == ss[0]).first()
            yan.full_name = ren.name
            yan.username = ss[0]
            yan.create_time = ss[1]
            session.add(yan)
            session.commit()


if __name__ == '__main__':
    huoqutime()
    time.sleep(3600*2)