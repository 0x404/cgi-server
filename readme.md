# 多线程CGI服务器

## 使用方法

参考`Flask`框架的设计，通过装饰器让用户自己组织网站该显示的内容

```python
from cgiserver import route

@route("/webroot", method="GET")
def web_page(**kwargs):
    """Bind function `web_page` to URL '/webroot'.
    Whenever a user visit `/webroot` using `GET` mehtod,
    he will get a `this is web root page` HTML page.
    """
    response = "<p> this is web root page </p>"
    return response

```

具体请见[example.py](./example.py)，我写了一个非常详细的使用说明。

后续将会打包到`pypi`，大家可以直接通过`pip`命令安装，非常方便。

## 目前功能

* `HTTP`解析
* `HTTP`服务器
* 静态路由和`CGI`路由
* 路由装饰器

## TODO

* 最大链接数量(xzy)
* 解析HTTP用正则(wzx)
* 解析HTTP的报错处理
* 解析decorated function(zqh)
* 实现参数能够通过模板指定(zqh)
* 实现decorated function[返回模板](http://bottlepy.org/docs/dev/tutorial.html#templates)
* 欢迎重构

## 参与开发

1. 环境配置
   - Python版本需要**大于等于3.9**，主要原因是当前代码里有一些typehint之前的版本并不支持
   
   - 目前并没有依赖任何第三方库，但依赖`pylint`和`black`来做代码风格检查和静态代码分析，以及`pytest`测试
   
   - 安装方法：
     
      ``` shell
     pip3 install -r requirements.txt
     ```
     
     
   
2. 提交代码
   - github的分支保护对私有仓库要收费，虽然大家都有main分支的push权限，但请不要直接push到main分支
   - 在完成自己的功能时请自己开一个分支，在自己的分支上完成代码的提交，待功能完成后提出合并请求
   - 已经添加github action来自动完成代码风格和静态代码检查，请确保提交前自己的commit是“打钩”的状态
   - 合并请求需要至少一个approval才可以合入master（大家都有权限）


## 设计思路

利用python的`socket`编程简单实现一个服务器，对`socket`发送过来的数据做`HTTP`协议的格式解析，获得一个`Config`，其中包含`HTTP`请求中的所有内容，如访问路径，访问方法等。

* 对于静态请求很简单，根据访问路径返回一个`HTML`字符串即可
* 对于动态请求也不难，对于`python`来说，一个`python`脚本就是一个`cgi`程序，所以把`Config`的路径绑定到对应的脚本路径上，运行脚本即可
  * 更具体一些，我们可以认为一个`python`的`Callable object`就是一个`cgi`程序，从而我们可以直接绑定到一个类或者一个函数上
* 关于多线程：我现在简单地开一个主线程用来监听端口，一旦有一个新的`socket`连接过来，开一个线程去跑一个`session`处理这个`socket`（由于`HTTP`协议一次请求一次回复，所以相对好做
