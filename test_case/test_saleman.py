import pytest

import  yaml
from api.agentapp import AgentApp
from api.baseapi import BaseApi

from api.saleman import Saleman

class TestSaleman:

    data = BaseApi.yaml_load('../yaml_data/test_saleman.yaml')

    def setup(self):
        self.agentapp = AgentApp()
        self.saleman = Saleman()

    def tearDown(self):
        pass

    def test_get_saleman_list(self):
        """01贴牌商业务员列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_list(token=token,user_id=user_id,tenant_id=tenant_id)
        # assert ['code'] == '000000'

        conn_data = self.saleman.get_saleman_list_data()
        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在对比第%s组数据，业务员编号为s%' % (i+1, r_list['saleman_num']))
                assert r_list['name'] == conn_data['list'][i]['name']
                assert r_list['saleman_num'] == conn_data['list'][i]['saleman_num']
                assert r_list['phone'] == conn_data['list'][i]['phone']
                assert r_list['create_at'] == conn_data['list'][i]['create_at']
                i = i + 1

    @pytest.mark.parametrize('data',data['test_get_saleman_info'])
    def test_get_saleman_info(self, data):
        """业务员信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_info(token=token, user_id=user_id, tenant_id=tenant_id, sale_num=data['sale_num'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data',data['test_saleman_insert_sale'])
    def test_get_saleman_info(self, data):
        """添加业务员"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.saleman_insert_sale(token=token, user_id=user_id, tenant_id=tenant_id, pwd=data['pwd'], phone=data['phone'],
                                             remark=data['remark'],contact_phone=data['contact_phone'],name=data['name'])
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data',data['test_saleman_update_sale'])
    def test_saleman_update_sale(self, data):
        """修改业务员"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.saleman_update_sale(token=token, user_id=user_id, tenant_id=tenant_id, pwd=data['pwd'],saleman_num=data['saleman_num'],
                                             remark=data['remark'],contact_phone=data['contact_phone'],name=data['name'])
        assert r['code'] == '000000'



    def test_saleman_channel_rates_config(self):
        """获取展业规则费率结构"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.saleman_channel_rates_config(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'


    def test_saleman__business_flow_list(self):
        """获取业务员数据列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.saleman_business_flow_list(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'


    """
    务员APP相关接口
    
    """

    @pytest.mark.parametrize('data', data['test_saleman_records'])
    def test_saleman__business_flow_list(self, data):
        """获取业务员数据列表"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_records(token=token, user_id=user_id, tenant_id=tenant_id, month=data['month'], day=data['day'], start=data['start'],
                                                    stop=data['stop'], page=data['page'], page_size=data['page_size'])
        assert r['code'] == '000000'


    def test_saleman_update_password(self):
        """修改密码发送验证码"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_send_register_code(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_saleman_update_password'])
    def test_get_saleman_update_password(self, data):
        """修改密码"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_update_password(token=token, user_id=user_id, tenant_id=tenant_id, password=data['password'], verification_code=data['verification_code'])
        assert r['code'] == '000000'



    @pytest.mark.parametrize('data', data['test_saleman_notice_list'])
    def test_get_saleman_notice_list(self, data):
        """业务员消息通知列表"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_notice_list(token=token, user_id=user_id, tenant_id=tenant_id, page=data['page'], page_size=data['page_size'])
        assert r['code'] == '000000'


    def test_get_saleman_update_notice_status(self):
        """更改通知状态"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        id = self.saleman.get_saleman_notice_list(token=token, user_id=user_id, tenant_id=tenant_id)['data']['list'][0]['id']
        r = self.saleman.get_saleman_update_notice_status(token=token, user_id=user_id ,tenant_id=tenant_id, id=id)
        assert r['code'] == '000000'

    def test_get_saleman_notify_num(self):
        """获取消息未读列表"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_notify_num(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'


    def test_get_saleman_get_sale_rates(self):
        """获取展业规则费率信息"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_get_sale_rates(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data',data['test_saleman_update_head_portrait'])
    def test_saleman_update_head_portrait(self, data):
        """修改头像"""
        user = self.agentapp.get_sale_token(0)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.saleman.get_saleman_update_head_portrait(token=token, user_id=user_id, tenant_id=tenant_id, url=data['url'])
        assert r['code'] == '000000'



