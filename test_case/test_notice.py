import pytest

from api.agentapp import AgentApp
from api.baseapi import BaseApi
from api.notice import Notice


class TestMerchant:
    data = BaseApi.yaml_load('../yaml_data/test_notice.yaml')


    def setup(self):
        self.agentapp = AgentApp()
        self.notice = Notice()

    def tearDown(self):
        pass

    def test_get_notice_agent_count(self):
        """代理商通知数量"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.notice.get_notice_agent_count(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code']== '000000'

    def test_get_notice_agent_count(self):
        """代理商通知列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.notice.get_notice_list(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code']== '000000'

    @pytest.mark.parametrize('data', data['test_update_agent_notice'])
    def test_get_update_agent_notice(self, data):
        """代理商通知列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        # id = self.notice.get_notice_list(token=token, user_id=user_id, tenant_id=tenant_id)['data'][1]['id']
        # print(notice_id)
        r = self.notice.get_update_agent_notice(token=token, user_id=user_id, tenant_id=tenant_id, notice_id=data['notice_id'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_create_notice'])
    def test_create_notice(self, data):
        """代理商通知列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.notice.get_create_notice(token=token, user_id=user_id, tenant_id=tenant_id, title=data['title'], content=data['content'],
                                          posted=data['posted'], author=data['author'])
        assert r['code'] == '000000'