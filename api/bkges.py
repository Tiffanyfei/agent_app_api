import requests

from api.agentapp import AgentApp

class Bkges(AgentApp):

    def get_bkge_indexs(self, token, user_id, tenant_id, **kwargs):
        """佣金统计页面"""
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
        url = AgentApp.fws + '/appapi/v4/bkges/bkges/bkge-indexs'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_channel_bkge_list(self, token, user_id, tenant_id, **kwargs):
        """通道佣金列表创 """
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
        url = AgentApp.fws + '/appapi/v4/bkges/bkges/channel-bkge-list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()