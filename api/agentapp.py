import requests

from api.baseapi import BaseApi
from api.common.connect_db import connect_DataBase
from api.common.connect_mongodb import DataBase_Mongo
from api.common.mysqldata import MysqlData


class AgentApp(BaseApi):
    # host地址
    # test测试环境
    ucenter = '*******'
    fws = '*******'
    test_user_our_0 = {'tenant-id': '61000001', 'username': 'admin@qq.com', 'password': '123456'}
    test_user_our_1 = {'tenant-id': '61000001', 'username': 'chenyifei@qq.com', 'password': '123456'}
    test_user_our_2 = {'tenant-id': '61000001', 'username': 'chenyifei2@qq.com', 'password': '123456'}
    test_user_our_3 = {'tenant-id': '61000001', 'username': 'chenyifei3@qq.com', 'password': '123456'}

    test_user_isv_0 = {'tenant-id': '61000034', 'username': '15510001001', 'password': '123456'}
    test_user_isv_1 = {'tenant-id': '61000034', 'username': '15510001002', 'password': '123456'}
    test_user_isv_2 = {'tenant-id': '61000034', 'username': '15510001013', 'password': '123456'}
    test_user_isv_3 = {'tenant-id': '61000034', 'username': '15510001014', 'password': '123456'}

    test_sale_our = {'tenant-id': '61000001', 'username': '13312349006', 'password': '123456'}
    test_sale_isv = {'tenant-id': '61000034', 'username': '002003', 'password': '123456'}

    db = {'host': "****", 'port': 50000, 'user': "user", 'password': "pw"}
    db_mongo = {'host': "****", 'port': 50002, 'user': "user", 'password': 'pw', 'dbname': 'channel'}

    # final预发布环境
    # ucenter = '*******'
    # fws = '*******'
    # test_user_our_0 = {'tenant-id': '61000001', 'username': 'admin@qq.com', 'password': '123456'}
    # test_user_our_1 = {'tenant-id': '61000001', 'username': '18610001001', 'password': '666666'}
    # test_user_our_2 = {'tenant-id': '61000001', 'username': '18610001002', 'password': '666666'}
    # test_user_our_3 = {'tenant-id': '61000001', 'username': '18610001003', 'password': '666666'}
    #
    # test_user_isv_0 = {'tenant-id': '61000009', 'username': '13412342101', 'password': '123456'}
    # test_user_isv_1 = {'tenant-id': '61000009', 'username': '13412342105', 'password': '123456'}
    # test_user_isv_2 = {'tenant-id': '61000009', 'username': '13412342106', 'password': '123456'}
    # test_user_isv_3 = {'tenant-id': '61000009', 'username': '13412342107', 'password': '123456'}
    #
    # test_sale_our = {'tenant-id': '61000001', 'username': '15736174443', 'password': '123456'}
    # test_sale_isv = {'tenant-id': '61000009', 'username': '002002', 'password': '123456'}
    #
    # db = {'host': "192.168.19.68", 'port': 50005, 'user': "remote", 'password': "is2ce8yfsq5r3Zloz0cN7wZ"}
    # db_mongo = {'host': "192.168.19.68", 'port': 50007, 'user': "uphicoo", 'password': 'uphicoo', 'dbname': 'channel'}

    # 登录相关url
    ucenter_login_url = ucenter + '/public/user/login-auth'
    ucenter_access_login_url = ucenter + '/public/access-user/login-auth'
    new_login_url = fws + '/appapi/v4/common/login/new-login'

    # header头文件
    device_uuid = '123456'
    agent_app = 'v4.0.3'
    Api_Version = 'v3.0'
    agent_login_type = 'agent'
    saleman_login_type = 'saleman'

    # token及user_id等参数
    token = dict()
    level = 0
    isv = 0
    token_sale = dict()
    isv_sale = 0

    @classmethod
    def conn_db(cls, dbdata: str):
        # conn = connect_DataBase(host=cls.db['host'], port=cls.db['port'], user=cls.db['user'], password=cls.db['password'], dbname=dbdata)
        # return conn
        conn=MysqlData(dbname=dbdata,dbconfig=cls.db)
        return conn

    @classmethod
    def close_db(cls, conn: MysqlData):
        conn.close_session()

    @classmethod
    def conn_db_mongo(cls):
        conn = DataBase_Mongo(host=cls.db_mongo['host'], port=cls.db_mongo['port'], dbname=cls.db_mongo['dbname'],
                              user=cls.db_mongo['user'], password=cls.db_mongo['password'])
        return conn

    @classmethod
    def close_db_mongo(cls, conn: DataBase_Mongo):
        conn.close_conn()

    @classmethod
    def get_token(cls, level=level, isv=isv):
        """
        获取代理商登录的token
        :param level: 登录的等级,0,1,2,3
        :param isv: 是否是isv，0--不是；1--是
        :return:
        """
        if (level, isv) in cls.token.keys():
            return cls.token[level, isv]
        if (level, isv) not in cls.token.keys():
            r = cls.login(level, isv)
            cls.token[level, isv] = {'token': r['return']['data']['token'], 'user_id': r['return']['data']['user_id'],
                                     'tenant_id': r['tenant_id']}
        return cls.token[level, isv]

    @classmethod
    def get_sale_token(cls, isv_sale=isv_sale):
        """
        获取业务员登录的token,isv_sale:1--isv;0--不是isv
        :return:
        """
        username = ""
        password = ""
        tenant_id = ""
        if isv_sale in cls.token_sale.keys():
            return cls.token_sale[isv_sale]
        if isv_sale not in cls.token_sale.keys():
            if isv_sale == 0:
                tenant_id = cls.test_sale_our['tenant-id']
                username = cls.test_sale_our['username']
                password = cls.test_sale_our['password']
            elif isv_sale == 1:
                tenant_id = cls.test_sale_isv['tenant-id']
                username = cls.test_sale_isv['username']
                password = cls.test_sale_isv['password']
            else:
                print('参数错误')
            r = requests.post(
                url=cls.ucenter_access_login_url,
                json={"username": username, 'password': password}
            )
            nauth_token = r.json()['data']['nauth_token']
            r = requests.post(
                url=cls.new_login_url,
                headers={'tenant-id': tenant_id},
                json={"token": nauth_token, 'login_type': 'saleman'}
            )
            cls.token_sale[isv_sale] = {'token': r.json()['data']['token'], 'user_id': r.json()['data']['user_id'],
                                        'tenant_id': tenant_id}
        return cls.token_sale[isv_sale]

    @classmethod
    def login(cls, level, isv):
        username = ""
        password = ""
        tenant_id = ""
        if isv == 0:
            tenant_id = cls.test_user_our_0['tenant-id']
            if level == 0:
                username = cls.test_user_our_0['username']
                password = cls.test_user_our_0['password']
            elif level == 1:
                username = cls.test_user_our_1['username']
                password = cls.test_user_our_1['password']
            elif level == 2:
                username = cls.test_user_our_2['username']
                password = cls.test_user_our_2['password']
            elif level == 3:
                username = cls.test_user_our_3['username']
                password = cls.test_user_our_3['password']
            else:
                print("入参错误，请重新传参")
        elif isv == 1:
            tenant_id = cls.test_user_isv_0['tenant-id']
            if level == 0:
                username = cls.test_user_isv_0['username']
                password = cls.test_user_isv_0['password']
            elif level == 1:
                username = cls.test_user_isv_1['username']
                password = cls.test_user_isv_1['password']
            elif level == 2:
                username = cls.test_user_isv_2['username']
                password = cls.test_user_isv_2['password']
            elif level == 3:
                username = cls.test_user_isv_3['username']
                password = cls.test_user_isv_3['password']
            else:
                print("入参错误，请重新传参")
        r = requests.post(
            url=cls.ucenter_login_url,
            json={"username": username, 'password': password}
        )
        nauth_token = r.json()['data']['nauth_token']
        r = requests.post(
            url=cls.new_login_url,
            headers={'tenant-id': tenant_id, 'device-uuid': cls.device_uuid},
            json={"token": nauth_token, 'login_type': 'agent'}
        )
        return {'return': r.json(), 'tenant_id': tenant_id}

    @classmethod
    def get_db_data(cls, db='agent_61000001'):
        """获取数据库信息进行匹配"""
        con = connect_DataBase(db)
