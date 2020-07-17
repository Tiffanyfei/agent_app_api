import pytest

from api.agentapp import AgentApp
from api.baseapi import BaseApi
from api.wx_auth import Wx_auth


class TestMerchant:
    data = BaseApi.yaml_load('../yaml_data/test_wx_auth.yaml')


    def setup(self):
        self.agentapp = AgentApp()
        self.wx_auth = Wx_auth()

    def tearDown(self):
        pass

    @pytest.mark.parametrize('data', data["test_wx_auth_get_apply_data"])
    def test_get_merchant_list_1(self, data):
        """认证状态"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.wx_auth.get_wx_auth_get_apply_data(token=token, user_id=user_id, tenant_id=tenant_id, merchant_num=data['merchant_num'], channel_id=data['channel_id'])
        assert r['code'] == '000000'
