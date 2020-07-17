import pytest
import yaml

from api.agentapp import AgentApp
from api.baseapi import BaseApi

from api.channel import Channel
from api.merchant import Merchant


class TestChannel:
    data = BaseApi.yaml_load('../yaml_data/test_channel.yaml')

    def setup(self):
        self.channel = Channel()
        self.merchant = Merchant()

    def tearDown(self):
        pass

    @pytest.mark.parametrize('data', data['test_channel_mcht_fields_info'])
    def test_channel_mcht_fields_info(self, data):
        """商户进件字段定义"""
        user = self.channel.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']

        test_merchant_num=self.merchant.get_merchant_list(token,user_id,tenant_id)['data']['list'][0]['merchant_num']
        test_channel_id=self.channel.get_availabl_channel(token,user_id,tenant_id,merchant_num=test_merchant_num)['data'][0]['channel_id']
        r = self.channel.channel_mcht_fields_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                                  channel_id=test_channel_id, merchant_num=test_merchant_num)
        conn_data=self.channel.get_channel_mcht_fields_info_data(test_merchant_num,test_channel_id)

        assert r['code'] == data['code']
        print(conn_data)

    def test_demo(self):
        user = self.channel.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']

        test_merchant_num = self.merchant.get_merchant_list(token, user_id, tenant_id)['data']['list'][0][
            'merchant_num']
        test_channel_id = \
        self.channel.get_availabl_channel(token, user_id, tenant_id, merchant_num=test_merchant_num)['data'][0][
            'channel_id']
        conn_data = self.channel.get_channel_mcht_fields_info_data(test_channel_id)
        conn_payment=self.channel.get_channel_mcht_payment(test_channel_id)
        print(conn_data)
        print(conn_payment)


    @pytest.mark.parametrize('data', data['test_get_channel_area'])
    def test_get_channel_area(self, data):
        """通道地区获取"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_area(token=token, user_id=user_id, tenant_id=tenant_id,
                                          channel_id=data['channel_id'], area_name=data['area_name'])

        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_get_channel_mcc'])
    def test_get_channel_mcc(self, data):
        """#获取通道MCC码"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_mcc(token=token, user_id=user_id, tenant_id=tenant_id,
                                         channel_id=data['channel_id'])
        assert r['code'] == '000000'

    def test_get_channel_bank_no(self):
        """获取银行支行"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_bank_no(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    def test_get_chaanel_bank_name(self):
        """获取银行信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_chaanel_bank_name(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_get_channel_contract'])
    def test_get_channel_contract(self, data):
        """合利宝签章合同"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_contract(token=token, user_id=user_id, tenant_id=tenant_id, **data['data'])
        print(r)
        assert r['code'] == '000000'

    def test_get_channel_status_statistics(self):
        """通道审计统计"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_status_statistics(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_get_merchant_open_channel'])
    def test_get_merchant_open_channel(self, data):
        """获取商户已开通通道信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_merchant_open_channel(token=token, user_id=user_id, tenant_id=tenant_id,
                                                   merchant_num=data['merchant_num'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_channel_audit_list'])
    def test_get_channel_audit_list(self, data):
        """通道审核进度列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_audit_list(token=token, user_id=user_id, tenant_id=tenant_id,
                                                status=data['status'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_get_merchant_open_channel'])
    def test_get_pay_type_list(self, data):
        """获取支付方式列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_pay_type_list(token=token, user_id=user_id, tenant_id=tenant_id,
                                           merchant_num=data['merchant_num'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_get_channel_rates'])
    def test_get_channel_rates(self, data):
        """获取通道启用配置信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_channel_rates(token=token, user_id=user_id, tenant_id=tenant_id,
                                           merchant_num=data['merchant_num'], type=data['type'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_update_payment_modes_and_rates'])
    def test_update_payment_modes_and_rates(self, data):
        """通道启用配置信息修改"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_update_payment_modes_and_rates(token=token, user_id=user_id, tenant_id=tenant_id,
                                                            pay_type=data['pay_type'],
                                                            is_checkout=data['is_checkout'],
                                                            merchant_id=data['merchant_id'],
                                                            channel_id=data['channel_id'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_get_merchant_open_channel'])
    def test_get_availabl_channel(self, data):
        """获取商户可用通道列表【未入住通道列表】"""
        user = self.channel.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.channel.get_availabl_channel(token=token, user_id=user_id, tenant_id=tenant_id,
                                              merchant_num=data['merchant_num'])
        assert r['code'] == '000000'
