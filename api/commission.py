import requests

from api.agentapp import AgentApp


class Commission(AgentApp):

     def get_commission_statistical_data(self, token ,user_id, tenant_id, **kwargs):
        """获取佣金提现统计 """
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
        url = AgentApp.fws + '/appapi/v4/finance/commission/statistical-data'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

     def get_commission_apply_list(self, token, user_id, tenant_id, **kwargs):
        """本级提现列表 """
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
        url = AgentApp.fws + '/appapi/v4/finance/commission/apply-list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

     def get_commission_sub_apply_list(self, token, user_id, tenant_id, **kwargs):
        """下级提现列表 """
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
        url = AgentApp.fws + '/appapi/v4/finance/commission/sub-apply-list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

     def get_apply_finance_cash(self, token, user_id, tenant_id, **kwargs):
        """提现申请 """
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/finance/commission/apply-finance-cash'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

     def get_commission_sub_is_remit(self, token, user_id, tenant_id, **kwargs):
        """下级提现管理"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/finance/commission/sub-is-remit'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

     def get_commission_get_postal_info(self, token, user_id, tenant_id, **kwargs):
        """获取提现信息"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        data = {}
        data.update(kwargs)
        url = AgentApp.fws + '/appapi/v4/finance/commission/get-postal-info'
        r = requests.get(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()