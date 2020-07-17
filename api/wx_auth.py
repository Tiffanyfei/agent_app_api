import requests

from api.agentapp import AgentApp


class Wx_auth(AgentApp):

    def get_wx_auth_get_apply_data(self, token, user_id, tenant_id, **kwargs):
        """认证状态"""
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
        url = AgentApp.fws + '/appapi/v4/channel/wx-auth/get-apply-data'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()