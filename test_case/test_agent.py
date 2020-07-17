import pytest

from api.agentapp import AgentApp
from api.baseapi import BaseApi
from api.agent import Agent

class TestAgent:
    data = BaseApi.yaml_load('../yaml_data/test_aentyaml.yaml')

    def setup(self):

        self.agentapp = AgentApp()
        self.agent = Agent()

    def tearDown(self):
        """
        用例执行完之后的操作
        :return:
        """
        pass

    @pytest.mark.parametrize('telphone', ['13637877554'])
    def test_send_register_code(self, telphone):
        """发送短信验证码"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.agent.send_register_code(token=token, user_id=user_id, tenant_id=tenant_id, telphone=telphone)
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data["test_creat_agent_1"])
    def test_creat_agent_1(self, data):
        """创建一级代理商"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """判断手机号是否可注册"""
        r = self.agent.is_enable_register(token=token, user_id=user_id, tenant_id=tenant_id, mobile=data['telphone'])

        assert r['code'] == '000000'
        assert r['data']['user_num'] == ''

        r = self.agent.creat_agent_1(token=token, user_id=user_id, tenant_id=tenant_id, ver_code=data['ver_code'], user_name=data['user_name'],
                                     telphone=data['telphone'], agent_name=data['agent_name'], respo_name=data['respo_name'], is_sub=data['is_sub'],
                                     start_time=data['start_time'], expire_time=data['expire_time'], agent_region=data['agent_region'], is_market=data['is_market'])


        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_edit_agent_1'])
    def test_edit_agent_1(self, data):
        """编辑代理商信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.agent.edit_agent_1(token=token, user_id=user_id, tenant_id=tenant_id, telphone=data['telphone'], respo_name=data['respo_name'],
                                     is_sub=data['is_sub'], start_time=data['start_time'], expire_time=data['expire_time'],
                                     agent_region=data['agent_region'], is_market=data['is_market'], agent_num=data['agent_num'])
        assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_my_agent_list_1'])
    def test_my_agent_list_1(self, data):
        """直属代理商列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.agent.my_agent_list(token=token, user_id=user, tenant_id=tenant_id, page=data['page'], page_size=data['page_size'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.agent.get_agent_list_data(user_id, data['page'], tenant_id, data['page_size'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']
        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在对比第%S组数据，商户编号为%s' % (i + 1, r_list['agent_num']))
                assert r_list['agent_num'] == conn_data['list'][i]['agent_num']
                assert r_list['agent_name'] == conn_data['list'][i]['agent_name']
                assert r_list['telphone'] == conn_data['telphone'][i]['telphone']
                assert r_list['respo_name'] == conn_data['respo_name'][i]['respo_name']
                assert r_list['p_agent_name'] ==conn_data['p_agent_name'][i]['p_agent_name']
                assert r_list['p_num'] == conn_data['p_num'][i]['p_num']
                assert r_list['status'] == conn_data['status'][i]['status']
                assert r_list['bank_chk_status'] == conn_data['bank_chk_status'][i]['bank_chk_status']
                assert r_list['day_make_code_limit'] ==conn_data['day_make_code_limit'][i]['day_make_code_limit']
                assert r_list['start_time'] == conn_data['start_time'][i]['start_time']
                assert r_list['expire_time'] == conn_data['expire_time'][i]['expire_time']
                assert r_list['agent_region'] == conn_data['agent_region'][i]['agent_region']
                assert r_list['level'] == conn_data['level'][i]['level']
                assert r_list['is_sub'] == conn_data['is_sub'][i]['is_sub']
                assert r_list['is_market'] == conn_data['is_market'][i]['is_market']
                assert r_list['created_at'] == conn_data['created_at'][i]['created_at']
                assert r_list['merchant_count'] ==conn_data['merchant_count'][i]['merchant_count']
                i = i + 1


    @pytest.mark.parametrize('data', data['test_my_agent_list_1'])
    def test_sub_agent_list_1(self, data):
        """下属代理商列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.agent.sub_agent_list(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

        #遍历断言data中得内容
        conn_data = self.agent.get_agent_list_data(user_id, data['page'], tenant_id,data['page_size'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']



    def test_get_agent_info(self):
        """获取代理商信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取代理商列表得第*个代理商编号"""
        agent_num = self.agent.my_agent_list(token=token, user_id=user_id, tenant_id=tenant_id)['data']['list'][1]['agent_num']
        """根据查询到得代理商编号进行搜索"""
        r = self.agent.get_agent_info(token=token, user_id=user_id, tenant_id=tenant_id,agent_num=agent_num)
        assert r['code'] == '000000'


    def test_get_channel_rates_config(self):
        """获取通道费率结构"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取代理商列表得第*个代理商编号"""
        agent_num = self.agent.my_agent_list(token=token, user_id=user_id, tenant_id=tenant_id)['data']['list'][1]['agent_num']
        """根据查询到得代理商编号进行搜索"""
        r = self.agent.get_channel_rates_config(token=token, user_id=user_id, tenant_id=tenant_id, agent_num=agent_num)
        assert r['code'] == '000000'

    # @pytest.mark.parametrize('data', data['test_channel_rates_update'])
    # def test_channel_rates_update(self, data):
    #     """编辑代理商费率信息"""
    #     user = self.agentapp.get_token()
    #     token = user['token']
    #     user_id = user['user_id']
    #     tenant_id = user['tenant_id']
    #     """获取代理商列表得第*个商户编号"""
    #     agent_num = self.agent.my_agent_list(token=token, user_id=user_id, tenant_id=tenant_id)['data']['list'][1]['agent_num']
    #
    #     r = self.agent.channel_rates_update(token=token, user_id=user_id, tenant_id=tenant_id, mob_weixin_openstatus_1000005=data['mob_weixin_openstatus_1000005'],
    #                                         mob_weixin_rate_1000005=data['mob_weixin_rate_1000005'], mob_unionpay_openstatus_1000005=data['mob_unionpay_openstatus_1000005'],
    #                                         mob_unionpay_rate_1000005=data['mob_unionpay_rate_1000005'], mob_unionpay_disrate_1000005=data['mob_unionpay_disrate_1000005'],
    #                                         mob_alipay_openstatus_1000005=data['mob_alipay_openstatus_1000005'], mob_alipay_rate_1000005=data['mob_alipay_rate_1000005'],
    #                                         pos_debit_openstatus_1000005=data['pos_debit_openstatus_1000005'], pos_debit_rate_1000005=data['pos_debit_rate_1000005'],
    #                                         pos_debit_ceiling_1000005=data['pos_debit_ceiling_1000005'], pos_credit_openstatus_1000005=data['pos_credit_openstatus_1000005'],
    #                                         pos_credit_rate_1000005=data['pos_credit_rate_1000005'], pos_oversea_openstatus_1000005=data['pos_oversea_openstatus_1000005'],
    #                                         pos_oversea_rate_1000005=data['pos_oversea_rate_1000005'], quickpass_debit_openstatus_1000005=data['quickpass_debit_openstatus_1000005'],
    #                                         quickpass_debit_rate_1000005=data['quickpass_debit_rate_1000005'], quickpass_debit_disrate_1000005=data['quickpass_debit_disrate_1000005'],
    #                                         quickpass_debit_ceiling_1000005=data['quickpass_debit_ceiling_1000005'], quickpass_credit_openstatus_1000005=data['quickpass_credit_openstatus_1000005'],
    #                                         quickpass_credit_rate_1000005=data['quickpass_credit_rate_1000005'], quickpass_oversea_openstatus_1000005=data['quickpass_oversea_openstatus_1000005'],
    #                                         quickpass_oversea_rate_1000005=data['quickpass_oversea_rate_1000005'], quickpass_oversea_disrate_1000005=data['quickpass_oversea_disrate_1000005'],
    #                                         unionpay_unionpay_openstatus_1000005=data['unionpay_unionpay_openstatus_1000005'], unionpay_unionpay_rate_1000005=data['unionpay_unionpay_rate_1000005'],
    #                                         unionpay_unionpay_disrate_1000005=data['unionpay_unionpay_disrate_1000005'])
    #     assert r['code'] == '000000'

    @pytest.mark.parametrize('data', data['test_update_agent_bank_info'])
    def test_update_agent_bank_info(self, data):
        """编辑代理商信息"""
        user = self.agentapp.get_token(1, 1)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        # agent_num = self.agent.my_agent_list(token=token, user_id=user_id, tenant_id=tenant_id)['data']['list'][5]['agent_num']
        r = self.agent.update_agent_bank_info(token=token, user_id=user_id, tenant_id=tenant_id, bank_accout_name=data['bank_accout_name'], bank_account_no=data['bank_account_no'],
                                              deposit_bank_code=data['deposit_bank_code'], sub_bank_code=data['sub_bank_code'], photo=data['photo'])

        assert r['code'] == '000000'