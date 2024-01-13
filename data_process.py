# coding:utf-8

import time
import requests

from config import r


# 获取站点和页面 PV
def get_pv(host, path):
    # 增加指定键的值，增加后的数值
    page_pv = r.incr("page_pv:%s:%s" % (host, path))
    # page_pv 不设置过期
    # r.expire("page_pv:%s:%s" % (host, path), 60 * 60 * 24 * 30)
    site_pv = r.incr("site_pv:%s" % host)
    # 设置 site_pv 过期时间 30 天
    r.expire("site_pv:%s" % host, 60 * 60 * 24 * 30)
    return page_pv, site_pv


# 统计进站 IP 并返回独立 IP 数，即 UV
def record_and_count_visitors(site_name, ip):
    # 添加当前 IP
    r.sadd("site_uv:%s" % site_name, ip)
    # 获取站点下所有独立 IP 数
    site_uv = r.scard("site_uv:%s" % site_name)
    # 设置过期时间为 30 天
    r.expire("site_uv:%s" % site_name, 60 * 60 * 24 * 30)
    r.expire("live_site:%s" % site_name, 60 * 60 * 24 * 30)
    # 返回独立 IP 数
    return site_uv


# 从不蒜子拉取原始数据
def fetch_past_data(host):
    # 设置不蒜子接口URL
    url = "https://busuanzi.ibruce.info/busuanzi?jsonpCallback=BusuanziCallback_777487655111"
    # 定义请求参数和请求头
    payload = {}
    headers = {
        'Referer': "https://" + host + "/",
        'Cookie': 'busuanziId=89D15D1F66D2494F91FB315545BF9C2A'
    }
    # 初始化响应对象
    response = None
    # 初始化重试次数计数器
    TIMES = 0

    # 循环直到获取到有效响应为止
    while not response:
        # 发起GET请求
        response = requests.request("GET", url, headers=headers, data=payload)
        print("首次连接，正在从不蒜子官网拉取数据")
        # 若30次重试后仍未获取到有效响应，则模拟响应数据，以避免无限循环
        if TIMES > 30:
            response = 'try{BusuanziCallback_777487655111({"site_uv":0,"page_pv":0,"version":2.4,"site_pv":0});}catch(e){}'
        # 这里有点没搞懂为啥要停，怕太快卡住？
        time.sleep(1)
        # 增加重试次数计数器
        TIMES += 1

    # 从响应文本中提取数据并转换为字典
    str_2_dict = eval(response.text[34:][:-13])
    site_uv = str_2_dict["site_uv"]
    page_pv = str_2_dict["page_pv"]
    site_pv = str_2_dict["site_pv"]

    # 将数据写入 Redis 并设置 30 天过期时间
    r.set("live_site:%s" % host, site_uv, ex=60 * 60 * 24 * 30)
    # page_pv 不设置过期
    # r.set("page_pv:%s:/" % host, page_pv, ex=60 * 60 * 24 * 30)
    r.set("page_pv:%s:/" % host, page_pv)
    r.set("site_pv:%s" % host, site_pv, ex=60 * 60 * 24 * 30)

    # 打印网站数据统计
    print("网址:%s" % host)
    print("全站访问人数:%s" % site_uv)
    print("首页访问量:%s" % page_pv)
    print("全站访问量:%s" % site_pv)

    # 返回全站访问人数
    return site_uv
