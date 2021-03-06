# coding=utf-8


query_interval = 4     # 快递单号查询间隔 {query_interval} 小时
query_first_interval = 2    # 获取第一次查询的更新间隔
query_err_interval = 2      # 查询失败的更新间隔
thread_nbmber = 3      # 调用线程数
parse_nbmber = 15      # 一个线程解析 parse 个url



proxyHost = "http-pro.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息
proxyUser = "**"
proxyPass = "**"

DB_token = {
    'PGSQL': {
        'PG_USERNAME': '',
        'PG_PASSWORD': '',
        'PG_HOST': '',
        'PG_PORT': '',
        'PG_DATABASE': 'express_spider',
    },

    'MSSQL': {
        'MS_server': '',
        'MS_port': '',
        'MS_user': '',
        'MS_password': '',
        'MS_database': 'express_spider'
    },

    'tiantu': {
        'MS_server': '',
        'MS_port': '',
        'MS_user': '',
        'MS_password': '',
        'MS_database': 'Express_Query'
    }
}

jd_key_state = {
    "揽收完成": "揽收",
    "交付京东物流": "未揽收",
    "到达": "途中",
    "离开": "途中",
    "等待配送": "途中",
    "开始配送": "派件",
    "签收": "签收",
    "再投": "异常",
    "代收": "签收",
    "完成配送": "签收",
    "拒收": "异常",
    "换单": "异常"

}

zhongtong_key_state = {
    "已揽收": "揽收",
    "发往": "途中",
    "到达": "途中",
    "感谢使用中通快递": "签收",
    "已经妥投": "签收",
    "次派件": "派件",
    "被退回": "异常",
    "问题件": "异常",

}

yuantong_key_state = {
    "已收件": "揽收",
    "已发往": "途中",
    "已到达": "途中",
    "已打包": "途中",
    "下一站": "途中",
    "已收入": "途中",
    "派件中": "派件",
    "及时取件": "途中",
    "正在派件": "派件",
    "请上门自提": "途中",
    "已签收": "签收",
    "代收": "签收",
    "失败签收": "异常",
    "已拆包": "途中",
    "留仓件": "途中",
    "已退回": "异常",
    "签收失败": "异常",
    "快件被快递员取出": "异常",
    "滞留": "异常",
    "重新派送": "异常",
    "间接操作": "途中",
    "转运": "途中",
    "派送": "派件",
    "再投": "异常",
    "离开": "途中",
    "发往": "途中",
}

yunda_key_state = {
    "到件扫描": "揽收",
    "称重": "途中",
    "中转集包": "途中",
    "进入": "途中",
    "装车": "途中",
    "发出": "途中",
    "到达目的地": "途中",
    "发往": "途中",
    "派件扫描": "派件",
    "签收": "签收",
    "卸车": "途中",
    "已揽件": "揽收",
    "到达：": "途中",
    "上级站点": "途中",
    ")派送": "派件",
    "到达": "途中",
    "揽件": "揽收",
    "为您派件": "派件",
    "已收件": "揽收",
    "【派送】扫描": "派件",
    "【分发】扫描": "途中",
    "【到件】扫描": "揽收",
    "卖家发货": "未揽收",
    "自提": "签收",
    "进行扫描": "途中",
    "【反馈】扫描": "途中",
    "快件扫描": "途中",
    "菜鸟驿站": "签收",
    "完成取件": "签收",
    "问题件": "异常",
    "节假日客户上班后派送": "异常",
}

youzhengguonei_key_state = {
    "已收寄": "揽收",
    "离开": "途中",
    "到达": "途中",
    "卖家发货": "未揽收",
    "接收": "途中",
    "正在投递": "派件",
    "已签收": "签收",
    "自提点": "签收",
    "已妥投": "签收",
    "包裹柜": "派件",
    "发往": "途中",
    "正在派件": "派件",
    "下一站": "途中",
    "已收入": "途中",
    "派件中": "派件",
    "转运": "途中",
    "代收": "签收",
    "请上门自提": "签收",
    "要求延迟投递": "异常",
    "其他【": "途中",
    "再投": "异常",
    "拒收": "拒收",
    "不详": "异常",
    "未妥投": "异常",
    "收件人已取走邮件": "签收",
    "收件人自取": "签收",
    "自取未取": "异常",

}

key_state = {
    "zhongtong": zhongtong_key_state,
    "yuantong": yuantong_key_state,
    "yunda": yunda_key_state,
    "jd": jd_key_state,
    "youzhengguonei": youzhengguonei_key_state
}
