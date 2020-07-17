import os

import requests

from api.agentapp import AgentApp


class Public(AgentApp):

    def get_auth_generate_sign(self, token, user_id, tenant_id, **kwargs):
        """签名验证接口"""
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
        url = AgentApp.fws + '/appapi/v4/common/auth/generate-sign'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_my_nauth_check(self, token, user_id, tenant_id, **kwargs):
        """商城权限"""
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
        url = AgentApp.fws + '/appapi/v4/my/nauth/check'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_my_public_upload(self, token, user_id, tenant_id, file):
        """上传图片"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        files={
            'image_file':(os.path.basename(file),open(file, 'rb'),'image/png'),

        }
        print(files)
        url = AgentApp.fws + '/appapi/v4/common/public/upload'
        r = requests.post(url=url, headers=headers, files=files)
        self.format(r)
        return r.json()



    def get_region_regions(self, token, user_id, tenant_id, **kwargs):
        """获取地区"""
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
        url = AgentApp.fws + '/appapi/v4/common/region/regions'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()



    def get_region_list(self, token, user_id, tenant_id, **kwargs):
        """获取下级地区列表"""
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
        url = AgentApp.fws + '/appapi/v4/common/region/list'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_region_info(self, token, user_id, tenant_id, **kwargs):
        """获取当前CODE区域信息"""
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
        url = AgentApp.fws + '/appapi/v4/common/region/info'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()


    def get_retrieve_send_code(self, token, user_id, tenant_id,**kwargs):
        """发送验证码(修改密码)"""
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
        url = AgentApp.fws + '/appapi/v4/common/retrieve/send-code'
        r = requests.get(url=url, json=data,headers=headers)
        self.format(r)
        return r.json()
