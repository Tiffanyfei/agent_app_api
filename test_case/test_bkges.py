import  pytest

from api.agentapp import AgentApp

from api.baseapi import BaseApi
from api.bkges import Bkges

class  TestBkges:
    data = BaseApi.yaml_load('../yaml_data/test_bkges.yaml')

    def setup(self):
        self.agentapp = AgentApp()
        self.bkges = Bkges()

    def tearDown(self):
        pass

    @pytest.mark.parametrize('data', data['test_bkge_indexs'])
    def test_get_bkge_indexs(self, data):
        """佣金统计页面"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.bkges.get_bkge_indexs(token=token, user_id=user_id, tenant_id=tenant_id, start_time=data['start_time'], stop_time=data['stop_time'],
                                       page=data['page'], page_size=data['page_size'], day=data['day'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_channel_bkge_list'])
    def test_get_bkge_indexs(self, data):
        """通道佣金列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.bkges.get_channel_bkge_list(token=token, user_id=user_id, tenant_id=tenant_id, start_time=data['start_time'], stop_time=data['stop_time'],
                                       page=data['page'], page_size=data['page_size'], day=data['day'])
        assert r['code'] == '000000'

