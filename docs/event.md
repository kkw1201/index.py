Index 允许注册若干个事件处理程序，以处理在应用程序启动之前或关闭时需要运行的代码。

* `on_startup`: Index 启动之前运行的函数
* `on_shutdown`: Index 关闭之前运行的函数

## 注册事件

你可以用装饰器语法注册事件处理程序，注册普通函数或由 `async def` 定义的异步函数均可。

```python
import logging

from indexpy import Index

app = Index()
logger = logging.getLogger("example")


@app.on_startup
def logger_on_startup():
    logger.info("Called on startup")


@app.on_shutdown
def logger_on_shutdown():
    logger.info("Called on shutdown")
```
