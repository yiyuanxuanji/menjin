# -*- coding: utf-8 -*-
import sys,json,requests,time,hashlib,datetime
import sys
from imp import reload

reload(sys)




url = "http://office.600654tz.com/"
static = "static/hardware/v2/getPassQRCode"
screct = "VuqY1Ox*FB7@kVzZlo38WsH@wkE06Uo0"

json_data = {
    "appkey": "nJxZT$OgV@WrrO@xGqUecRKdxq*rnaZZ",
    "time": int(time.time() * 1000),
    "businessId": "1",
    "UserName": "18616841413",
    "AccessDate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "CodeType": "1"
}
print(json_data["time"])
data = static + str(json_data) + screct
new_temp = data[0:len(data) - 1]
m = hashlib.md5()
m.update(new_temp.encode())
sign = m.hexdigest().upper()
headers = {'Content-Type': 'application/x-www-form-urlencoded', }
response = requests.post(url=url + static + "?token=" + sign, headers=headers,
                         data="paramjson=+{}".format(json_data))

parkid = eval(response.text)["JsonResult"]
print(parkid)
parkid = eval(parkid)["data"]
# parkid = json.dumps(parkid,  ensure_ascii=False)
# parkid = "{}".format(parkid)

parkid = parkid.split("|")
parkid = parkid[0]+"00"+"|"+parkid[1]+"\\"
print(parkid)
# import qrcode
# img = qrcode.make("18616841413.100|0000002c0800008529539C925F3BEC9D8401238DF6DE394CFD35024A9DECDE8FCDE884DEA7AD21C8B9DC")
# img.save('./simpleqrcode.jpg')
# img.show()