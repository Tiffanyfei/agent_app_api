import requests
import time
from api.agentapp import AgentApp

class Agent(AgentApp):

    def send_register_code(self, token, user_id, tenant_id, telphone):
        """发送短信验证码"""
        header = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        params = {'telphone': telphone}
        url = AgentApp.fws + '/appapi/v4/agent/agent/send-register-code'
        r = requests.get(url=url, headers=header, params=params)
        self.format(r)
        return r.json()

    def is_enable_register(self,token,user_id, tenant_id, mobile):
        """判断是否可注册"""
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
        url = AgentApp.fws + '/appapi/v4/agent/agent/is-enable-register'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def creat_agent_1(self, token, user_id, tenant_id, telphone, **kwargs):
        """添加代理商信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        data = {'telphone': telphone}
        data.update(kwargs)

        """kwargs 需要多个参数时不需要过多定义"""
        # params.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/agent/agent/add'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def edit_agent_1(self, token, user_id, tenant_id, agent_num, **kwargs):
        """编辑代理商信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        data = {'agent_num': agent_num}
        data.update(kwargs)
        url = AgentApp.fws + 'appapi/v4/agent/agent/edit'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()


    def my_agent_list(self, token, user_id, tenant_id, **kwargs):
         """直属代理商列表"""
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
         url = AgentApp.fws + '/appapi/v4/agent/agent/my-agent-list'
         r =requests.get(url=url, headers=headers, params=params)
         self.format(r)
         return r.json()

    def get_agent_list_data(self, user_id, page, tenant_id, pagesize):
        """数据库链接"""
        conn = self.conn_db(dbdata='agent_61000001')
        """ %s 将ISV贴牌作为一个变量 """
        # conn_agent=self.conn_db(dbdata='agent_%s'%tenant_id)
        # conn_merchants = self.conn_db(dbdata='merchants')
        lenght = len(conn.get_dir_agent_list(user_id))
        pages = self.get_pages(lenght, 20)
        data = {
            'list': [],
            'total_records': lenght,
            'pages': page,
            'page': page
        }

        # 拼接list的内容
        agent_list = self.get_list_by_page(list=conn.get_dir_agent_list(user_id), pagesize=pagesize, page=page)
        for agent_num in agent_list:
            data['list'].append(
                {
                    'agent_name': conn.get_agent_name(agent_num),
                    'agent_num': agent_num,
                    'telphone': conn.get_dir_agent_list(agent_num)['telphone'],
                    'respo_name': conn.get_dir_agent_list(agent_num)['respo_name'],
                    'p_agent_name': conn.get_dir_agent_list(agent_num)['p_agent_name'],
                    'p_num': conn.get_dir_agent_list(agent_num)['p_num'],
                    'status': conn.get_dir_agent_list(agent_num)['status'],
                    'bank_chk_status': conn.get_dir_agent_list(agent_num)['bank_chk_status'],
                    'day_make_code_limit': conn.get_dir_agent_list(agent_num)['day_make_code_limit'],
                    'start_time': conn.get_dir_agent_list(agent_num)['start_time'],
                    'expire_time': conn.get_dir_agent_list(agent_num)['expire_time'],
                    'agent_region': conn.get_dir_agent_list(agent_num)['agent_region'],
                    'level': conn.get_dir_agent_list(agent_num)['level'],
                    'is_sub': conn.get_dir_agent_list(agent_num)['is_sub'],
                    'is_market': conn.get_dir_agent_list(agent_num)['is_market'],
                    'created_at': conn.get_dir_agent_list(agent_num)['created_at'],
                    'merchant_count': conn.get_agent_merchant_count(agent_num),
                }

            )
            self.close_db(conn)
            return data
        # 根据 agent_num查询data



    def sub_agent_list(self, token, user_id, tenant_id, **kwargs):
     """下属代理商列表"""
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
     url = AgentApp.fws + '/appapi/v4/agent/agent/sub-agent-list'
     r =requests.get(url=url, headers=headers, params=params)
     self.format(r)
     return r.json()


    def get_agent_info(self, token, user_id, tenant_id, agent_num):
     """获取代理商信息"""
     headers = {
         'tenant-id': tenant_id,
         'user-auth-token': token,
         'user-login-type': AgentApp.agent_login_type,
         'device-uuid': AgentApp.device_uuid,
         'user-id': user_id,
         'agent-app': AgentApp.agent_app,
         'Api-version': AgentApp.Api_Version,
     }
     params = {'agent_num': agent_num}
     url = AgentApp.fws + '/appapi/v4/agent/agent/info'
     r = requests.get(url=url, headers=headers, params=params)
     self.format(r)
     return r.json()

    def get_channel_rates_config(self, token, user_id, tenant_id, agent_num):
        """获取通道费率结构"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        params = {'agent_num': agent_num}
        url = AgentApp.fws + '/appapi/v4/agent/agent/channel-rates-config'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    # def channel_rates_update(self, token, user_id, tenant_id, agent_num, **kwargs):
    #     """编辑代理商费率"""
    #     headers = {
    #         'tenant-id': tenant_id,
    #         'user-auth-token': token,
    #         'user-login-type': AgentApp.agent_login_type,
    #         'device-uuid': AgentApp.device_uuid,
    #         'user-id': user_id,
    #         'agent-app': AgentApp.agent_app,
    #         'Api-version': AgentApp.Api_Version,
    #     }
    #     data = {'agent_num': agent_num}
    #     data.update(kwargs)
    #     url = AgentApp.fws + '/appapi/v4/agent/agent/channel-rates-update'
    #     r = requests.post(url=url, json=data, headers=headers)
    #     self.format(r)
    #     return r.json()

    def update_agent_bank_info(self, token, user_id, tenant_id, **kwargs):
        """修改代理商账号信息"""
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
        # data = {'agent_num': 701001017}
        # data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/agent/agent/update-agent-bank-info'
        r = requests.post(url=url, json=params, headers=headers)
        self.format(r)
        return r.json()