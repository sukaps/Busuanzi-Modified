# Busuanzi-Modified

修改自[@zkeq](https://github.com/zkeq)的[Busuanzi_backend_self](https://github.com/zkeq/Busuanzi_backend_self)项目  
感谢dalao开源

# 前言
前段时间不蒜子挂了找替代API的时候就找到了[@zkeq](https://github.com/zkeq)写的这个项目  
**刚开始学Python不久，就对其源码进行一个学习分析**  
然后做了一些改动，添加了 Page_uv 部署在个人的服务器上  
示例：  
使用说明：<https://busuanzi.sukap.cn/>
部署示例：<https://counter.busuanzi.sukap.cn/>  
**后端在无referer的情况下会跳转到前端示例界面**  
不过在Github上**直接点击**上方链接进入就**不会**跳转到前端示例，而是输出数据

# 改动内容

1. 将原项目中的 ``get_before_data.py`` 、 ``pv.py`` 、 ``uv.py`` 整合为一个文件，即 ``data_process.py``
2. 添加了 ``page_uv`` 记录界面的独立访客
3. 原项目中每个文件都单独连接一次Redis的操作缩减整合进 ``config.py`` 中。由于我使用的是部署在Docker上的Redis，为了方便更改各个参数，就单独分离了**部署端口**和**Redis地址**、**端口**、**数据库索引**，额外添加了**数据库密码**，也在 ``config.py`` 里面
4. 对于源码中 ``若请求中未包含 referer 头，则返回文字 "Powered by: FastAPI + Redis" `` 这一操作，将返回文字更改为跳转到指定网站，网站可在 ``config.py`` 中更改
5. 原项目内的 ``redis-server`` 是适配的 ``replit`` 的架构，所以这里直接去除了，改为调用服务器自带的Redis命令
6. ~~逐步分析源码的时候添加了点注释~~
