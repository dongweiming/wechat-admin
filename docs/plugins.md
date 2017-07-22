## 插件开发

[wechat-admin](https://dongweiming.github.io/wechat-admin/) 支持插件开发。目前存在的插件都存放在 [wechat-plugins](https://github.com/dongweiming/wechat-plugins)项目中，可以提交PR把你的开发的插件贡献到这里。

### 如何使用插件

你可以直接使用现存的插件：

```bash
❯ git clone --recursive https://github.com/dongweiming/wechat-plugins
```

然后在wechat-admin的config.py或者local\_settings.py(推荐)中激活它们：

```python
PLUGIN_PATHS = [YOUR-PLUGIN-PATH]
PLUGINS = ['simsimi', 'help']
```

另外也支持直接import插件模块：

```python
import my_plugin
PLUGINS = [my_plugin, 'help']
```

### 如何编写一个插件

1. 给插件创建一个唯一名字的目录，比如插件叫做assets，为了项目结构简洁，不要直接在根目录下添加assets.py
2. 进去创建目录，添加README.md，添加该插件的一些说明
3. 添加插件程序，必要的内容如下：

```python
from wxpy.chats import Friend  # 可查看全部聊天类型
from wxpy.api.consts import TEXT  # 可查看全部消息类型


class AssetsPlugin:
    name = 'AssetsPlugin'  # 插件名字，必填
    version = '0.1'  # 版本，选填，目前还没用到
    chats = Friend  # Friend表示聊天类型，好友和我发消息时触发。默认是None，也就是会在任何类型触发
    msg_types = TEXT  # TEXT表示消息类型，只有发文本时触发。默认是None，也就是任何类型下都会触发
    except_self = True  # 是否忽略自己发的消息，理论上这种插件都要为True
    run_async = True  # 处理消息是否为异步，建议都为异步
    patterns = None  # 此插件会处理的消息模式，匹配模式才会触发，支持正则，默认。None，表示全部匹配
    exclusive = False  # 是否排外，为True表示符合此patterns的消息只能该类插件触发
    description = description  # 用于help模块显示插件描述
    exclude_patterns = ['help']  # 匹配此模式不会触发。默认为None忽略此项

    @classmethod
    def main(cls, msg):  # 需要提供名字为main的类方法，参数为wxpy传过来的msg
        result = do_sometings()
        return result
        

def export():  # 需要包含export函数，返回插件类即可
    return SimSimiPlugin 
```

可参考现在已包含的插件代码了解更多细节

** 强制要求代码经过flake8的检查 **

### 插件列表

| 插件名 | 描述 | 
| ------| ------ |
| Simsimi | 小黄鸡哟哟 |
| Help | 帮助插件，根据所有插件的description属性的内容生成 |
| Tuling | @群主即可开聊 |

