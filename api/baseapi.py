import datetime
import json
import logging
import time

import requests
import yaml
from requests import Request
from jsonpath import jsonpath


class BaseApi:
    params = {}
    data = {}

    @classmethod
    def format(cls, r):
        """打印日志，将r转为json然后按照一定格式打印"""
        cls.r = r
        print(json.dumps(json.loads(r.text), indent=2, ensure_ascii=False))

    @classmethod
    def assert_data(self, data: dict, r: json):
        """循环遍历字典进行断言"""
        keys = data.keys()
        for key1 in keys:
            if isinstance(data[key1], dict):
                for key2 in data[key1].keys():
                    if isinstance(data[key1][key2], dict):
                        for key3 in data[key2].keys():
                            assert r[key1][key2][key3] == data[key1][key2][key3]
                    else:
                        assert r[key1][key2] == data[key1][key2]
            else:
                assert r[key1] == data[key1]

    def jsonpath(self, path, r=None, **kwargs):
        if r is None:
            r = self.r.json()
        return jsonpath(r, path)

    # 封装yaml文件的加载
    @classmethod
    def yaml_load(cls, path) -> list:
        """解压yaml文件"""
        with open(file=path, encoding='utf8') as f:
            return yaml.load(f, yaml.FullLoader)

    @classmethod
    def yaml_replace(cls, req: dict, kv: dict):
        raw = yaml.dump(req)
        for key, value in kv.items():
            raw = raw.replace(f"${{{key}}}", repr(value))
        return yaml.safe_load(raw)

    def get_pages(self, lenght: int, pagesize: int):
        """换算总页数"""
        pages=0
        if lenght==0 and pagesize>0:
            pages=0
        elif lenght>0 and pagesize>0:
            if lenght % pagesize == 0:
                pages=lenght//pagesize
            else:
                pages=lenght//pagesize+1
        else:
            print('入参错误，请重新传值')
        return pages

    def get_list(self,tup:tuple):
        """元祖转为数组,去重"""
        list=[]
        for l in tup:
            if l not in list:
                list.append(l)
        return list

    def dict_fetchall(self,cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_list_by_page(self,list,pagesize,page):
        """分页"""
        lenght=len(list)
        pages=self.get_pages(lenght,pagesize)

        result_list=[]
        if lenght == 0:
            return result_list
        elif pages == 1:
            result_list = list
        elif pages > 1 and page < pages:
            result_list = list[20 * (page - 1):20 * page]
        elif pages > 1 and page == pages:
            result_list = list[20 * (page - 1):lenght]
        else:
            print('入参错误，请仔细检查入参')
        return result_list

    def api_load(self, path):
        return self.yaml_load(path)

    def api_send(self, req: dict):

        req['params']['access_token'] = self.get_token(self.secret)
        print(req)

        # 模板内容替换
        # todo: 使用format
        raw = yaml.dump(req)
        for key, value in self.params.items():
            print(key, value)
            raw = raw.replace(f"${{{key}}}", repr(value))
            print("replace")
        req = yaml.safe_load(raw)

        print(req)

        r = requests.request(
            req['method'],
            url=req['url'],
            params=req['params'],
            json=req['json']
        )
        self.format(r)
        return r.json()

    # todo: 封装类似HttpRunner这样的数据驱动框架
    def steps(self, path):
        with open(path) as f:
            steps: list[dict] = yaml.safe_load(f)
            request: Request = None
            for step in steps:
                logging.info(step)
                if "by" in step.keys():
                    element = self.find(step["by"], step["locator"])
                if "action" in step.keys():
                    action = step["action"]
                    if action == "find":
                        pass
                    elif action == "click":
                        element.click()
                    elif action == "text":
                        element.text
                    elif action == "attribute":
                        element.get_attribute(step["value"])
                    elif action in ["send", "input"]:
                        content: str = step["value"]
                        for key in self._params.keys():
                            content = content.replace("{%s}" % key, self._params[key])
                        element.send_keys(content)

    def get_time_stamp(self, t):
        """标准格式转时间戳"""
        time_stamp = int(time.mktime(t.timetuple()))
        return time_stamp

    def get_time_to_stamp(self, dt):
        """'%Y-%m-%d %H:%M:%S'格式转时间戳"""
        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = int(time.mktime(timeArray))
        return timestamp

    def get_day_start(self, t):
        """获取凌晨时间戳"""
        day = datetime.datetime.fromtimestamp(t)
        day_start = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        day_start = self.get_time_stamp(day_start)
        return day_start

    def get_day_end(self, t):
        day_end = self.get_day_start(t) + 86399
        return day_end

    def get_now(self):
        """获取当前时间戳"""
        now = int(time.time())
        return now

    def get_today_start(self):
        """获取今天凌晨时间戳"""
        now = self.get_now()
        today_start = self.get_day_start(now)
        return today_start

    def get_today_end(self):
        """获取今天最后的时间戳"""
        now = self.get_now()
        today_end = self.get_day_end(now)
        return today_end

    def get_yesterday_start(self):
        """获取昨天凌晨时间戳"""
        yesterday_start = self.get_today_start() - 86400
        return yesterday_start

    def get_yesterday_end(self):
        """获取昨天最后一秒"""
        yesterday_end = self.get_today_start() - 1
        return yesterday_end

    def get_this_month_start(self):
        """获取本月第一天凌晨时间戳"""
        today = datetime.datetime.now()
        this_month_start_day = today.replace(day=1)
        this_month_start_day_m = self.get_time_stamp(this_month_start_day)
        this_month_start = self.get_day_start(this_month_start_day_m)
        return this_month_start

    def get_this_month_end(self):
        """获取本月最后一秒时间戳"""
        today = datetime.datetime.now()
        if today.month == 12:
            today_next_month = datetime.datetime(today.year + 1, 1, 1)
            today_next_month_m = self.get_time_stamp(today_next_month)
        else:
            today_next_month = datetime.datetime(today.year, today.month + 1, 1)
            today_next_month_m = self.get_time_stamp(today_next_month)
        this_month_end = today_next_month_m - 1
        return this_month_end

    def get_lastmonth_start(self):
        """获取上月第一天凌晨时间戳"""
        today = datetime.datetime.now()
        today_last_month = datetime.datetime(today.year, today.month - 1, 1)
        lastmonth_start = self.get_time_stamp(today_last_month)
        return lastmonth_start

    def get_lastmonth_end(self):
        """获取上月最后一秒时间戳"""
        lastmonth_end = self.get_this_month_start() - 1
        return lastmonth_end

    def get_time(self, time_stamp):
        """时间戳转换为标准格式"""
        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
        return time1
