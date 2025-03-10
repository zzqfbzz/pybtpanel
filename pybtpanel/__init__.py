# -*- coding: utf-8 -*-

import time
import hashlib
import json
import requests

requests.packages.urllib3.disable_warnings()


class bt_api:

    def __init__(self, bt_url=None, bt_key=None):
        if bt_url:
            self.__BT_URL = bt_url
            self.__BT_KEY = bt_key

    def __get_md5(self, s):
        """
        计算MD5
        :param s:
        :return:
        """
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        return m.hexdigest()

    def __get_key_data(self):
        """
        构造带有签名的关联数组

        :return:
        """
        now_time = int(time.time())
        requests_data = {
            "request_token": self.__get_md5(str(now_time) + '' + self.__get_md5(self.__BT_KEY)),
            "request_time": now_time
        }
        return requests_data

    def __http_post(self, url, requests_data, timeout=1800):
        """
        发送POST请求，忽略SSL验证(因为自签的原因)
        :param url:
        :param requests_json:
        :param timeout:
        :return:
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # 使用requests发送POST请求并禁用SSL验证
        response = requests.post(url, data=requests_data, headers=headers, timeout=timeout, verify=False)

        return response.text

    def get_logs(self):
        """
        获取日志列表
        :return:
        """

        url = self.__BT_URL + '/data?action=getData'
        requests_data = self.__get_key_data()

        requests_data['table'] = 'logs'
        requests_data['limit'] = 10
        requests_data['tojs'] = 'test'

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_systeminfo(self):
        """
        获取系统基础统计
        :return:
        """
        url = self.__BT_URL + '/system?action=GetSystemTotal'
        requests_data = self.__get_key_data()

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_diskinfo(self):
        """
        获取磁盘分区信息
        :return:
        """
        url = self.__BT_URL + '/system?action=GetDiskInfo'
        requests_data = self.__get_key_data()

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_network(self):
        """
        获取实时状态信息(CPU、内存、网络、负载)
        :return:
        """
        url = self.__BT_URL + '/system?action=GetNetWork'
        requests_data = self.__get_key_data()

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_taskcount(self):
        """
        检查是否有安装任务
        :return:
        """
        url = self.__BT_URL + '/ajax?action=GetTaskCount'
        requests_data = self.__get_key_data()

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_panelup(self):
        """
        检查面板更新
        :return:
        """
        url = self.__BT_URL + '/ajax?action=UpdatePanel'
        requests_data = self.__get_key_data()

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_sitelist(self, limit=10, page=None, site_type=None, order=None, tojs=None, search=None):
        """
        参数名称参数值示例说明
        :param limit:取回的数据行数【默认10】
        :param page:当前分页[可选]
        :param site_type:分类标识,-1:分部分类0:默认分类[可选
        :param order:排序规则使用id降序：iddesc使用名称升序：namedesc[可选]
        :param tojs:分页JS回调,若不传则构造URI分页连接[可选]
        :param search:搜索内容[可选]
        :return:
        """
        url = self.__BT_URL + '/data?action=getData&table=sites'
        requests_data = self.__get_key_data()

        requests_data['limit'] = limit
        requests_data['p'] = page
        requests_data['type'] = site_type
        requests_data['order'] = order
        requests_data['tojs'] = tojs
        requests_data['search'] = search

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_sitetypes(self):
        """
        获取网站分类
        :return:
        """
        url = self.__BT_URL + '/site?action=get_site_types'
        requests_data = self.__get_key_data()
        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_phpversion(self):
        """
        获取已安装的PHP版本列表
        :return:
        """
        url = self.__BT_URL + '/site?action=GetPHPVersion'
        requests_data = self.__get_key_data()
        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def add_site(self, webname: dict, path, type_id, station_type, version, port,
                 ps, ftp: bool, ftp_username, ftp_password, sql: bool, codeing, datauser, datapassword):
        """
        创建网站

        :param webname:网站主域名和域名列表 请传JSON[必传]  {"domain":"domain.com","domainlist":[],"count":0}
        :param path:根目录 [必传]  /www/wwwroot/domain.com
        :param type_id:分类标识 [必传]
        :param station_type:项目类型 请传PHP[必传]
        :param version:PHP 版本 请从PHP版本列表中选择 [必传]
        :param port:网站端口 [必传]
        :param ps:网站备注 [必传]
        :param ftp:是否创建FTP[必传]
        :param ftp_username:FTP 用户名 在要创建FTP时必传
        :param ftp_password: FTP 密码 在要创建FTP时必传
        :param sql:是否创建数据库[必传]
        :param codeing:数据库字符集 在要创建数据库时必传 [utf8|utf8mb4|gbk|big5]
        :param datauser:数据库用户名及名称在要创建数据库时必传
        :param datapassword:数据库密码在要创建数据库时必传
        :return:
        """

        url = self.__BT_URL + '/site?action=AddSite'
        requests_data = self.__get_key_data()

        requests_data['webname'] = json.dumps(webname)
        requests_data['path'] = path
        requests_data['type_id'] = type_id
        requests_data['station_type'] = station_type
        requests_data['version'] = version
        requests_data['port'] = port
        requests_data['ps'] = ps
        requests_data['ftp'] = ftp
        requests_data['ftp_username'] = ftp_username
        requests_data['ftp_password'] = ftp_password
        requests_data['sql'] = sql
        requests_data['codeing'] = codeing
        requests_data['datauser'] = datauser
        requests_data['datapassword'] = datapassword

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def del_site(self, site_id, webname, path, database, ftp):
        """
        删除网站
        :param site_id:网站ID[必传]
        :param webname:网站名称[必传]
        :param path:是否删除网站根目录，如果不删除请不要传此参数[可选]
        :param database:是否删除关联数据库，如果不删除请不要传此参数[可选]
        :param ftp:是否删除关联FTP，如果不删除请不要传此参数[可选]
        :return:
        """
        url = self.__BT_URL + '/site?action=DeleteSite'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['webname'] = webname
        requests_data['path'] = path
        requests_data['database'] = database
        requests_data['ftp'] = ftp

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def stop_site(self, site_id, webname):
        """
        停用网站
        :param site_id:
        :param webname:
        :return:
        """
        url = self.__BT_URL + '/site?action=SiteStop'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['name'] = webname

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def start_site(self, site_id, webname):
        """
        启用网站
        :param site_id:
        :param webname:
        :return:
        """
        url = self.__BT_URL + '/site?action=SiteStart'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['name'] = webname

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_expdate(self, site_id, exp_date):
        """
        网站到期时间
        :param site_id:网站ID [必传]
        :param exp_date: 到期时间 永久：0000-00-00[必传]
        :return:
        """
        url = self.__BT_URL + '/site?action=SetEdate'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['edate'] = exp_date

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_ps(self, site_id, ps=None):
        """
        修改网站备注
        :param site_id:
        :param ps:
        :return:
        """
        url = self.__BT_URL + '/data?action=setPs&table=sites'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['ps'] = ps

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_sitebakeups(self, page, limit, tojs, search):
        """
        获取网站备份列表
        :param page:
        :param limit:
        :param tojs:
        :param search:
        :return:
        """
        url = self.__BT_URL + '/data?action=getData&table=backup'
        requests_data = self.__get_key_data()

        requests_data['p'] = page
        requests_data['limit'] = limit
        requests_data['tojs'] = tojs
        requests_data['search'] = search
        requests_data['type'] = 0

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_sitebackup(self, site_id):
        """
        创建网站备份
        :param site_id:
        :return:
        """
        url = self.__BT_URL + '/site?action=ToBackup'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def del_backup(self, backup_id):
        """
        删除网站备份
        :param backup_id:
        :return:
        """

        url = self.__BT_URL + '/site?action=DelBackup'
        requests_data = self.__get_key_data()

        requests_data['id'] = backup_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_sitedomainlist(self, site_id):
        """
        获取网站的域名列表
        :param site_id:
        :return:
        """
        url = self.__BT_URL + '/data?action=getData&table=domain'
        requests_data = self.__get_key_data()

        requests_data['search'] = site_id
        requests_data['list'] = True

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def add_domain(self, site_id, webname, domain):
        """
        添加域名
        :param site_id:
        :return:
        """
        url = self.__BT_URL + '/site?action=AddDomain'
        requests_data = self.__get_key_data()

        requests_data['search'] = site_id
        requests_data['webname'] = webname
        requests_data['domain'] = domain

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def del_domain(self, site_id, webname, domain, port):
        """
        删除域名
        :param site_id:
        :param webname:
        :param domain:
        :param port:
        :return:
        """

        url = self.__BT_URL + '/site?action=DelDomain'
        requests_data = self.__get_key_data()

        requests_data['search'] = site_id
        requests_data['webname'] = webname
        requests_data['domain'] = domain
        requests_data['port'] = port

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_rewritelist(self, siteName):
        """
        获取可选的预定义伪静态列表
        :param siteName:网站名称[必传]
        :return:
        """
        url = self.__BT_URL + '/site?action=GetRewriteList'
        requests_data = self.__get_key_data()

        requests_data['siteName'] = siteName

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_filebody(self, path):
        """
        获取指定预定义伪静态规则内容(获取文件内容)
        取网站配置文件内容(获取文件内容)
        :return:
        """
        url = self.__BT_URL + '/files?action=GetFileBody'
        requests_data = self.__get_key_data()

        requests_data['path'] = path

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_filebody(self, path, data):
        """
        保存伪静态规则内容(保存文件内容)
        保存网站配置文件(保存文件内容)
        :param path:
        :param data:
        :return:
        """
        url = self.__BT_URL + '/files?action=SaveFileBody'
        requests_data = self.__get_key_data()

        requests_data['path'] = path
        requests_data['data'] = data
        requests_data['encoding'] = 'utf-8'

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_sitepath(self, site_id):
        """
        取回指定网站的根目录
        :param site_id:
        :return:
        """
        url = self.__BT_URL + '/data?action=getKey&table=sites&key=path'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_diruserini(self, site_id, path):
        """
        取回防跨站配置/运行目录/日志开关状态/可设置的运行目录列表/密码访问状态

        """
        url = self.__BT_URL + '/site?action=GetDirUserINI'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['path'] = path

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_diruserini(self, path):
        """
        设置防跨站状态(自动取反)

        """
        url = self.__BT_URL + '/site?action=SetDirUserINI'
        requests_data = self.__get_key_data()

        requests_data['path'] = path

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_accesslogs(self, site_id):
        """
        设置写访问日志

        """
        url = self.__BT_URL + '/site?action=logsOpen'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_sitepath(self, site_id, path):
        """
        修改网站根目录

        """
        url = self.__BT_URL + '/site?action=SetPath'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['path'] = path

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_siteaccesslogs(self, site_id, path):
        """
        设置是否写网站访问日志

        """
        url = self.__BT_URL + '/site?action=SetSiteRunPath'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['path'] = path

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_accesspwd(self, site_id, username, password):
        """
        设置密码访问

        """
        url = self.__BT_URL + 'site?action=SetHasPwd'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['username'] = username
        requests_data['password'] = password

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def close_accesspwd(self, site_id):
        """
        关闭密码访问

        """
        url = self.__BT_URL + '/site?action=CloseHasPwd'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_limitnet(self, site_id):
        """
        获取流量限制相关配置（仅支持nginx）

        """
        url = self.__BT_URL + '/site?action=GetLimitNet'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_limitnet(self, site_id, perserver, perip, limit_rate):
        """
        开启或保存流量限制配置（仅支持nginx）

        """
        url = self.__BT_URL + '/site?action=SetLimitNet'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id
        requests_data['perserver'] = perserver
        requests_data['perip'] = perip
        requests_data['limit_rate'] = limit_rate

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def close_limitnet(self, site_id):
        """
        关闭流量限制（仅支持nginx）

        """
        url = self.__BT_URL + '/site?action=CloseLimitNet'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def get_index(self, site_id):
        """
        取默认文档信息

        """
        url = self.__BT_URL + '/site?action=GetIndex'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        result = self.__http_post(url, requests_data)
        return json.loads(result)

    def set_index(self, site_id, index):
        """
        设置默认文档

        """
        url = self.__BT_URL + '/site?action=SetIndex'
        requests_data = self.__get_key_data()

        requests_data['id'] = site_id

        requests_data['Index'] = index

        result = self.__http_post(url, requests_data)
        return json.loads(result)
