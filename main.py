# coding:utf-8

import json
import uvicorn

from urllib.parse import urlparse
from fastapi import FastAPI, Request, Header, Response
from fastapi.responses import RedirectResponse

from config import r, server_port, website
from data_process import get_pv, record_and_count_visitors, fetch_past_data

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/")
def root(request: Request,
         referer: str = Header(None),
         jsonpCallback: str = ""
         ):
    # 若请求中未包含 referer 头，则重定向至指定网址
    if not referer:
        # 更改为跳转至指定网址
        return RedirectResponse(url=website)
    # 获取客户端主机地址和 referer 的主机地址及路径
    client_host = request.client.host
    url_res = urlparse(referer)
    host = url_res.netloc
    path = url_res.path
    # 如果 referer 的路径中包含"index"，则截取
    if "index" in path:
        path = path.split("index")[0]
    # 从 Redis 中获取过去保存的网站 UV 数据，若不存在则调用 fetch_past_data 方法获取
    past_site_uv = r.get("live_site:%s" % host)
    if not past_site_uv:
        past_site_uv = fetch_past_data(host)
    else:
        past_site_uv = int(past_site_uv.decode())
    # 增加当前 UV 值并调用 record_and_count_visitors 方法统计数据
    uv = record_and_count_visitors(host, client_host) + past_site_uv
    # 调用 get_pv 方法获取页面 PV 和站点 PV
    page_pv, site_pv = get_pv(host, path)
    # 构造返回的数据
    dict_data = {
        "site_uv": uv,
        "page_pv": page_pv,
        "site_pv": site_pv,
        "version": 2.4
    }
    # 构造 JSONP 格式的字符串数据
    data_str = "try{" + jsonpCallback + "(" + json.dumps(dict_data) + ");}catch(e){}"
    print(data_str)
    # 返回响应结果
    return Response(content=data_str, media_type="application/javascript")


if __name__ == "__main__":
    """
        更改调用系统的或Docker的Redis命令
        print("chmod redis")
        subprocess.run(chmod_redis, shell=True)
        print("start redis")
        subprocess.Popen(start_redis, shell=True)
    """
    print("The Redis service is changed to use system or Docker commands.")
    print("start uvicorn")
    uvicorn.run("main:app", host="0.0.0.0", port=server_port, log_level="info", proxy_headers=True, forwarded_allow_ips="*")
