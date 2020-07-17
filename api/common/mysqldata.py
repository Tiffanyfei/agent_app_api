from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from api.baseapi import BaseApi


class MysqlData(BaseApi):
    """
    使用sqlalchemy、automap连接现有数据库查询数据
    """

    def __init__(self, dbname, dbconfig):
        self.uri = 'mysql+pymysql://' + dbconfig['user'] + ':' + dbconfig['password'] + \
                   '@' + dbconfig['host'] + ':' + str(dbconfig['port']) + '/' + dbname + '?charset=utf8mb4'
        self.engine = create_engine(self.uri, echo=False)
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        self.Base.classes.keys()
        self.session = Session(self.engine)

    def close_session(self):
        """关闭当前的session"""
        self.session.close_all()

    def get_table(self, table_name):
        """获取table"""
        table = self.Base.classes.__getitem__(key=table_name)
        return table

    def find(self, table, **kwargs):
        """单条查询"""
        #agent_num='123456'
        result = self.session.query(table).filter_by(**kwargs).first()
        return result

    def find_all(self, table, *criterion):
        """多条查询"""
        #agent_num=='123456'
        result = self.session.query(table).filter(*criterion).all()
        return result

    def find_count(self, table, *criterion):
        """获取条件查询后的list长度"""
        result = self.session.query(table).filter(*criterion).count()
        return result

    def get_sub_agent_list(self, agent_num):
        table = self.get_table('agent')
        my_agent_list_1 = []
        my_agent_list_2 = []
        my_agent_list_3 = []
        for agent in self.session.query(table).filter(table.p_num == agent_num).all():
            my_agent_list_1.append(agent.agent_num)
        for agent in self.session.query(table).filter(table.p_num.in_(my_agent_list_1)).all():
            my_agent_list_2.append(agent.agent_num)
        for agent in self.session.query(table).filter(table.p_num.in_(my_agent_list_2)).all():
            my_agent_list_3.append(agent.agent_num)

        sub_agent_list = my_agent_list_1 + my_agent_list_2 + my_agent_list_3
        return sub_agent_list

    def get_merchant_photo_url(self, table, merchant_num, code):
        data = self.find(table, code=code, merchant_num=merchant_num)
        if data == None:
            photo_url = ''
        else:
            photo_url = data.photo_url
        return photo_url

    def get_chk_status(self, chk_section, merchant_num):
        """返回商户每个部分的资料状态"""
        merchant_table = self.get_table('merchants')
        merchant_details_data = self.get_table('merchant_details')
        status = 0

        if chk_section == 'contact_chk_status':
            key = self.find(merchant_details_data, merchant_num=merchant_num)
            key = key.contact_name
        elif chk_section == 'leader_chk_status':
            key = self.find(merchant_table, merchant_num=merchant_num)
            key = key.leader_name
        elif chk_section == 'base_chk_status':
            key = self.find(merchant_table, merchant_num=merchant_num)
            key = key.full_name
        elif chk_section == 'bank_chk_status':
            key = self.find(merchant_details_data, merchant_num=merchant_num)
            key = key.bank_account_no
        else:
            key = ''
        if key != '':
            status = 20
        return status

    def get_areaname_by_code_merchant(self, table, area: list):
        """返回area对应的name"""
        result = ''
        for code in area:
            name = self.find(table, code=code)
            if name != None:
                name = name.alias
                result = result + name + '-'
        return result[:-1]

    def get_id_type_name(self, type):
        """获取证件的name"""
        name = ''
        if type == 1:
            name = '身份证'
        elif type == 2:
            name = '港澳台通行证'
        elif type == 3:
            name = '台湾身份证'
        elif type == 4:
            name = '香港身份证'
        elif type == 5:
            name = '澳门身份证'
        elif type == 9:
            name = '其它'
        return name

    def get_photo_code_list(self, data_list):
        code_list = []
        if data_list != None:
            for i in data_list:
                code_list.append(i.code)
        return code_list

