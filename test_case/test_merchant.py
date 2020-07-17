import pytest

from api.baseapi import BaseApi
from api.merchant import Merchant


class TestMerchant:
    data = BaseApi.yaml_load('../yaml_data/test_merchant.yaml')

    def setup(self):
        self.merchant = Merchant()

    def tearDown(self):
        pass

    @pytest.mark.parametrize('data', data["test_get_merchant_list_1"])
    def test_get_merchant_list_1(self, data):
        """获取直属商户列表"""
        user = self.merchant.get_token(level=data['level'], isv=data['isv'])
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id, page=data['page'],
                                            page_size=data['page_size'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.merchant.get_merchant_list_data(user_id=user_id, tenant_id=tenant_id, page=data['page'],
                                                         pagesize=data['page_size'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                # assert r_list['agent_name']==conn_data['list'][i]['agent_name']
                # assert r_list['last_payed_at']==conn_data['list'][i]['last_payed_at']
                i = i + 1

    @pytest.mark.parametrize('data', data["test_get_merchant_list_2"])
    def test_get_merchant_list_2(self, data):
        """获取直属商户列表--搜索商户名称"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id, page=data['page'],
                                            page_size=data['page_size'], full_name=data['full_name'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.merchant.get_merchant_list_data_by_fullname(user_id, data['page'], tenant_id,
                                                                     data['full_name'], data['page_size'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                # assert r_list['agent_name']==conn_data['list'][i]['agent_name']
                # assert r_list['last_payed_at']==conn_data['list'][i]['last_payed_at']
                i = i + 1

    @pytest.mark.parametrize('data', data["test_get_merchant_list_3"])
    def test_get_merchant_list_3(self, data):
        """01贴牌商获取直属商户列表---翻页"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id, page=data['page'],
                                            page_size=data['page_size'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.merchant.get_merchant_list_data(user_id, tenant_id, data['page'], data['page_size'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                # assert r_list['agent_name']==conn_data['list'][i]['agent_name']
                # assert r_list['last_payed_at']==conn_data['list'][i]['last_payed_at']
                i = i + 1

    @pytest.mark.parametrize('data', data["test_get_sub_merchant_list_1"])
    def test_get_sub_merchant_list_1(self, data):
        """获取下属代理商列表"""
        user = self.merchant.get_token(level=data['level'], isv=data['isv'])
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_sub_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id, page=data['page'],
                                                page_size=data['page_size'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.merchant.get_sub_merchant_list_data(user_id, tenant_id, data['page'], data['page_size'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                assert r_list['agent_name'] == conn_data['list'][i]['agent_name']
                # assert r_list['last_payed_at']==conn_data['list'][i]['last_payed_at']
                i = i + 1

    @pytest.mark.parametrize('data', data['test_get_sub_merchant_list_2'])
    def test_get_sub_merchant_list_2(self, data):
        """获取下属商户列表--搜索商户名称"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']

        r = self.merchant.get_sub_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id,
                                                full_name=data['full_name'], page=data['page'],
                                                page_size=data['page_size'])
        assert r['code'] == data['code']
        # 遍历断言data中的内容
        conn_data = self.merchant.get_sub_merchant_list_data_by_fullname(user_id, tenant_id, data['page'],
                                                                         data['page_size'], data['full_name'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                assert r_list['agent_name'] == conn_data['list'][i]['agent_name']
                # assert r_list['last_payed_at']==conn_data['list'][i]['last_payed_at']
                i = i + 1

    @pytest.mark.parametrize('data',data['test_get_loss_merchant_list_1'])
    def test_get_loss_merchant_list_1(self,data):
        """获取流失商户列表"""
        user = self.merchant.get_token(level=data['user']['level'],isv=data['user']['isv'])
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_loss_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id,**data['data'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.merchant.get_loss_merchant_list_data(user_id, tenant_id, data['data']['page'],data['data']['page_size'])

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                assert r_list['agent_name'] == conn_data['list'][i]['agent_name']
                # assert r_list['leader_name'] == conn_data['list'][i]['leader_name']
                assert r_list['last_payed_at'] == str(conn_data['list'][i]['last_payed_at'])
                assert r_list['is_directly'] == conn_data['list'][i]['is_directly']
                i = i + 1


    @pytest.mark.parametrize('data',data['test_get_loss_merchant_list_2'])
    def test_get_loss_merchant_list_2(self, data):
        """获取流失商户列表---搜索商户名称"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_loss_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id, **data['data'])
        assert r['code'] == data['code']

        # 遍历断言data中的内容
        conn_data = self.merchant.get_loss_merchant_list_data(user_id, tenant_id, data['data']['page'],
                                                              data['data']['page_size'],full_name=data['data']['full_name'])
        assert r['data']['total_records'] == conn_data['total_records']
        assert r['data']['pages'] == conn_data['pages']
        assert r['data']['page'] == conn_data['page']

        if len(conn_data['list']) > 0:
            i = 0
            for r_list in r['data']['list']:
                print('正在比对第%s组数据，商户编号为%s' % (i + 1, r_list['merchant_num']))
                assert r_list['merchant_num'] == conn_data['list'][i]['merchant_num']
                assert r_list['full_name'] == conn_data['list'][i]['full_name']
                assert r_list['contact_phone'] == conn_data['list'][i]['contact_phone']
                assert r_list['create_at'] == str(conn_data['list'][i]['create_at'])
                assert r_list['update_at'] == str(conn_data['list'][i]['update_at'])
                assert r_list['store_total'] == conn_data['list'][i]['store_total']
                assert r_list['staff_total'] == conn_data['list'][i]['staff_total']
                assert r_list['channels'] == conn_data['list'][i]['channels']
                assert r_list['agent_name'] == conn_data['list'][i]['agent_name']
                # assert r_list['leader_name'] == conn_data['list'][i]['leader_name']
                assert r_list['last_payed_at'] == str(conn_data['list'][i]['last_payed_at'])
                assert r_list['is_directly'] == conn_data['list'][i]['is_directly']
                i = i + 1

    @pytest.mark.parametrize('data',data['test_get_idcard_type_1'])
    def test_get_idcard_type_1(self,data):
        """获取商户证件类型"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.get_idcard_type(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == data['code']
        assert r['data'] == data['assert_data']

    @pytest.mark.parametrize('data', data['test_get_merchant_info_1'])
    def test_get_merchant_info_1(self,data):
        """获取商户信息"""
        user = self.merchant.get_token(level=data['user']['level'],isv=data['user']['isv'])
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取直属商户列表的第1的商户编号"""
        merchant_num_list = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id)['data']['list']
        if merchant_num_list != []:
            merchant_num=merchant_num_list[0]['merchant_num']
            r = self.merchant.get_merchant_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                                merchant_num=merchant_num)
            conn_r_data=self.merchant.get_merchant_info_data(merchant_num,user_id,tenant_id)

            assert r['code'] == data['code']
            assert r['data']==conn_r_data

    @pytest.mark.parametrize('data', data["test_get_create_merchant_1"])
    def test_create_merchant_1(self, data):
        """创建商户"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.merchant.create(token=token, user_id=user_id, tenant_id=tenant_id, **data['data'])
        assert r['code'] == '000000'

        merchant_num=r['data']['merchant_num']
        merchant_info=self.merchant.get_merchant_info_data(merchant_num,user_id,tenant_id)
        for key in data['data'].keys():
            assert merchant_info[key]==r['data'][key]

    @pytest.mark.parametrize('data', data["test_create_merchant_2"])
    def test_create_merchant_2(self, data):
        """创建商户---完整添加2个商户"""
        user = self.merchant.get_token(level=3, isv=1)
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']

        for i in range(2):
            r = self.merchant.create(token=token, user_id=user_id, tenant_id=tenant_id, **data['base_info'])
            merchant_num = r['data']['merchant_num']
            merchant_info = self.merchant.get_merchant_info_data(merchant_num, user_id, tenant_id)
            for key in data['base_info'].keys():
                assert merchant_info[key] == r['data'][key]
            r = self.merchant.edit_merchant_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                                 merchant_num=merchant_num, **data['merchant_info'])
            r = self.merchant.edit_leader_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                               merchant_num=merchant_num, **data['leader_info'])
            r = self.merchant.edit_bank_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                             merchant_num=merchant_num, **data['bank_info'])

    @pytest.mark.parametrize('data', data["test_edit_base_info"])
    def test_edit_base_info(self, data):
        """编辑商户基础资料"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取直属商户列表的第1的商户编号"""
        merchant_num_list = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id)['data'][
            'list']
        if merchant_num_list != []:
            merchant_num = merchant_num_list[0]['merchant_num']
            r = self.merchant.edit_base_info(token=token, user_id=user_id, tenant_id=tenant_id,merchant_num=merchant_num,**data['data'])
            assert r['code'] == data['code']

            merchant_info=self.merchant.get_merchant_info_data(merchant_num,user_id,tenant_id)
            for key in data['data'].keys():
                assert merchant_info[key]==data['data'][key]


    @pytest.mark.parametrize('data', data['test_edit_merchant_info'])
    def test_edit_merchant_info(self, data):
        """01贴牌商编辑商户基本资料"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取直属商户列表的第1的商户编号"""
        merchant_num_list = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id)['data'][
            'list']
        if merchant_num_list != []:
            merchant_num = merchant_num_list[0]['merchant_num']
            r = self.merchant.edit_merchant_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                                 merchant_num=merchant_num, **data['data'])
            assert r['code'] == data['code']

            merchant_info=self.merchant.get_merchant_info_data(merchant_num,user_id,tenant_id)
            for key in data['assert_data'].keys():
                assert merchant_info[key] == data['assert_data'][key]


    @pytest.mark.parametrize('data', data['test_edit_leader_info'])
    def test_edit_leader_info(self, data):
        """编辑商户的法人信息"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取直属商户列表的第1的商户编号"""
        merchant_num_list = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id)['data'][
            'list']
        if merchant_num_list != []:
            merchant_num = merchant_num_list[0]['merchant_num']
            r = self.merchant.edit_leader_info(token=token, user_id=user_id, tenant_id=tenant_id,
                                               merchant_num=merchant_num, **data['data'])
            assert r['code'] == data['code']
            merchant_info = self.merchant.get_merchant_info_data(merchant_num, user_id, tenant_id)
            for key in data['assert_data'].keys():
                assert merchant_info[key] == data['assert_data'][key]

    @pytest.mark.parametrize('data', data['test_edit_bank_info'])
    def test_edit_bank_info(self, data):
        """编辑账户信息"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        """获取直属商户列表的第1的商户编号"""
        merchant_num_list = self.merchant.get_merchant_list(token=token, user_id=user_id, tenant_id=tenant_id)['data'][
            'list']
        if merchant_num_list != []:
            merchant_num = merchant_num_list[0]['merchant_num']
            r = self.merchant.edit_bank_info(token=token, user_id=user_id, tenant_id=tenant_id,merchant_num=merchant_num,**data['data'])
            assert r['code'] == data['code']
            merchant_info=self.merchant.get_merchant_info_data(merchant_num,user_id,tenant_id)
            for key in data['assert_data'].keys():
                assert merchant_info[key]==data['assert_data'][key]

    @pytest.mark.parametrize('data',data['test_is_enable_register'])
    def test_is_enable_register(self,data):
        """手机号是否可以注册"""
        user = self.merchant.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']

        test_user=self.merchant.get_mobile(type=data['type'])
        mobile=test_user['mobile']
        r=self.merchant.is_enable_register(token,user_id,tenant_id,mobile)
        assert r['code']==data['assert_result']['code']

        if 'message' in data['assert_result'].keys():
            assert r['message'] == data['assert_result']['message']

        if 'assert_data' in data.keys():
            assert r['data'][data['assert_data'][0]]==test_user['user_num']
