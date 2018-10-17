import pymssql

server = '58.252.75.38'
port = '2466'
user = 'vip'
password = 'vip2015'
database = 'TTLP_01'


class WMS:

    def __init__(self):
        self.db = pymssql.connect(server=server, port=port, user=user, password=password, database=database)

    def query(self):
        sql = 'SELECT * FROM [USER]'

        cursor = self.db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        print(rows)


db = WMS()
db.query()




"""
@SmallPotY 天图这边的临时表：
CREATE TABLE [dbo].[Express_Trace_Temp](
	[Id] [int] IDENTITY(1,1) NOT NULL,	--自增ID
	[Express_No] [varchar](32) NOT NULL,	--快递单号
	[Express_Company] [varchar](20) NOT NULL,	--快递公司编码
	[Express_Status] [int] NULL,					--快递状态
	[Has_Signed] [int] NULL,							--是否签收
	[Trace_Context] [varchar](255) NULL,	--节点跟踪内容
	[Trace_Date_Time] [datetime] NULL,		--节点时间
	[Area_Name] [varchar](50) NULL,				--区域名称，如“上海市”
	[Process_Status] [int] NULL,					--状态，取数用
）
"""



{
	"message": "ok",
	"nu": "816236960521",
	"ischeck": "1",
	"condition": "F00",
	"com": "yuantong",
	"status": "200",
	"state": "3",
	"data": [{
		"time": "2018-09-16 13:48:39",
		"ftime": "2018-09-16 13:48:39",
		"context": "快件已签收 签收人: 他人代签, 四校代理点已签收，小秋为您竭诚服务，有问题请联系： 15083622574 感谢使用圆通速递，期待再次为您服务",
		"location": null
	}, {
		"time": "2018-09-16 13:33:20",
		"ftime": "2018-09-16 13:33:20",
		"context": "快件已到达冶金学校老校区旁快递服务中心妈妈驿站,联系电话18379002007",
		"location": null
	}, {
		"time": "2018-09-16 13:31:20",
		"ftime": "2018-09-16 13:31:20",
		"context": "江西省新余市河下镇公司派件人: 肖小崔（13979053898） 正在派件",
		"location": null
	}, {
		"time": "2018-09-14 19:45:07",
		"ftime": "2018-09-14 19:45:07",
		"context": "快件已到达 金华转运中心",
		"location": null
	}, {
		"time": "2018-09-14 16:58:15",
		"ftime": "2018-09-14 16:58:15",
		"context": "快件已到达 江西省新余市公司",
		"location": null
	}, {
		"time": "2018-09-14 13:18:34",
		"ftime": "2018-09-14 13:18:34",
		"context": "快件已发往 江西省新余市公司",
		"location": null
	}, {
		"time": "2018-09-14 12:31:53",
		"ftime": "2018-09-14 12:31:53",
		"context": "快件已到达 南昌转运中心",
		"location": null
	}, {
		"time": "2018-09-14 04:25:23",
		"ftime": "2018-09-14 04:25:23",
		"context": "快件已到达 武昌转运中心",
		"location": null
	}, {
		"time": "2018-09-14 02:33:53",
		"ftime": "2018-09-14 02:33:53",
		"context": "快件已发往 南昌转运中心",
		"location": null
	}, {
		"time": "2018-09-13 22:58:34",
		"ftime": "2018-09-13 22:58:34",
		"context": "快件已到达 武昌转运中心",
		"location": null
	}, {
		"time": "2018-09-13 21:12:53",
		"ftime": "2018-09-13 21:12:53",
		"context": "快件已发往 武昌转运中心",
		"location": null
	}, {
		"time": "2018-09-13 16:57:10",
		"ftime": "2018-09-13 16:57:10",
		"context": "湖北省鄂州市葛店开发区公司取件人: 严红武（18064157077） 已收件",
		"location": null
	}]
}