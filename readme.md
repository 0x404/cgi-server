# 多线程CGI服务器

## 教程

### 从PYPI安装

在线安装（PyPI上有项目源码，该下载方式在结课前暂不可用）

```shell
pip install cgi-server
```

本地安装，从最新的[release](https://github.com/0x404/cgi-server/releases/)中下载`.whl`文件，下载完成后执行如下命令（注意版本命名）

```shell
pip install cgi_server-1.2.1-py3-none-any.whl
```


### 从源码安装

下载源码，可以从最新的[release](https://github.com/0x404/cgi-server/releases/)下载代码，也可以通过git下载

```shell
git clone git@github.com:0x404/cgi-server.git
```

下载完成后，进入文件根目录，执行安装命令

```shell
python setup.py install
```

安装成功后，即可作为一个普通的Python库使用

### 使用

下面的例子构建了一个如何利用本库快速创建一个`hello world`页面


```python
# hello.py
from cgiserver import route, run

@route("/helloworld", method="GET")
def web_page(**kwargs):
    response = "<h1> Hello World </h1>"
    return response

if __name__ == "__main__":
    run("127.0.0.1", 8888)
```

执行如下命令：

```
python hello.py
```

即可在`http://127.0.0.1:8888/helloworld`看到一个`hello world`页面

更详细的使用说明请见[example.py](./example.py)，里面详细介绍了本库的各种功能

## 卸载

使用如下命令完成卸载

```shell
pip uninstall cgi-server
```



## 目前功能

* `HTTP`解析
* `HTTP`服务器
* 静态路由和`CGI`路由
* 路由装饰器
* 最大链接数量



## TODO

* 解析HTTP的报错处理(wzx)
* 解析decorated function(zqh)
* 实现参数能够通过模板指定(zqh)
* 完善HTTP返回代码400和403的处理
* 解析HTTP用正则匹配
* 完善[测试](./tests/)，目前的测试不够完善，尤其是对出错处理
* 服务器处理请求可以说是一个IO形的行为，有很多时间消耗在（等待）输入/输出上；Python的全局解释锁导致这类程序多线程和单线程区别并不是很大，为了提高系统性能，我们是不是应该用多进程来替代多线程呢？
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
