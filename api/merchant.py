import requests

from api.agentapp import AgentApp


class Merchant(AgentApp):

    def get_merchant_list(self, token, user_id, tenant_id, **kwargs):
        """直属商户列表"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/get-merchant-list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_merchant_list_data(self, user_id, tenant_id, page, pagesize):
        """获取直属商户列表中的data"""
        conn = self.conn_db(dbdata='merchants')
        conn_agent = self.conn_db(dbdata='agent_' + tenant_id)
        conn_mongo = self.conn_db_mongo()

        # 各种table
        merchant_table = conn.get_table('merchants')
        merchant_details_table = conn.get_table('merchant_details')
        stores_table = conn.get_table('stores')
        staffs_table = conn.get_table('staffs')
        agent_table = conn_agent.get_table('agent')

        length = conn.find_count(merchant_table, merchant_table.agent_num == user_id, merchant_table.is_del == 0)
        pages = self.get_pages(length, pagesize)

        data = {
            'list': [],
            'total_records': length,
            'pages': pages,
            'page': page
        }

        merchant_list_all = conn.session.query(merchant_table).filter(
            merchant_table.agent_num == user_id, merchant_table.is_del == 0).order_by(
            merchant_table.created_at.desc()).all()
        merchant_list = self.get_list_by_page(merchant_list_all, pagesize, page)

        for merchant_data in merchant_list:
            last_payed_at = 0
            if merchant_data.last_payed_at > 0:
                last_payed_at = self.get_time(merchant_data.last_payed_at)
            data['list'].append(
                {
                    'merchant_num': merchant_data.merchant_num,
                    'full_name': merchant_data.full_name,
                    'contact_phone': conn.find(merchant_details_table,
                                               merchant_num=merchant_data.merchant_num).contact_phone,
                    'create_at': merchant_data.created_at,
                    'update_at': merchant_data.updated_at,
                    'store_total': str(
                        conn.find_count(stores_table, stores_table.merchant_num == merchant_data.merchant_num)),
                    'staff_total': str(
                        conn.find_count(staffs_table, staffs_table.merchant_num == merchant_data.merchant_num)),
                    'agent_name': conn_agent.find(agent_table, agent_num=merchant_data.agent_num).agent_name,
                    'leader_name': merchant_data.leader_name,
                    'last_payed_at': last_payed_at,
                    'channels': conn_mongo.get_merchant_user_channel_name_list(merchant_data.merchant_num)
                }
            )
        self.close_db(conn)
        self.close_db(conn_agent)
        self.close_db_mongo(conn_mongo)
        return data

    def get_merchant_list_data_by_fullname(self, user_id, page, tenant_id, full_name, pagesize):
        """根据full_name 查询data"""

        conn = self.conn_db(dbdata='merchants')
        conn_agent = self.conn_db(dbdata='agent_%s' % tenant_id)
        conn_mongo = self.conn_db_mongo()

        full_name = '%' + full_name + '%'

        # 各种table
        merchant_table = conn.get_table('merchants')
        merchant_details_table = conn.get_table('merchant_details')
        stores_table = conn.get_table('stores')
        staffs_table = conn.get_table('staffs')
        agent_table = conn_agent.get_table('agent')

        length = conn.find_count(merchant_table, merchant_table.agent_num == user_id, merchant_table.is_del == 0,
                                 merchant_table.full_name.like(full_name))
        pages = self.get_pages(length, pagesize)

        data = {
            'list': [],
            'total_records': length,
            'pages': pages,
            'page': page
        }

        merchant_list_all = conn.session.query(merchant_table).filter(
            merchant_table.agent_num == user_id, merchant_table.is_del == 0,
            merchant_table.full_name.like(full_name)).order_by(
            merchant_table.created_at.desc()).all()
        merchant_list = self.get_list_by_page(merchant_list_all, pagesize, page)

        for merchant_data in merchant_list:
            last_payed_at = 0
            if merchant_data.last_payed_at > 0:
                last_payed_at = self.get_time(merchant_data.last_payed_at)
            data['list'].append(
                {
                    'merchant_num': merchant_data.merchant_num,
                    'full_name': merchant_data.full_name,
                    'contact_phone': conn.find(merchant_details_table,
                                               merchant_num=merchant_data.merchant_num).contact_phone,
                    'create_at': merchant_data.created_at,
                    'update_at': merchant_data.updated_at,
                    'store_total': str(
                        conn.find_count(stores_table, stores_table.merchant_num == merchant_data.merchant_num)),
                    'staff_total': str(
                        conn.find_count(staffs_table, staffs_table.merchant_num == merchant_data.merchant_num)),
                    'agent_name': conn_agent.find(agent_table, agent_num=merchant_data.agent_num).agent_name,
                    'leader_name': merchant_data.leader_name,
                    'last_payed_at': last_payed_at,
                    'channels': conn_mongo.get_merchant_user_channel_name_list(merchant_data.merchant_num)
                }
            )
        self.close_db(conn)
        self.close_db(conn_agent)
        self.close_db_mongo(conn_mongo)
        return data

    def get_sub_merchant_list(self, token, user_id, tenant_id, **kwargs):
        """下属商户列表查询"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/sub-merchant-list'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_sub_merchant_list_data(self, user_id, tenant_id, page, pagesize):
        """获取下属商户列表中的data"""
        conn = self.conn_db(dbdata='merchants')
        conn_agent = self.conn_db(dbdata='agent_' + tenant_id)
        conn_mongo = self.conn_db_mongo()

        # 各种table
        merchant_table = conn.get_table('merchants')
        merchant_details_table = conn.get_table('merchant_details')
        stores_table = conn.get_table('stores')
        staffs_table = conn.get_table('staffs')
        agent_table = conn_agent.get_table('agent')

        sub_agent_list = conn_agent.get_sub_agent_list(user_id)

        merchant_list_all = conn.session.query(merchant_table).filter(
            merchant_table.agent_num.in_(sub_agent_list), merchant_table.is_del == 0).order_by(
            merchant_table.created_at.desc()).all()
        merchant_list = self.get_list_by_page(merchant_list_all, pagesize, page)
        length = len(merchant_list_all)
        pages = self.get_pages(length, pagesize)

        data = {
            'list': [],
            'total_records': length,
            'pages': pages,
            'page': page
        }

        for merchant_data in merchant_list:
            last_payed_at = 0
            if merchant_data.last_payed_at > 0:
                last_payed_at = self.get_time(merchant_data.last_payed_at)
            data['list'].append(
                {
                    'merchant_num': merchant_data.merchant_num,
                    'full_name': merchant_data.full_name,
                    'contact_phone': conn.find(merchant_details_table,
                                               merchant_num=merchant_data.merchant_num).contact_phone,
                    'create_at': merchant_data.created_at,
                    'update_at': merchant_data.updated_at,
                    'store_total': str(
                        conn.find_count(stores_table, stores_table.merchant_num == merchant_data.merchant_num)),
                    'staff_total': str(
                        conn.find_count(staffs_table, staffs_table.merchant_num == merchant_data.merchant_num)),
                    'agent_name': conn_agent.find(agent_table, agent_num=merchant_data.agent_num).agent_name,
                    'leader_name': merchant_data.leader_name,
                    'last_payed_at': last_payed_at,
                    'channels': conn_mongo.get_merchant_user_channel_name_list(merchant_data.merchant_num)
                }
            )
        self.close_db(conn)
        self.close_db(conn_agent)
        self.close_db_mongo(conn_mongo)
        return data

    def get_sub_merchant_list_data_by_fullname(self, user_id, tenant_id, page, pagesize, fullname):
        """根据fullname模糊查询下属商户"""
        conn = self.conn_db(dbdata='merchants')
        conn_agent = self.conn_db(dbdata='agent_' + tenant_id)
        conn_mongo = self.conn_db_mongo()

        # 各种table
        merchant_table = conn.get_table('merchants')
        merchant_details_table = conn.get_table('merchant_details')
        stores_table = conn.get_table('stores')
        staffs_table = conn.get_table('staffs')
        agent_table = conn_agent.get_table('agent')

        sub_agent_list = conn_agent.get_sub_agent_list(user_id)

        merchant_list_all = conn.session.query(merchant_table).filter(
            merchant_table.agent_num.in_(sub_agent_list), merchant_table.is_del == 0,
            merchant_table.full_name.like('%' + fullname + '%')).order_by(
            merchant_table.created_at.desc()).all()
        merchant_list = self.get_list_by_page(merchant_list_all, pagesize, page)
        length = len(merchant_list_all)
        pages = self.get_pages(length, pagesize)

        data = {
            'list': [],
            'total_records': length,
            'pages': pages,
            'page': page
        }

        for merchant_data in merchant_list:
            last_payed_at = 0
            if merchant_data.last_payed_at > 0:
                last_payed_at = self.get_time(merchant_data.last_payed_at)
            data['list'].append(
                {
                    'merchant_num': merchant_data.merchant_num,
                    'full_name': merchant_data.full_name,
                    'contact_phone': conn.find(merchant_details_table,
                                               merchant_num=merchant_data.merchant_num).contact_phone,
                    'create_at': merchant_data.created_at,
                    'update_at': merchant_data.updated_at,
                    'store_total': str(
                        conn.find_count(stores_table, stores_table.merchant_num == merchant_data.merchant_num)),
                    'staff_total': str(
                        conn.find_count(staffs_table, staffs_table.merchant_num == merchant_data.merchant_num)),
                    'agent_name': conn_agent.find(agent_table, agent_num=merchant_data.agent_num).agent_name,
                    'leader_name': merchant_data.leader_name,
                    'last_payed_at': last_payed_at,
                    'channels': conn_mongo.get_merchant_user_channel_name_list(merchant_data.merchant_num)
                }
            )
        self.close_db(conn)
        self.close_db(conn_agent)
        self.close_db_mongo(conn_mongo)
        return data

    def get_loss_merchant_list(self, token, user_id, tenant_id, **kwargs):
        """流失商户列表"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/loss-merchant-list'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_loss_merchant_list_data(self, user_id, tenant_id, page, pagesize, **kwargs):
        """获取流失商户中的data"""
        conn = self.conn_db(dbdata='merchants')
        conn_agent = self.conn_db(dbdata='agent_' + tenant_id)
        conn_mongo = self.conn_db_mongo()

        # 各种table
        merchant_table = conn.get_table('merchants')
        merchant_details_table = conn.get_table('merchant_details')
        stores_table = conn.get_table('stores')
        staffs_table = conn.get_table('staffs')
        agent_table = conn_agent.get_table('agent')

        agent_list = conn_agent.get_sub_agent_list(user_id)
        agent_list.append(user_id)
        loss_time_norm = self.get_now() - 2 * 24 * 60 * 60

        if 'full_name' in kwargs.keys():
            merchant_list_all = conn.session.query(merchant_table).filter(
                merchant_table.agent_num.in_(agent_list),
                merchant_table.full_name.like('%' + kwargs['full_name'] + '%')).order_by(
                merchant_table.created_at.desc()).all()
            for data in merchant_list_all:
                if data.last_payed_at==0:
                    if str(data.created_at)>=self.get_time(loss_time_norm):
                        merchant_list_all.remove(data)
                else:
                    if data.last_payed_at>=loss_time_norm:
                        merchant_list_all.remove(data)
        else:
            merchant_list_all = conn.session.query(merchant_table).filter(
                merchant_table.agent_num.in_(agent_list)).order_by(
                merchant_table.created_at.desc()).all()
            for m_data in merchant_list_all:
                print(0, m_data.merchant_num,m_data.last_payed_at)
                if m_data.last_payed_at==0:
                    print(1,m_data.merchant_num)
                    if str(m_data.created_at)>=self.get_time(loss_time_norm):
                        print(2, m_data.merchant_num)
                        merchant_list_all.remove(m_data)
                else:
                    print(3,m_data.merchant_num)
                    if m_data.last_payed_at>=loss_time_norm:
                        print(4, m_data.merchant_num)
                        merchant_list_all.remove(m_data)

        merchant_list = self.get_list_by_page(merchant_list_all, pagesize, page)
        length = len(merchant_list_all)
        pages = self.get_pages(length, pagesize)

        data = {
            'list': [],
            'total_records': length,
            'pages': pages,
            'page': page
        }

        for merchant_data in merchant_list:
            last_payed_at = merchant_data.created_at
            if merchant_data.last_payed_at > 0:
                last_payed_at = self.get_time(merchant_data.last_payed_at)
            is_directly = 2
            if merchant_data.agent_num == user_id:
                is_directly = 1
            data['list'].append(
                {
                    'merchant_num': merchant_data.merchant_num,
                    'full_name': merchant_data.full_name,
                    'contact_phone': conn.find(merchant_details_table,
                                               merchant_num=merchant_data.merchant_num).contact_phone,
                    'create_at': str(merchant_data.created_at),
                    'update_at': str(merchant_data.updated_at),
                    'store_total': str(
                        conn.find_count(stores_table, stores_table.merchant_num == merchant_data.merchant_num)),
                    'staff_total': str(
                        conn.find_count(staffs_table, staffs_table.merchant_num == merchant_data.merchant_num)),
                    'agent_name': conn_agent.find(agent_table, agent_num=merchant_data.agent_num).agent_name,
                    'leader_name': merchant_data.leader_name,
                    'last_payed_at': last_payed_at,
                    'channels': conn_mongo.get_merchant_user_channel_name_list(merchant_data.merchant_num),
                    'is_directly': is_directly
                }
            )
        self.close_db(conn)
        self.close_db(conn_agent)
        self.close_db_mongo(conn_mongo)
        return data

    def get_idcard_type(self, token, user_id, tenant_id):
        """获取商户证件类型"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/get-idcard-type'
        r = requests.get(url=url, headers=headers)
        self.format(r)
        return r.json()

    def get_merchant_info(self, token, user_id, tenant_id, merchant_num):
        """获取商户信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        params = {'merchant_num': merchant_num}
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/get-merchant-info'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_merchant_info_data(self, merchant_num, user_id, tenant_id, ):
        """获取商户信息--data"""
        conn = self.conn_db(dbdata='merchants')
        conn_agent = self.conn_db(dbdata='agent_' + tenant_id)
        conn_tenant = self.conn_db(dbdata='tenant')
        conn_ucenter = self.conn_db(dbdata='ucenter')

        merchant_table = conn.get_table('merchants')
        merchant_details_table = conn.get_table('merchant_details')
        region_table = conn_tenant.get_table('region')
        agent_table = conn_agent.get_table('agent')
        user_table = conn_ucenter.get_table('user')
        merchant_photos_table = conn.get_table('merchant_photos')

        merchant_data = conn.find(merchant_table, merchant_num=merchant_num)
        merchant_details_data = conn.find(merchant_details_table, merchant_num=merchant_num)
        agent_data = conn_agent.find(agent_table, agent_num=merchant_data.agent_num)
        user_data = conn_ucenter.find(user_table, user_num=merchant_data.user_num)
        merchant_photos_data = conn.session.query(merchant_photos_table).filter(
            merchant_photos_table.merchant_num == merchant_num).all()

        sale_name = ''
        if merchant_data.sale_num != '':
            saleman_table = conn_agent.get_table('saleman')
            saleman_data = conn_agent.find(saleman_table, agent_num=merchant_data.agent_num,
                                           saleman_num=merchant_data.sale_num)
            sale_name = saleman_data.name

        area = []
        if [merchant_data.province, merchant_data.city, merchant_data.area] != ['', '', '']:
            area = [merchant_data.province, merchant_data.city, merchant_data.area]

        bank_area = []
        if [merchant_details_data.bank_province, merchant_details_data.bank_city,
            merchant_details_data.bank_area] != ['', '', '']:
            bank_area = [merchant_details_data.bank_province, merchant_details_data.bank_city,
                         merchant_details_data.bank_area]

        data = {
            'id': merchant_data.id,
            'contact_name': merchant_details_data.contact_name,
            'contact_phone': merchant_details_data.contact_phone,
            'contact_id_no': merchant_details_data.contact_id_no,
            'contact_email': merchant_details_data.contact_email,
            'sale_num': merchant_data.sale_num,
            'agent_num': merchant_data.agent_num,
            'user_num': merchant_data.user_num,
            'tenant_num': merchant_data.tenant_num,
            'merchant_num': merchant_num,
            'type': merchant_data.type,
            'full_name': merchant_data.full_name,
            'short_name': merchant_data.short_name,
            'province': merchant_data.province,
            'city': merchant_data.city,
            'area': area,
            'real_address': merchant_details_data.real_address,
            'service_phone': merchant_data.service_phone,
            'bus_licence_no': merchant_details_data.bus_licence_no,
            'bus_licence_reg_date': merchant_details_data.bus_licence_reg_date,
            'bus_licence_expire': merchant_details_data.bus_licence_expire,
            'leader_name': merchant_data.leader_name,
            'leader_phone': merchant_details_data.leader_phone,
            'leader_id_type': merchant_details_data.leader_id_type,
            'leader_id_no': merchant_details_data.leader_id_no,
            'leader_id_effective_date': merchant_details_data.leader_id_effective_date,
            'leader_id_expire': merchant_details_data.leader_id_expire,
            'bank_account_name': merchant_details_data.bank_account_name,
            'bank_account_no': merchant_details_data.bank_account_no,
            'bank_name': merchant_details_data.bank_name,
            'bank_name_code': merchant_details_data.bank_name_code,
            'bank_branch_name': merchant_details_data.bank_branch_name,
            'bank_branch_code': merchant_details_data.bank_branch_code,
            'bank_province': merchant_details_data.bank_province,
            'bank_city': merchant_details_data.bank_city,
            'bank_area': bank_area,
            'bank_address': merchant_details_data.bank_address,
            'bank_pre_mobile': merchant_details_data.bank_pre_mobile,
            'bank_account_type': merchant_details_data.bank_account_type,
            'contact_chk_status': conn.get_chk_status('contact_chk_status', merchant_num),
            'leader_chk_status': conn.get_chk_status('leader_chk_status', merchant_num),
            'base_chk_status': conn.get_chk_status('base_chk_status', merchant_num),
            'bank_chk_status': conn.get_chk_status('bank_chk_status', merchant_num),
            'area_name': conn_tenant.get_areaname_by_code_merchant(region_table,
                                                                   [merchant_data.province, merchant_data.city,
                                                                    merchant_data.area]),
            'bank_area_name': conn_tenant.get_areaname_by_code_merchant(region_table,
                                                                        [merchant_details_data.bank_province,
                                                                         merchant_details_data.bank_city,
                                                                         merchant_details_data.bank_area]),
            'sale_name': sale_name,
            'agent_name': agent_data.agent_name,
            'mobile': user_data.mobile,
            'leader_id_type_name': conn.get_id_type_name(merchant_details_data.leader_id_type),
            'bank_id_card_type_name': conn.get_id_type_name(merchant_details_data.bank_id_card_type),
            'bank_id_card_effective': merchant_details_data.bank_id_card_effective,
            'bank_id_card_expire': merchant_details_data.bank_id_card_expire,
            'bank_id_card_no': merchant_details_data.bank_id_card_no,
            'bank_id_card_type': merchant_details_data.bank_id_card_type
        }

        if merchant_photos_data != None:
            bus_licence_oth = []
            conn_bus_licence_oth = conn.get_merchant_photo_url(merchant_photos_table, merchant_num,
                                                               'bus_licence_oth')
            if conn_bus_licence_oth != '[]' and conn_bus_licence_oth != '':
                print(conn_bus_licence_oth)
                out_list = ["[", "\"", "\'", "]"]
                for out in out_list:
                    conn_bus_licence_oth=conn_bus_licence_oth.replace(out, '')
                bus_licence_oth = conn_bus_licence_oth.split(',')

            for photo_code in conn.get_photo_code_list(merchant_photos_data):
                if photo_code == 'bus_licence_oth':
                    data[photo_code] = bus_licence_oth
                else:
                    data[photo_code] = conn.get_merchant_photo_url(merchant_photos_table, merchant_num, photo_code)
        # if conn.get_chk_status('bank_chk_status', merchant_num) != 0:
        #     data['bank_id_card_type_name']=conn.get_id_type_name(merchant_details_data.bank_id_card_type)
        # else:
        #     data['bank_id_card_type_name']=''

        conn.close_session()
        conn_agent.close_session()
        conn_tenant.close_session()
        conn_ucenter.close_session()
        return data

    def is_enable_register(self, token, user_id, tenant_id, mobile):
        """判断手机号是否可以注册"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        params = {'mobile': mobile}
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/is-enable-register'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_mobile(self,type):
        """
        从数据库中查询一个电话
        type:不同类型的电话
        """
        if type=='new':
            """新号码"""
            conn = self.conn_db(dbdata='test_data')
            user_mobile_table = conn.get_table('user_mobile')
            user_mobile_data = conn.find(user_mobile_table, code='creat_merchant')
            mobile = user_mobile_data.mobile
            return {'mobile':mobile,'user_num':''}
        elif type=='useder':
            """已经注册过商户的号码"""
            conn = self.conn_db(dbdata='test_data')
            user_mobile_table = conn.get_table('user_mobile')
            user_mobile_data = conn.find(user_mobile_table, code='creat_merchant')
            mobile = user_mobile_data.mobile
            return {'mobile':str(int(mobile)-1)}
        elif type=='old':
            """代理商账号，但是没有注册过商户"""
            conn=self.conn_db(dbdata='ucenter')
            user_table=conn.get_table('user')
            user_seat_table=conn.get_table('user_seat')
            merchant_user_num_data=conn.find_all(user_seat_table,user_seat_table.seat==2000)
            user_num_list=[]
            for data in merchant_user_num_data:
                user_num_list.append(data.user_num)
            agent_user_data=conn.find_all(user_table,user_table.user_num.notin_(user_num_list))
            agent_user_num_list = []
            for data in agent_user_data:
                agent_user_num_list.append({'user_num':data.user_num,'mobile':data.mobile})
            return agent_user_num_list[0]
        else:
            print('入参错误，请重新提交')
            return ''

    def create(self, token, user_id, tenant_id, **kwargs):
        """添加商户"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        # 获取创建商户的mobile
        conn = self.conn_db(dbdata='test_data')
        user_mobile_table = conn.get_table('user_mobile')
        user_mobile_data = conn.find(user_mobile_table, code='creat_merchant')
        mobile = user_mobile_data.mobile

        data = {'mobile': mobile}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/create'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        # 更新测试数据库的mobile
        user_mobile_data.mobile = str(int(user_mobile_data.mobile) + 1)
        conn.session.commit()
        return r.json()

    def edit_base_info(self, token, user_id, tenant_id, merchant_num, **kwargs):
        """编辑基本资料"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        data = {'merchant_num': merchant_num}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/edit-base-info'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def edit_merchant_info(self, token, user_id, tenant_id, merchant_num, **kwargs):
        """编辑商户信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        data = {'merchant_num': merchant_num}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/edit-merchant-info'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def edit_leader_info(self, token, user_id, tenant_id, merchant_num, **kwargs):
        """编辑法人信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        data = {'merchant_num': merchant_num}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/edit-leader-info'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def edit_bank_info(self, token, user_id, tenant_id, merchant_num, **kwargs):
        """编辑账户信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-Version': AgentApp.Api_Version
        }
        data = {'merchant_num': merchant_num}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/merchant/merchant/edit-bank-info'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

