import pytest

from api.agentapp import AgentApp
from api.baseapi import BaseApi
from api.commission import Commission


class TestMerchant:
    data = BaseApi.yaml_load('../yaml_data/test_commission.yaml')


    def setup(self):
        self.agentapp = AgentApp()
        self.commission = Commission()

    def tearDown(self):
        pass


    def test_get_commission_statistical_data(self):
        """获取佣金提现统计"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.commission.get_commission_statistical_data(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_commission_apply_list'])
    def test_get_commission_apply_list(self, data):
        """本级提现列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.commission.get_commission_apply_list(token=token, user_id=user_id, tenant_id=tenant_id, page=data['page'], page_size=data['page_size'],
                                                      start_date=data['start_date'], end_date=data['end_date'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_commission_sub_apply_list'])
    def test_get_commission_sub_apply_list(self, data):
        """下级提现列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.commission.get_commission_sub_apply_list(token=token, user_id=user_id, tenant_id=tenant_id, status=data['status'],page=data['page'],
                                                          page_size=data['page_size'])
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data', data['test_apply_finance_cash'])
    def test_apply_finance_cash(self, data):
        """提现申请"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.commission.get_apply_finance_cash(token=token, user_id=user_id, tenant_id=tenant_id, money=data['money'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_commission_sub_is_remit'])
    def test_get_commission_sub_is_remit(self,data):
        """下级提现管理"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.commission.get_apply_finance_cash(token=token, user_id=user_id, tenant_id=tenant_id, action=data['action'],
                                                   cash_num=data['cash_num'], remark=data['remark'])
        assert r['code'] == '000000'


    def test_get_commission_get_postal_info(self):
        """获取提现信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.commission.get_commission_get_postal_info(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'
