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
@SmallPotY ��ͼ��ߵ���ʱ��
CREATE TABLE [dbo].[Express_Trace_Temp](
	[Id] [int] IDENTITY(1,1) NOT NULL,	--����ID
	[Express_No] [varchar](32) NOT NULL,	--��ݵ���
	[Express_Company] [varchar](20) NOT NULL,	--��ݹ�˾����
	[Express_Status] [int] NULL,					--���״̬
	[Has_Signed] [int] NULL,							--�Ƿ�ǩ��
	[Trace_Context] [varchar](255) NULL,	--�ڵ��������
	[Trace_Date_Time] [datetime] NULL,		--�ڵ�ʱ��
	[Area_Name] [varchar](50) NULL,				--�������ƣ��硰�Ϻ��С�
	[Process_Status] [int] NULL,					--״̬��ȡ����
��
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
		"context": "�����ǩ�� ǩ����: ���˴�ǩ, ��У�������ǩ�գ�С��Ϊ���߳Ϸ�������������ϵ�� 15083622574 ��лʹ��Բͨ�ٵݣ��ڴ��ٴ�Ϊ������",
		"location": null
	}, {
		"time": "2018-09-16 13:33:20",
		"ftime": "2018-09-16 13:33:20",
		"context": "����ѵ���ұ��ѧУ��У���Կ�ݷ�������������վ,��ϵ�绰18379002007",
		"location": null
	}, {
		"time": "2018-09-16 13:31:20",
		"ftime": "2018-09-16 13:31:20",
		"context": "����ʡ�����к�����˾�ɼ���: ФС�ޣ�13979053898�� �����ɼ�",
		"location": null
	}, {
		"time": "2018-09-14 19:45:07",
		"ftime": "2018-09-14 19:45:07",
		"context": "����ѵ��� ��ת������",
		"location": null
	}, {
		"time": "2018-09-14 16:58:15",
		"ftime": "2018-09-14 16:58:15",
		"context": "����ѵ��� ����ʡ�����й�˾",
		"location": null
	}, {
		"time": "2018-09-14 13:18:34",
		"ftime": "2018-09-14 13:18:34",
		"context": "����ѷ��� ����ʡ�����й�˾",
		"location": null
	}, {
		"time": "2018-09-14 12:31:53",
		"ftime": "2018-09-14 12:31:53",
		"context": "����ѵ��� �ϲ�ת������",
		"location": null
	}, {
		"time": "2018-09-14 04:25:23",
		"ftime": "2018-09-14 04:25:23",
		"context": "����ѵ��� ���ת������",
		"location": null
	}, {
		"time": "2018-09-14 02:33:53",
		"ftime": "2018-09-14 02:33:53",
		"context": "����ѷ��� �ϲ�ת������",
		"location": null
	}, {
		"time": "2018-09-13 22:58:34",
		"ftime": "2018-09-13 22:58:34",
		"context": "����ѵ��� ���ת������",
		"location": null
	}, {
		"time": "2018-09-13 21:12:53",
		"ftime": "2018-09-13 21:12:53",
		"context": "����ѷ��� ���ת������",
		"location": null
	}, {
		"time": "2018-09-13 16:57:10",
		"ftime": "2018-09-13 16:57:10",
		"context": "����ʡ�����и�꿪������˾ȡ����: �Ϻ��䣨18064157077�� ���ռ�",
		"location": null
	}]
}