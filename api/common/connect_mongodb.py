from pymongo import MongoClient

# from sshtunnel import SSHTunnelForwarder
from api.baseapi import BaseApi
from api.common.connect_db import connect_DataBase


class DataBase_Mongo(BaseApi):
    """
        连接数据库
        """

    def __init__(self, host: '', port: int, dbname: '', user: '', password: ''):

        self.conn = MongoClient(host=host, port=port).get_database(dbname)
        self.conn.authenticate(user, password)

        # ssh连接
        # self.server = SSHTunnelForwarder(ssh_address_or_host=('47.95.116.12', 22),
        #                                  ssh_username="developer",
        #                                  ssh_password="b0tf6hg3p3uvphpnuyuh63nm3bydhq",
        #                                  remote_bind_address=("127.0.0.1", 27017))
        # self.server.start()
        # self.conn = pymongo.MongoClient(host="127.0.0.1", port=self.server.local_bind_port,
        #                                 tz_aware=False).get_database('channel')
        # self.conn.authenticate("uphicoo", "uphicoo")

    def close_conn(self):
        self.conn.logout()

        # ssh连接
        # self.conn.logout()
        # self.server.close()

    def get_channel_name_by_id(self, id):
        """
        获取通道名称
        :param id:通道id
        :return:
        """
        collection = self.conn['channel_definition']
        result = collection.find({'id': id})
        return list(result)[0]['name']

    def get_merchant_own_channel_list(self, merchant_num):
        """
        获取商户拥有的通道的id的list
        :param merchant_num:
        :return:
        """
        collection = self.conn['merchant_own_channel']
        result = collection.find_one({'merchant_id': merchant_num})
        result_list = []
        if len(result) > 0:
            result_list = self.get_list(result['channels'])
        return result_list

    def get_merchant_use_channel_list(self, merchant_num):
        """
        获取商户使用的channel的id的list
        :param merchant_num:
        :return:
        """
        collection = self.conn['merchant_channel_config']
        list = collection.find_one({'merchant_id': merchant_num})
        result_list = []
        if list is not None:
            ll = []
            for l1 in self.get_list(list['configs']):
                for l2 in l1['channels']:
                    ll.append(l2['channel_id'])
            result_list_mb = self.get_list(ll)

            collection = self.conn['merchant_channel_data']
            list = collection.find({'merchant_id': merchant_num})
            res_list = []
            if list is not None:
                ll = []
                for data in list:
                    ll.append(data['channel_id'])
                res_list = self.get_list(ll)

            for code in result_list_mb:
                if code in res_list:
                    result_list.append(code)

        return result_list

    def get_merchant_user_channel_name_list(self, merchant_num):
        """商户使用的通道的name的list"""
        list = self.get_merchant_use_channel_list(merchant_num)
        result_list = []
        if len(list) > 0:
            for id in list:
                result_list.append({"channel_name": self.get_channel_name_by_id(id)})
        return result_list

    def get_agent_dir_merchant_own_channel_list(self, agent_num, status):
        """
        获取代理商直属商户的通道入驻列表
        :param agent_num:
        :param status:
        :return:
        """

        collection = self.conn['merchant_channel_data']
        result = collection.find({"agent_id": agent_num, "status": status})
        return self.get_result_list(result)

    def get_agent_dir_merchant_own_channel_list_by_merchant(self, agent_num, status):
        """
        获取代理商直属商户的通道入驻列表(代理商-商户维度）
        :param agent_num:
        :param status:
        :return:
        """

        collection = self.conn['merchant_channel_data']
        con = connect_DataBase()
        merchant_list = con.get_dir_merchant_list(agent_num)
        con.close_conn()
        result = collection.find({"merchant_id": {"$in": merchant_list}, "status": status})
        return self.get_result_list(result)

    def get_result_list(self, result):
        """
        遍历result，转换成list
        :param result:
        :return:
        """
        result_list = []
        for x in result:
            result_list.append(x)
        return result_list

    def get_sale_expend_merchant_own_channel(self, agent_num, sale_num, status):
        """
        获取业务员发展的商户的通道入驻列表
        :param agent_num:
        :param sale_num:
        :param atatus:
        :return:
        """
        collection = self.conn['merchant_channel_data']
        con = connect_DataBase()
        merchant_list = con.get_sale_expand_merchant_list_all(agent_num, sale_num)
        con.close_conn()
        result = collection.find({"merchant_id": {"$in": merchant_list}, "status": status})
        return self.get_result_list(result)

    def get_channel_mcht_fields_info(self, channel_id):
        """
        获取通道资料
        :param channel_id:
        :return:
        """
        collection = self.conn['channel_mcht_fields']
        result = collection.find_one({"id": channel_id})
        return result

    def get_channel_mcht_payment(self,channel_id):
        """
        获取通道的费率结构
        :param channel_id:
        :return:
        """
        collection = self.conn['channel_definition']
        result = collection.find_one({"id": channel_id})
        return result

    def get_merchant_channel_data(self,channel_id,merchant_num):
        """
        获取商户的入驻资料
        :param channel_id:
        :param merchant_num:
        :return:
        """
        collection = self.conn['merchant_channel_data']
        result=collection.find_one({"channel_id":channel_id,"merchant_id":merchant_num})
        return result


