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
![travis](https://img.shields.io/travis/dongweiming/wechat-admin.svg)
![ver](https://img.shields.io/badge/release-v0.1-red.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/dongweiming/wechat-admin/issues)

# Preview

![效果图](https://github.com/dongweiming/wechat-admin/blob/master/screenshots/wechat_admin.png)

<a href="https://vimeo.com/227285498" target="_blank"><img src="https://github.com/dongweiming/wechat-admin/blob/master/screenshots/web.png" alt="Web效果" width="400" border="10" /></a>

### 欢迎扫码体验：
<img src="https://github.com/dongweiming/wechat-admin/blob/master/screenshots/chat.png" alt="扫码加群" width="640" border="10" />

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
* 支持插件系统，内置图灵机器人、ChatterBot、Simsimi等插件
* 可以指定公众号，当公众号发布文章后自动转发到指定的群聊里
* 群成员可发起投票踢人，可以灵活的设置投票规则

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


### 通用方案

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
❯ venv/bin/pip install -r requirements.txt  # 如果已经激活虚拟环境，`venv/bin/`这样的前缀可不加，下同
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
❯ venv/bin/gunicorn app:app --bind 0.0.0.0:8100 -w 6 -t 0
```

PS: 如果是本地运行，可以不使用gunicorn，直接使用Flask的多线程调试模式：

```bash
❯ python app.py
```

访问 WEB页面 http://localhost:8100 使用微信扫码登录

登录成功后，启动Celery Beat和Worker：

```bash
❯ venv/bin/celery -A wechat worker -l info -B
```

注意：第一次会拉取全部的联系人和各群聊成员列表，需要一点时间。观察终端输出了解初始化任务的完成情况。

### 使用Docker

假设已经安装了Docker，执行如下命令即可。

```bash
❯ pip install docker-compose
❯ git clone --recursive https://github.com/dongweiming/wechat-plugins
❯ venv/bin/docker-compose build
❯ venv/bin/docker-compose run init  # 只有在第一次才需要执行这步
❯ venv/bin/docker-compose run --service-ports -d web  # 启动Web，地址也是 http://localhost:8100
❯ venv/bin/docker-compose run -d celery  # 同样是在扫码登录之后再启动
```

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

## 必看: 常见问题 FAQ

### 为什么在使用一段时间后偶尔会出现`puid not found`这种错误呢？

由于微信的设计，不提供一种唯一且稳定的uid之类的数据，所以wxpy设计了一套登录用户和其相关联系人、群聊、公众号的映射关系，另外我修改了wxpy的实现，可以更多的获得caption (昵称, 性别, 省份, 城市)相关的内容，让对象中的puid更稳定。

由于其中某些人/群的设置的改变，它的puid可能改变，在每次扫码登录之后都会触发一个更新这个映射关系的任务，让这个映射关系更新成最新的。你遇到这种错误说明你需要重新登录，或者，手动触发一下这个任务：

```python
from wechat.tasks import retrieve_data
retrieve_data.delay()
```

### 为什么用着用着有时候感觉卡住了，接口不返回了？

Issue: [#9](https://github.com/dongweiming/wechat-admin/issues/9)

感谢 [@zgjhust 的意见](https://github.com/dongweiming/wechat-admin/issues/11)

这是一个小型项目，我没有添加Nginx支持，直接使用了Gunicorn。在用Gunicorn的时候使用了`-t 0`也就是不超时。

这样用的原因是项目中的sse需要一个长连接，而且从用户打开登录页面到扫码完成这个时间不好控制，就索性不超时了，但是也造成了未响应的请求不能及时释放。事实上应该把/stream拿出来特殊处理，其他的路由需要有超时时间设置的（这块，我会择机重构一下）。

现在的解决办法是指定更多的Worker数量，以及经常的重启gunicorn(使用supervisor管理会更方便）：

```bash
gunicorn app:app --bind 0.0.0.0:8100 -w 10 -t 0
```

或者不用gunicorn， 直接使用Flask的threaded参数启动：

```bash
❯ cat app.py
...
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8100, debug=app.debug, threaded=True)
     
❯ python app.py
```


### 为什么有时候发现这个管理系统已经不工作了，如果让这个系统能尽量长的工作呢？

不工作了通常有2个原因：

1. 由于微信的设计，我这个系统、Mac微信、网页微信这三者不能同时在线，否则就会被踢下线。
2. 这个系统事实上还是使用网页微信，一段时间后（我还没有总结出来这个时间阈值）会自动登出，需要你重新扫码登录。

尽管我在celery上设计的重启任务的功能，但是由于下线后重新重新扫码登录，这一步无法自动化，造成系统不工作了。

如果希望这个系统尽量长的工作，我的建议是：

1. 应该专门购买一张手机卡注册微信使用本系统，这样不会影响个人使用的微信不能登录微信客户端了。
2. 把程序不要运行在个人电脑上，可以放在vps或者其他服务器上，这样可保持正常情况下的一直在线。
3. 我给wxpy、ItChat都加了信号(Signals)系统，你可以仿造我的项目代码中的例子，加一个订阅者，能够在它有问题的时候用短信、Slack、邮件等方式第一时间通知你，让你及时处理，举个例子：

```python
from celery.task import periodic_task
from celery.task.control import revoke

def restart_listener(sender, **kw):
    task_id = r.get(LISTENER_TASK_KEY)
    if task_id:
        revoke(str(task_id, 'utf-8'))
    task_id = app.send_task('wechat.tasks.listener')
    r.set(LISTENER_TASK_KEY, task_id)

stopped.connect(restart_listener)
```

要注意订阅操作应该发生在import wxpy/itchat之前。

### 为什么这个系统功能有限？我看手机微信能做的事情要多得多嘛

是的，这是一个封装wxpy/itchat的项目，说到底还是使用网页微信(wx.qq.com)，所以它的API的功能决定了本系统的能力。

解密手机微信API，把这些未开放的API的集成进来不太好，还可能引起法律方面的问题。

### 如何解决「当前登录环境异常。为了你的帐号安全，暂时不能登录web微信...」的问题？

问题可以看这个[issue](https://github.com/Chatie/wechaty/issues/603)，有不少人遇到了，在被封之后没有办法解决。但是可以注意让它尽量不被封。经过这几天的研究，我找到三条经验：

1. 不要只使用Itchat中的[USER_AGENT](https://github.com/littlecodersh/ItChat/blob/master/itchat/config.py#L10)，可以在几个之间切换（注意要不同浏览器的UA），但是不要每次的UA不一样。
2. 注意在群内的操作不要太频繁，机器人以及自动欢迎之类的慎用，尽量减少你的回应频率。
3. 如果发现登录后突然弹出验证码，这是一个前兆，要暂停机器人功能，可以停止进程或者选择像用户那样登录网页微信或者Mac微醺客户端一段时间。

## 感谢

* [vue-admin](https://github.com/taylorchen709/vue-admin)
* [wxpy](https://github.com/youfou/wxpy)
* [ItChat](https://github.com/littlecodersh/ItChat)
