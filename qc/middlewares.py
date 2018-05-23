# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from qc.settings import USER_AGENTS as ua_list
import random
import redis
import hashlib
from scrapy.exceptions import IgnoreRequest

class UserAgentMiddleware(object):
    """
    给每个请求随机选取user_Agent
    """
    def process_request(self,request, spider):
        user_agent = random.choice(ua_list)
        request.headers['USER_AGENTS'] = user_agent
        # request.meta['proxy']  设置代理
        print('request: ', request.headers['USER_AGENTS'] )
        print('*'*30)


class QcRedisMiddleware(object):
    """
    把每个url放到redis set中
    """
    def __init__(self):
        self.sr = redis.StrictRedis(host='127.0.0.1',port=6379,db=1)

    def process_request(self, request, spider):
        if request.url.startswith("https://job.51job.com"):

            # md5详情页链接
            md5 = hashlib.md5()
            md5.update(request.url.encode())
            res = self.sr.sadd("qu_url",md5.hexdigest())
            if not res:
                raise IgnoreRequest  # 忽略失败的请求

