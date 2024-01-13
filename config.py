# coding:utf-8

import redis

# 在原版 @zkeq 的源码中
# 无 referer 直接访问后端的网址是输出文字 "Powered by: FastAPI + Redis"
# 此处更改为跳转到指定 url
website = 'https://busuanzi.sukap.cn'
# 部署的端口
server_port = 4567
# Redis 地址，默认 127.0.0.1 ，如果使用的是 Docker ，则填写 Redis 的 Docker 内部 IP
redis_host = '127.0.0.1'
# Redis 的映射端口，默认 6379
redis_port = 6379
# Redis 的数据库索引
redis_db = 0
# 数据库密码
redis_password = ''

r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
