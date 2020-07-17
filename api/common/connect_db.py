import pymysql

from DBUtils.PooledDB import PooledDB
from sshtunnel import SSHTunnelForwarder

from api.baseapi import BaseApi


class connect_DataBase(BaseApi):
    """
    连接数据库
    """

    def __init__(self, dbname='', host="", user="", password="", port=0):
        pool = PooledDB(pymysql, mincached=20, host=host, user=user, password=password, db=dbname, charset='utf8mb4',
                        port=port)
        self.conn = pool.connection()
        self.cursor = self.conn.cursor()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

    def get_result(self, sql):
        """传入sql，获取结果"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def res_fetchall_by_list(self, mysql, list):
        """根据list查询mysql结果，返回list"""
        self.cursor.execute(mysql, list)
        res_list = self.cursor.fetchall()
        result = []
        if len(list) > 0:
            for i in res_list:
                result.append(i[0])
        return result

    def res_fetchall(self, mysql):
        """执行mysql语句拿到数组结果"""
        self.cursor.execute(mysql)
        list = self.cursor.fetchall()
        result = []
        if len(list) > 0:
            for i in list:
                result.append(i[0])
        return result

    def res_fetchone(self, mysql):
        """执行mysql语句拿到一条结果"""
        self.cursor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_agent_all_money(self, agent_num):
        """
        获取代理商所有的交易总金额
        :param agent_num:
        :return:
        """
        mysql = "SELECT sum(money) from agent_summary_record WHERE agent_num='%s'" % agent_num
        self.cursor.execute(mysql)
        agent_money = self.cursor.fetchone()[0]
        if agent_money == None:
            agent_money = 0
        return '%.2f' % agent_money

    def get_agent_list(self, agent_num):
        """
        获取我的所有未删除代理商agent_num列表
        :param agent_num:
        :return:
        """
        mysql = "SELECT agent_num FROM agent WHERE is_del=0 AND p_num='%s' OR p_num IN " \
                "(SELECT agent_num FROM agent WHERE p_num='%s' or p_num IN " \
                "(SELECT agent_num FROM agent WHERE p_num='%s'))" % (agent_num, agent_num, agent_num)
        return self.res_fetchall(mysql)

    def get_sub_agent_list(self, agent_num):
        """
        获取我的下级代理商agent_num列表
        :param agent_num:
        :return:
        """
        mysql = "SELECT agent_num FROM agent WHERE is_del=0 AND p_num IN " \
                "(SELECT agent_num FROM agent WHERE p_num='%s' or p_num IN " \
                "(SELECT agent_num FROM agent WHERE p_num='%s'))" % (agent_num, agent_num)
        return self.res_fetchall(mysql)

    def get_dir_agent_list(self, agent_num):
        """
        获取我的直属代理商agent_num列表
        :param agent_num:
        :return:
        """
        mysql = "SELECT agent_num FROM agent WHERE is_del=0 AND p_num='%s' ORDER BY created_at DESC" % (agent_num)
        return self.res_fetchall(mysql)

    def get_merchant_list(self, agent_num, tenant_num):
        """获取所有未删除商户merchant_num的列表"""
        agent_list = self.get_agent_list(agent_num)
        agent_list.append(agent_num)
        mysql = 'select merchant_num from merchants WHERE is_del=0 AND agent_num IN (%s)' % ','.join(
            ['%s'] * len(agent_list))
        return self.res_fetchall_by_list(mysql, agent_list)

    def get_dir_merchant_list(self, agent_num):
        """
        获取直属商户merchant_num的列表
        """
        mysql = 'select merchant_num from merchants s WHERE is_del=0 AND agent_num=%s order by updated_at desc,s.created_at ASC' % agent_num
        return self.res_fetchall(mysql)

    def get_dir_merchant_list_by_fullname(self, agent_num, full_name):
        """
        获取直属商户merchant_num的列表,full_name模糊搜索
        """
        mysql = "select merchant_num from merchants WHERE full_name LIKE '%%%s%%' and is_del=0 AND agent_num=%s order by updated_at desc" % (
         full_name,agent_num)
        return self.res_fetchall(mysql)

    def get_sub_merchant_list(self, agent_num):
        """
        获取下属商户merchant_num的列表
        :param agent_num: 代理商编号
        :return:
        """
        agent_list = self.get_agent_list(agent_num)
        mysql = 'select merchant_num from merchants WHERE is_del=0 AND agent_num IN (%s)' % ','.join(
            ['%s'] * len(agent_list))
        return self.res_fetchall_by_list(mysql, agent_list)

    def get_loss_merchant_list(self, agent_num):
        """
        获取流失商户merchant_num的列表
        :param agent_num: 代理商编号
        :return:
        """
        agent_list = self.get_agent_list(agent_num)
        agent_list.append(agent_num)
        mysql = 'SELECT merchant_num FROM merchants WHERE is_del=0 AND ' \
                'NOW()-channel_open_time>172800 AND NOW()-last_payed_at>172800 AND channel_open_time>0 AND agent_num IN (%s)' % ','.join(
            ['%s'] * len(agent_list))
        return self.res_fetchall_by_list(mysql, agent_list)

    def get_loss_merchant_list_by_sale(self, agent_num, sale_num):
        """
        获取业务员的流失商户列表
        :param agent_num:
        :param sale_num:
        :return:
        """
        mysql = 'SELECT merchant_num FROM merchants WHERE is_del=0 AND ' \
                'NOW()-channel_open_time>172800 AND NOW()-last_payed_at>172800 AND channel_open_time>0 AND ' \
                'agent_num=%s and sale_num=%s' % (agent_num, sale_num)
        return self.res_fetchall(mysql)

    def get_agent_notices(self, agent_num):
        """
        获取代理商首页消息列表
        :param agent_num:
        :return:
        """
        mysql = ("SELECT notice_agent.status,notice_agent.agent_num,notices.author,"
                 "notices.created_at,notices.id,"
                 "notices.posted,notices.status,notices.title from "
                 "notices,notice_agent "
                 "WHERE notices.id=notice_agent.notice_id AND notice_agent.agent_num='%s'"
                 "ORDER BY notices.created_at desc limit 0,20") % agent_num
        self.cursor.execute(mysql)
        result_list = self.cursor.fetchall()
        list = []
        if len(result_list) > 0:
            for i in result_list:
                result = {'agent_status': i[0], 'agent_num': i[1], 'author': i[2], 'created_at': i[3],
                          'id': i[4], 'posted': i[5], 'status': i[6], 'title': i[7]}
                list.append(result)
        return list

    def get_sale_list(self, agent_num):
        """
        获取代理商的所有业务员
        :return:
        """
        mysql = 'select saleman_num from saleman WHERE is_del=0 and agent_num=%s' % agent_num
        self.cursor.execute(mysql)
        list = self.cursor.fetchall()
        result = []
        if len(list) > 0:
            for i in list:
                result.append(i[0])
        return result

    def get_agent_money_thismonth(self, agent_num):
        """
        获取代理商本月交易金额
        :param agent_num:
        :return:
        """
        start_time = self.get_this_month_start()
        end_time = self.get_this_month_end()
        mysql = 'select sum(money) from agent_summary_record WHERE agent_num=%s AND day BETWEEN %s AND %s' \
                % (agent_num, start_time, end_time)
        self.cursor.execute(mysql)
        agent_money = self.cursor.fetchone()[0]
        if agent_money == None:
            agent_money = 0
        return '%.2f' % agent_money

    def get_agent_money_lastmonth(self, agent_num):
        """
        获取代理商上月交易金额
        :param agent_num:
        :return:
        """
        start_time = self.get_lastmonth_start()
        end_time = self.get_lastmonth_end()
        mysql = 'select sum(money) from agent_summary_month WHERE agent_num=%s AND month BETWEEN %s AND %s' \
                % (agent_num, start_time, end_time)
        self.cursor.execute(mysql)
        agent_money = self.cursor.fetchone()[0]
        if agent_money == None:
            agent_money = 0
        return '%.2f' % agent_money

    def get_merchant_check_list(self, agent_num, agent_level):
        """
        获取首页商户审核状态
        :param agent_num:
        :return:
        """
        start_time = self.get_now() - 100 * 86400
        end_time = self.get_now()
        if agent_level == 0:
            merchant_list = self.get_merchant_list(agent_num)
        else:
            merchant_list = self.get_dir_merchant_list(agent_num)
        mysql = 'select merchant_num,b_channel,check_status FROM merchant_channel_status WHERE' \
                ' check_status NOT IN (100,110) AND merchant_num IN (%s) ' \
                'AND create_at BETWEEN %s AND %s ' \
                'GROUP BY merchant_num,b_channel ' \
                'ORDER BY create_at desc limit 0,10' % (','.join(['%s'] * len(merchant_list)), start_time, end_time)
        self.cursor.execute(mysql, merchant_list)
        list = self.cursor.fetchall()
        result = []
        if len(list) > 0:
            for i in list:
                result.append({'merchant_num': i[0], 'b_channel': i[1], 'check_status': i[2]})
        return result

    def get_b_channel_name(self, b_chennel):
        """
        获取通道的名称
        :param b_chennel:
        :return:
        """
        b_chennel = int(b_chennel)
        if b_chennel == 0:
            return '官方通道'
        elif b_chennel == 1:
            return '平安银行'
        elif b_chennel == 2:
            return '网商银行'
        elif b_chennel == 3:
            return '富民'
        elif b_chennel == 4:
            return '乐刷'
        elif b_chennel == 5:
            return '新大陆'
        elif b_chennel == 6:
            return '三峡银行'
        elif b_chennel == 7:
            return '合利宝'
        elif b_chennel == 8:
            return '银联官方'
        elif b_chennel == 9:
            return '和融通'
        elif b_chennel == 10:
            return '随行付'
        elif b_chennel == 11:
            return '哆啦宝'
        else:
            return '入参有误，请重新请求'

    def get_check_status_name(self, check_status):
        """
        获取check_status的name
        :param check_status:
        :return:
        """
        check_status = int(check_status)
        if check_status == 100:
            return '申请中'
        elif check_status == 110:
            return '已审核入驻中'
        elif check_status == 200:
            return '已成功'
        elif check_status == -100:
            return '已禁用'
        elif check_status == -200:
            return '申请失败'
        else:
            return '入参有误，请重新请求'

    def get_agent_money_by_channel_thismonth(self, agent_num, b_channel):
        """
        获取本月代理商通道交易流水
        :param agent_num:
        :param channel:
        :return:
        """
        start_time = self.get_this_month_start()
        end_time = self.get_this_month_end()
        mysql = 'select sum(money) from agent_summary_record WHERE agent_num=%s AND b_channel=%s AND day BETWEEN %s AND %s' \
                % (agent_num, b_channel, start_time, end_time)
        self.cursor.execute(mysql)
        agent_money = self.cursor.fetchone()[0]
        if agent_money == None:
            agent_money = 0
        return '%.2f' % agent_money

    def get_agent_money_by_channel_lastmonth(self, agent_num, b_channel):
        """
        获取上月代理商通道交易流水
        :param agent_num:
        :param b_channel:
        :return:
        """
        start_time = self.get_lastmonth_start()
        end_time = self.get_lastmonth_end()
        mysql = 'select sum(money) from agent_summary_record WHERE agent_num=%s AND b_channel=%s AND day BETWEEN %s AND %s' \
                % (agent_num, b_channel, start_time, end_time)
        self.cursor.execute(mysql)
        agent_money = self.cursor.fetchone()[0]
        if agent_money == None:
            agent_money = 0
        return '%.2f' % agent_money

    def get_merchant_money_top(self, agent_num):
        """
        获取商户交易流水top10
        :param agent_num:
        :return:
        """
        start_time = self.get_this_month_start()
        end_time = self.get_this_month_end()
        merchant_list = self.get_merchant_list(agent_num)

        mysql = 'select merchant_num,sum(deal_mount-refund_amount) AS money FROM merchant_transaction_record ' \
                'WHERE day BETWEEN %s AND %s AND merchant_num IN (%s) ' \
                'GROUP BY merchant_num ' \
                'ORDER BY money DESC LIMIT 0,10' % (start_time, end_time, ','.join(['%s'] * len(merchant_list)))
        self.cursor.execute(mysql, merchant_list)
        list = self.cursor.fetchall()
        result = []
        if len(list) > 0:
            for i in list:
                result.append({'merchant_num': i[0], 'money': '%.2f' % i[1]})
        return result

    def get_merchant_name(self, merchant_num):
        """
        获取商户名
        :param merchant_num:
        :return:
        """
        mysql = 'select full_name from merchants WHERE merchant_num=%s' % merchant_num
        self.cursor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_merchant_contact_name(self, merchant_num):
        """
        获取联系人姓名
        :return:
        """
        mysql = 'select contact_name from merchant_detail where merchant_num=%s' % merchant_num
        self.cursor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_merchant_contact_phone(self, merchant_num):
        """
        获取联系人电话
        :return:
        """
        mysql = 'select contact_phone from merchant_details where merchant_num=%s' % merchant_num
        return self.res_fetchone(mysql)

    def get_merchant_area(self, merchant_num):
        """
        获取商户的区域
        """
        mysql = 'select province,city,area from merchants where merchant_num=%s' % merchant_num
        return self.res_fetchone(mysql)

    def get_sale_expand_merchant_list(self, agent_num, sale_num, start_time, stop_time):
        """
        获取业务员在时间段内拓展商户的列表
        :param agent_num:
        :param sale_num:
        :param start_time:时间戳
        :param stop_time:时间戳
        :return:
        """
        mysql = 'select merchant_num from merchants where is_del=0 and agent_num=%s and sale_num=%s and create_at>=%s and create_at<=%s' % (
            agent_num, sale_num, start_time, stop_time)
        return self.res_fetchall(mysql)

    def get_sale_expand_merchant_list_all(self, agent_num, sale_num):
        """
        获取业务员发展的所有商户，去除已删除的
        :param agent_num:
        :param sale_num:
        :return:
        """
        mysql = 'select merchant_num from merchants where is_del=0 and agent_num=%s and sale_num=%s' % (
            agent_num, sale_num)
        return self.res_fetchall(mysql)

    def get_sale_expand_merchant_money_today(self, agent_num, sale_num):
        """
        获取业务员的商户今天有效交易金额、有效交易笔数、产生的佣金
        :param agent_num:
        :param sale_num:
        :return:
        """
        today_start = self.get_today_start()
        today_end = self.get_today_end()
        merchant_list = self.get_sale_expand_merchant_list_all(agent_num, sale_num)
        result = []
        mysql1 = 'select sum(order_money),count(*),sum(money) from agent_bkge_records where ' \
                 'agent_num=%s and bkge_type=1 ' \
                 'and pay_at between %s and %s ' \
                 'and merchant_num in (%s)' % (
                     agent_num, today_start, today_end, ','.join(['%s'] * len(merchant_list)))
        mysql2 = 'select sum(order_money),count(*),sum(money) from agent_bkge_records where ' \
                 'agent_num=%s and bkge_type=2 ' \
                 'and pay_at between %s and %s ' \
                 'and merchant_num in (%s)' % (
                     agent_num, today_start, today_end, ','.join(['%s'] * len(merchant_list)))
        self.cursor.execute(mysql1, merchant_list)
        list1 = self.cursor.fetchall()
        self.cursor.execute(mysql2, merchant_list)
        list2 = self.cursor.fetchall()

        money = 0
        number = list1[0][1]
        bkge_money = 0

        if number > 0:
            if list2[0][1] > 0:
                money = list1[0][0] - list2[0][0]
                bkge_money = list1[0][2] - list2[0][2]
            else:
                money = list1[0][0]
                bkge_money = list1[0][2]
        result.append({'money': '%.2f' % money, 'number': number, 'bkge_money': '%.2f' % bkge_money})

        return result

    def get_sale_expand_merchant_money_notoday(self, agent_num, sale_num, start_time, stop_time):
        """
        获取业务员的商户非今日时间段的有效交易金额、有效交易笔数、产生的佣金
        :param agent_num:
        :param sale_num:
        :param start_time:
        :param stop_time:
        :return:
        """
        today_start = self.get_today_start()
        today_end = self.get_today_end()
        merchant_list = self.get_sale_expand_merchant_list_all(agent_num, sale_num)
        result = []
        if start_time == today_start or stop_time == today_end:
            return '请输入正确的时间段'
        else:
            mysql = 'select sum(total_money),sum(number),sum(bkge_money) from agent_bkge_day where ' \
                    'agent_num=%s ' \
                    'and day between %s and %s ' \
                    'and merchant_num in (%s)' % (
                        agent_num, start_time, stop_time, ','.join(['%s'] * len(merchant_list)))
            self.cursor.execute(mysql, merchant_list)
            list = self.cursor.fetchall()
            if list[0][1] != None:
                for i in list:
                    result.append({'money': '%.2f' % i[0], 'number': int(i[1]), 'bkge_money': '%.2f' % i[2]})
            else:
                result.append({'money': 0.00, 'number': 0, 'bkge_money': 0.00})
        return result

    def get_sale_expand_merchant_money(self, agent_num, sale_num, start_time, stop_time):
        """
        获取业务员的商户在时间段内的有效交易金额、有效交易笔数、产生的佣金
        :param agent_num:
        :param sale_num:
        :param start_time:
        :param stop_time:
        :return:
        """
        today_start = self.get_today_start()
        today_end = self.get_today_end()
        result = []
        if start_time == today_start and stop_time >= today_end:
            result = self.get_sale_expand_merchant_money_today(agent_num, sale_num)
        elif start_time < today_start and stop_time >= today_end:
            result1 = self.get_sale_expand_merchant_money_notoday(agent_num, sale_num, start_time, today_end - 1)
            result2 = self.get_sale_expand_merchant_money_today(agent_num, sale_num)
            result.append({'money': '%.2f' % (float(result1[0]['money']) + float(result2[0]['money'])),
                           'number': result1[0]['number'] + result2[0]['number'],
                           'bkge_money': '%.2f' % (float(result1[0]['bkge_money']) + float(result2[0]['bkge_money']))})
        elif start_time < today_start and stop_time < today_start:
            result = self.get_sale_expand_merchant_money_notoday(agent_num, sale_num, start_time, stop_time)
        else:
            "请输入正确的时间"
        return result

    def get_agent_expand_merchant_money_today(self, agent_num):
        """
        获取代理商的商户今天有效交易金额、有效交易笔数、产生的佣金
        :param agent_num:
        :return:
        """
        today_start = self.get_today_start()
        today_end = self.get_today_end()
        merchant_list = self.get_merchant_list(agent_num)
        result = []
        mysql1 = 'select sum(order_money),count(*),sum(money) from agent_bkge_records where ' \
                 'agent_num=%s and bkge_type=1 ' \
                 'and pay_at between %s and %s ' \
                 'and merchant_num in (%s)' % (
                     agent_num, today_start, today_end, ','.join(['%s'] * len(merchant_list)))
        mysql2 = 'select sum(order_money),count(*),sum(money) from agent_bkge_records where ' \
                 'agent_num=%s and bkge_type=2 ' \
                 'and pay_at between %s and %s ' \
                 'and merchant_num in (%s)' % (
                     agent_num, today_start, today_end, ','.join(['%s'] * len(merchant_list)))
        self.cursor.execute(mysql1, merchant_list)
        list1 = self.cursor.fetchall()
        self.cursor.execute(mysql2, merchant_list)
        list2 = self.cursor.fetchall()

        money = 0
        number = list1[0][1]
        bkge_money = 0

        if number > 0:
            if list2[0][1] > 0:
                money = list1[0][0] - list2[0][0]
                bkge_money = list1[0][2] - list2[0][2]
            else:
                money = list1[0][0]
                bkge_money = list1[0][2]
        result.append({'money': '%.2f' % money, 'number': number, 'bkge_money': '%.2f' % bkge_money})

        return result

    def get_agent_expand_merchant_money_notoday(self, agent_num, start_time, stop_time):
        """
        获取代理商的商户非今日时间段的有效交易金额、有效交易笔数、产生的佣金
        :param agent_num:
        :param start_time:
        :param stop_time:
        :return:
        """
        today_start = self.get_today_start()
        today_end = self.get_today_end()
        merchant_list = self.get_merchant_list(agent_num)
        result = []
        if start_time == today_start or stop_time == today_end:
            return '请输入正确的时间段'
        else:
            mysql = 'select sum(total_money),sum(number),sum(bkge_money) from agent_bkge_day where ' \
                    'agent_num=%s ' \
                    'and day between %s and %s ' \
                    'and merchant_num in (%s)' % (
                        agent_num, start_time, stop_time, ','.join(['%s'] * len(merchant_list)))
            self.cursor.execute(mysql, merchant_list)
            list = self.cursor.fetchall()
            if list[0][1] != None:
                for i in list:
                    result.append({'money': '%.2f' % i[0], 'number': int(i[1]), 'bkge_money': '%.2f' % i[2]})
            else:
                result.append({'money': 0.00, 'number': 0, 'bkge_money': 0.00})
        return result

    def get_agent_expand_merchant_money(self, agent_num, start_time, stop_time):
        """
        获取代理商的商户在时间段内的有效交易金额、有效交易笔数、产生的佣金
        :param agent_num:
        :param start_time:
        :param stop_time:
        :return:
        """
        today_start = self.get_today_start()
        today_end = self.get_today_end()
        result = []
        if start_time == today_start and stop_time >= today_end:
            result = self.get_agent_expand_merchant_money_today(agent_num)
        elif start_time < today_start and stop_time >= today_end:
            result1 = self.get_agent_expand_merchant_money_notoday(agent_num, start_time, today_end - 1)
            result2 = self.get_agent_expand_merchant_money_today(agent_num)
            result.append({'money': '%.2f' % (float(result1[0]['money']) + float(result2[0]['money'])),
                           'number': result1[0]['number'] + result2[0]['number'],
                           'bkge_money': '%.2f' % (float(result1[0]['bkge_money']) + float(result2[0]['bkge_money']))})
        elif start_time < today_start and stop_time < today_start:
            result = self.get_agent_expand_merchant_money_notoday(agent_num, start_time, stop_time)
        else:
            "请输入正确的时间"
        return result

    def get_agent_expand_merchant_list(self, agent_num, start_time, stop_time):
        """
        获取代理商在时间段内拓展所有商户的列表
        :param agent_num:
        :param start_time:时间戳
        :param stop_time:时间戳
        :return:
        """
        mysql = 'select merchant_num from merchant where is_del=0 and create_at>=%s and create_at<=%s and (' \
                'agent_num=%s or agent_num IN (' \
                'SELECT agent_num FROM agent WHERE p_num=%s OR p_num IN (' \
                'SELECT agent_num FROM agent WHERE p_num=%s OR p_num IN (' \
                'SELECT agent_num FROM agent WHERE p_num=%s))))' % (
                    start_time, stop_time, agent_num, agent_num, agent_num, agent_num)
        self.cursor.execute(mysql)
        list = self.cursor.fetchall()
        result = []
        if len(list) > 0:
            for i in list:
                result.append(i[0])
        return result

    def get_merchant_info(self, merchant_num):
        """获取商户资料"""
        mysql = 'select * from merchants where merchant_num=%s' % (merchant_num)
        self.cursor.execute(mysql)
        list = self.dict_fetchall(self.cursor)[0]
        return list

    def get_agent_name(self, agent_num):
        """获取代理商名称"""
        mysql = 'select agent_name from agent where agent_num=%s' % agent_num
        self.cursor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_agent_telphone(self, agent_num):
        """获取代理商手机号码"""
        mysql = 'select telphone from agent where agent_num=%s' % agent_num
        self.cousor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_agent_merchant_count(self, agent_num):
        """获取代理商的所有商户数"""
        mysql = 'select count(*) from merchants where agent_num=%' % agent_num
        self.cousor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_merchant_store_total(self, merchant_num):
        """获取商户的店铺数量"""
        mysql = 'select count(*) from stores where merchant_num=%s' % merchant_num
        self.cursor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]

    def get_merchant_staff_total(self, merchant_num):
        """获取商户的店员数量"""
        mysql = 'select count(*) from staffs where merchant_num=%s' % merchant_num
        self.cursor.execute(mysql)
        result = self.cursor.fetchone()
        return result[0]


    def get_saleman_list(self):
        """获取01业务员信息"""
        mysql = 'select * from saleman'
        self.cursor.execute(mysql)

    def get_saleman_info(self, saleman_num):
        """获取业务员资料"""
        mysql = 'select * from saleman where saleman_num= %s' % (saleman_num)
        self.cursor.execute(mysql)
        list = self.dict_fetchall(self.cursor)[0]
        return list
    def get_saleman_name(self, saleman_num):
        """获取业务员姓名"""
        mysql = 'select name from saleman where saleman_num= %s' %(saleman_num)
        return self.res_fetchone(mysql)

    def get_saleman_phone(self, saleman_num):
        """获取业务员手机号"""
        mysql = 'select phone from saleman where saleman_num= %s' %(saleman_num)
        return self.res_fetchone(mysql)


    def get_saleman_contact_phone(self, saleman_num):
        """业务员联系电话"""
        mysql = 'select contact_phone from saleman where saleman_num= %s' %(saleman_num)
        return self.res_fetchone(mysql)

    def get_saleman_create_at(self, saleman_num):
        """创建时间"""
        mysql = 'select create_at from saleman where saleman_num= %s' %(saleman_num)
        return self.res_fetchone(mysql)





# con = connect_DataBase(dbname='agent_61000001',host='192.168.19.68',port=50005,user='remote',password='is2ce8yfsq5r3Zloz0cN7wZ')
# # con.get_merchant_list_info('8020000019')
# print(con.get_dir_merchant_list('700000429'))

# conn = connect_DataBase(db='merchant_61000001',host='39.106.118.50',user='remote',password='is2ce8yfsq5r3Zloz0cN7wZ')
# print(conn.get_merchant_staff_total('8018001111'))

# con = connect_DataBase(dbname='merchants',host='192.168.19.68',port=50005,user='remote',password='is2ce8yfsq5r3Zloz0cN7wZ')
# print(con.get_dir_merchant_list_by_fullname('700000429','陈亦飞'))
#
#
# con.close_conn()
