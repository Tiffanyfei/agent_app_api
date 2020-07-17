import requests

from api.agentapp import AgentApp
from api.common.connect_mongodb import DataBase_Mongo


class Channel(AgentApp):

    def channel_mcht_fields_info(self, token, user_id, tenant_id, **kwargs):
        """商户进件字段定义"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/channel-mcht-fields-info'
        r = requests.get(url=url, headers=headers, params=params)
        self.format(r)
        return r.json()

    def get_channel_mcht_fields_info_data(self, merchant_num,channel_id):
        """获取通道的data信息"""
        conn = self.conn_db_mongo()
        merchant_own_channel_list=conn.get_merchant_own_channel_list(merchant_num)
        if channel_id in merchant_own_channel_list:
            merchant_channel_data=conn.get_merchant_channel_data(channel_id,merchant_num)
        else:
            channel_data = conn.get_channel_mcht_fields_info(channel_id)
            channel_paymant_data=conn.get_channel_mcht_payment(channel_id)

        conn.close_conn()
        return channel_data

    def get_channel_mcht_payment(self,channel_id):
        """获取通道的payment"""
        conn=self.conn_db_mongo()
        data=conn.get_channel_mcht_payment(channel_id)
        conn.close_conn()
        return data

    def get_channel_area(self, token, user_id, tenant_id, channel_id, area_name):
        """获取通道地区"""
        headers = {
            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        params = {'channel_id': channel_id, 'area_name': area_name}
        url = AgentApp.fws + '/appapi/v4/channel/channel/area'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_channel_mcc(self, token, user_id, tenant_id, channel_id):
        """获取通道MCC码"""
        headers = {

            'tenant-id': tenant_id,
            'user-auth-token': token,
            'user-login-type': AgentApp.agent_login_type,
            'device-uuid': AgentApp.device_uuid,
            'user-id': user_id,
            'agent-app': AgentApp.agent_app,
            'Api-version': AgentApp.Api_Version,
        }
        params = {'channel_id': channel_id}
        url = AgentApp.fws + '/appapi/v4/channel/channel/mcc'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_channel_bank_no(self, token, user_id, tenant_id, **kwargs):
        """获取银行支行"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/bank-no'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_chaanel_bank_name(self, token, user_id, tenant_id, **kwargs):
        """获取银行信息"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/bank-name'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_channel_contract(self, token, user_id, tenant_id, **kwargs):
        """合利宝签章合同"""
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
        url = AgentApp.fws = '/appapi/v4/channel/channel/contract'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def get_channel_status_statistics(self, token, user_id, tenant_id, **kwargs):
        """通道审计统计"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/channel-status-statistics'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_merchant_open_channel(self, token, user_id, tenant_id, **kwargs):
        """获取商户已开通通道信息"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/get-merchant-open-channel'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_channel_audit_list(self, token, user_id, tenant_id, **kwargs):
        """通道审核进度列表 """
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/channel-audit-list'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_pay_type_list(self, token, user_id, tenant_id, **kwargs):
        """获取支付方式列表"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/get-pay-type-list'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_channel_rates(self, token, user_id, tenant_id, **kwargs):
        """获取通道启用配置信息"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/get-channel-rates'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()

    def get_update_payment_modes_and_rates(self, token, user_id, tenant_id, **kwargs):
        """通道启用配置信息修改"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/update-payment-modes-and-rates'
        r = requests.post(url=url, json=data, headers=headers)
        self.format(r)
        return r.json()

    def get_availabl_channel(self, token, user_id, tenant_id, **kwargs):
        """获取商户可用通道列表【未入住通道列表】"""
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
        url = AgentApp.fws + '/appapi/v4/channel/channel/get-available-channel'
        r = requests.get(url=url, params=params, headers=headers)
        self.format(r)
        return r.json()
