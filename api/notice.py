import requests

from api.agentapp import AgentApp


class Notice(AgentApp):

    def get_notice_agent_count(self, token, user_id, tenant_id, **kwargs):
        """代理商通知数量"""
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
        url = AgentApp.fws + '/appapi/v4/notify/notify/notice-agent-count'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_notice_list(self, token, user_id, tenant_id, **kwargs):
        """代理商通知列表"""
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
        url = AgentApp.fws + '/appapi/v4/notify/notify/get-notice-list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_update_agent_notice(self, token, user_id, tenant_id, **kwargs):
        """代理商通知状态更改 """
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
        params.update(**kwargs)
        url = AgentApp.fws + '/appapi/v4/notify/notify/update-agent-notice'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_create_notice(self, token, user_id, tenant_id, **kwargs):
        """代理商通知状态更改 """
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
        params.update(**kwargs)
        url = AgentApp.fws + '/appapi/v4/notify/notify/create-notice'
        r = requests.post(url=url, json=params, headers=headers)
        self.format(r)
        return r.json()