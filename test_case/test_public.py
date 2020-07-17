import pytest

from api.agentapp import AgentApp
from api.baseapi import BaseApi
from api.public import Public


class TestMerchant:
    data = BaseApi.yaml_load('../yaml_data/test_Public.yaml')


    def setup(self):
        self.agentapp = AgentApp()
        self.public = Public()

    def tearDown(self):
        pass

    def test_get_auth_generate_sign(self):
        """签名验证接口"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.public.get_auth_generate_sign(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'

    def test_get_my_nauth_check(self):
        """商城权限"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.public.get_my_nauth_check(token=token, user_id=user_id, tenant_id=tenant_id)
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data', data['test_public_upload'])
    def test_get_my_public_upload(self, data):
        """上传图片"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.public.get_my_public_upload(token=token, user_id=user_id, tenant_id=tenant_id, file=data['image_file'])
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data',data['test_region_regions'])
    def test_get_region_regions(self, data):
        """获取地区"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.public.get_region_regions(token=token, user_id=user_id, tenant_id=tenant_id, version=data['version'])
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data',data['test_region_regions'])
    def test_region_list(self, data):
        """获取下级地区列表"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        p_code = self.public.get_region_regions(token=token, user_id=user_id, tenant_id=tenant_id, version=data['version'])['data']['regions'][0]['p_code']
        r = self.public.get_region_list(token=token, user_id=user_id, tenant_id=tenant_id, p_code=p_code)
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data',data['test_region_regions'])
    def test_get_region_info(self, data):
        """获取当前CODE区域信息"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        code = self.public.get_region_regions(token=token, user_id=user_id, tenant_id=tenant_id, version=data['version'])['data']['regions'][0]['code']

        r = self.public.get_region_info(token=token, user_id=user_id, tenant_id=tenant_id, code=code)
        assert r['code'] == '000000'


    @pytest.mark.parametrize('data',data['test_retrieve_send_code'])
    def test_get_region_info(self, data):
        """发送验证码(修改密码)"""
        user = self.agentapp.get_token()
        token = user['token']
        user_id = user['user_id']
        tenant_id = user['tenant_id']
        r = self.public.get_retrieve_send_code(token=token, user_id=user_id, tenant_id=tenant_id, mobile=data['mobile'], login_type=data['login_type'])
        assert r['code'] == '000000'


