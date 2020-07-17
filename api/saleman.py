import requests

from api.agentapp import AgentApp

class Saleman(AgentApp):
    def get_saleman_list(self, token, user_id, tenant_id, **kwargs):
        """业务员列表"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device_uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/saleman/saleman/list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_saleman_list_data(self):
        """数据库查询"""
        conn = self.conn_db(dbdata='agent_61000001')
        lenght = len(conn.get_saleman_list())
        pages = self.get_pages(lenght,20)
        data = {
            'list': [],
            'total_records': lenght,
            'pages': pages,
            'page': pages
        }
        # 拼接list内容
        saleman_list=self.get_list_by_page(list=conn.get_saleman_list)
        for saleman_num in saleman_list:
            info = conn.get_saleman_info(saleman_num)
            data['list'].append(
                {
                    'name': conn.get_saleman_name(saleman_num),
                    'saleman_num': saleman_num,
                    'phone': conn.get_saleman_phone(saleman_num),
                    'contact_phone': conn.get_saleman_create_at(saleman_num),
                    'create_at': conn.get_saleman_create_at(saleman_num)
                }

            )
            self.close_db(conn)
            return data



    def get_saleman_info(self, token, user_id, tenant_id, sale_num):
        """业务员列表"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device_uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        params = {'sale_num': sale_num}
        url = AgentApp.fws + '/appapi/v4/saleman/saleman/query-salesman'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def saleman_insert_sale(self, token, user_id, tenant_id,**kwargs):
        """新增业务员"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device_uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/saleman/saleman/insert-sale'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def saleman_update_sale(self, token, user_id, tenant_id,**kwargs):
        """修改业务员"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device_uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/saleman/saleman/update-sale'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def saleman_channel_rates_config(self, token, user_id, tenant_id,**kwargs):
        """获取展业规则费率结构"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device_uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/saleman/saleman/channel-rates-config'
        r = requests.get(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()


    def saleman_business_flow_list(self, token, user_id, tenant_id,**kwargs):
        """获取业务员数据列表"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device_uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/saleman/saleman/business-flow-list'
        r = requests.get(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()


    """
    业务员APP相关接口
    """

    def get_saleman_records(self, token, user_id, tenant_id, **kwargs):
        """业务员数据列表"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/records'
        r = requests.get(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def get_saleman_send_register_code(self, token, user_id, tenant_id, **kwargs):
        """修改密码发送验证码"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/send-register-code'
        r = requests.get(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def get_saleman_update_password(self, token, user_id, tenant_id, **kwargs):
        """修改密码"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/update-password'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()


    def get_saleman_notice_list(self, token, user_id, tenant_id, **kwargs):
        """业务员消息通知列表"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/notice-list'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def get_saleman_update_notice_status(self, token, user_id, tenant_id, **kwargs):
        """更改通知状态"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/update-notice-status'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_saleman_notify_num(self, token, user_id, tenant_id, **kwargs):
        """获取消息未读列表"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/notify-num'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()


    def get_saleman_get_sale_rates(self, token, user_id, tenant_id, **kwargs):
        """获取展业规则费率信息"""
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        params = {}
        params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/get-sale-rates'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_saleman_update_head_portrait(self, token, user_id, tenant_id,**kwargs):
        """修改头像 """
        headers = {
            'tenant_id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.saleman_login_type,
            'user-id': user_id,
            'agent-app': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/salemanapp/saleman/update-head-portrait'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()