<p align="center">
  <img width="280" src="./assets/logo.png" alt="logo" />
</p>

# wechat-admin

> 微信管理系统

![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![vueversions](https://img.shields.io/badge/Vue.js-2.3.4-4fc08d.svg)
![es2015](https://img.shields.io/badge/ECMAScript-6-green.svg)
![celery](https://img.shields.io/badge/celery-4.0.2-4BC51D.svg)
![element ui](https://img.shields.io/badge/element-1.3.6-20a0ff.svg)
![pypi](https://img.shields.io/pypi/v/nine.svg)
![ver](https://img.shields.io/badge/release-v0.1-red.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/dongweiming/wechat-admin/issues)

## 特性

* 支持显示好友列表，可过滤
* 支持显示群聊列表，可过滤
* 可以同时给多个用户/群聊成员发送消息，支持发送文件，emoji表情。可预览
* 如果为群聊创建者，可以删除（多个）成员
* 可以选择好友/群聊成员创建新群
* 对自动建群、加群关键词、邀请文本等可配置
* 永久保存消息，可以通过消息列表页面查看和过滤。接收消息进程停止自动重启
* 支持消息提醒
* 支持发送加群聊成员好友请求
* 自动添加联系人，拉对方入群，群满之后自动创建新群

...

## 使用的技术和库

### 前端

* Vue
* Axios
* Element-ui
* Vue-cli

### 后端

* Flask
* Celery
* SSE
* [Walrus](https://github.com/coleifer/walrus)
* Gunicorn
* Flask-Migrate
* Flask-SQLAlchemy
* [ItChat](https://github.com/dongweiming/ItChat)
* [Wxpy](https://github.com/dongweiming/wxpy)
* PyMySQL

## 使用方法

安装MySQL、Redis，然后创建库（默认是test）：

```bash
❯ mysql -u root -p
mysql> drop database test;
Query OK, 9 rows affected (0.32 sec)

mysql> create database test;
Query OK, 1 row affected (0.01 sec)

mysql> ^DBye
```

下载源码并安装依赖：

```bash
❯ git clone https://github.com/dongweiming/wechat-admin
❯ cd wechat-admin
❯ virtualenv venv  # 只支持Python 3
❯ source venv/bin/activate  # 推荐使用autoenv
❯ venv/bin/pip install -r requirements.txt
```

设置说明：自定义配置应该存放在local\_settings.py（需创建）中，可重载config.py中的设置

安装插件（可选）：

```bash
❯ git clone --recursive https://github.com/dongweiming/wechat-plugins
# 如果有额外插件配置，需要修改PLUGIN_PATHS和PLUGINS
```

插件开发请移步：[Plugins Page](https://dongweiming.github.io/wechat-admin/plugins/)

初始化数据库：

```python
❯ export FLASK_APP=manager.py
❯ venv/bin/flask initdb
```

启动服务：

```bash
❯ venv/bin/gunicorn app:app --bind 0.0.0.0:8100 -w 4 -t 0
```

访问 WEB页面 http://localhost:8100 使用微信扫码登录


登录成功后，启动Celery Beat和Worker：

```bash
❯ venv/bin/celery -A wechat worker -l info -B
```

注意：第一次会拉取全部的联系人和各群聊成员列表，需要一点时间。观察终端输出了解初始化任务的完成情况。

## 本地开发

### 配置前端开发环境

安装cnpm提高包下载速度：

```bash
❯ npm install -g cnpm --registry=https://registry.npm.taobao.org
```

安装需要的包：

```bash
❯ cnpm i 
```

启动调试环境：

```bash
❯ npm run dev
```

启动成功默认会打开 http://localhost:8080 ，后端API依然使用的是 http://localhost:8100/j

本地开发完毕通过如下方式构建：

```bash
❯ npm run build
```

刷新 http://localhost:8100 就可以看到最新的效果了。

如果希望修改线上/环境的地址，需要修改build/webpack.dev.conf.js或者build/webpack.prod.conf.js中的API_URL的值。

WARN: 每次build会删除static目录，所以收到的内容被会删除，请提前备份！

### 后端开发

要注意修改表结构，每次都要：

```bash
❯ venv/bin/flask db migrate
❯ venv/bin/flask db upgrade
```

## 感谢

* [vue-admin](https://github.com/taylorchen709/vue-admin)
* [wxpy](https://github.com/youfou/wxpy)
* [ItChat](https://github.com/littlecodersh/ItChat)

## TODO

1. 设置页面可添加说明
2. 公众号自动转发
