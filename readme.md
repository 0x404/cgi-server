# 多线程CGI服务器

## 教程

### 从PYPI安装

使用`pip`安装，需要python版本**>=3.9**

```shell
pip install cgi-server
```



### 从源码安装

下载源码，需要python版本**>=3.9**，可以从最新的[release](https://github.com/0x404/cgi-server/releases/)下载代码，也可以通过git下载

```shell
git clone git@github.com:0x404/cgi-server.git
```

下载完成后，进入文件根目录，执行安装命令

```shell
python setup.py install
```

安装成功后，即可作为一个Python库使用

### 使用

下面的例子构建了一个如何利用本库快速创建一个`hello world`页面


```python
# hello.py
from cgiserver import route, run

@route("/helloworld", method="GET")
def web_page():
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

除此之外，可以参考这个[仓库](https://github.com/0x404/computer-network-practice)，在这个仓库中使用本框架构建了一个网页应用程序，支持静态页面，`Ajax`请求等功能

### 卸载

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
* 解析HTTP的报错处理
* 错误代码400, 403, 404处理和用户自定义模板


## 参与开发

详细要求请见[CONTTRIBUTING.md](docs/CONTRIBUTING.md)

