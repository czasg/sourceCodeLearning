__file__ = '笔记本'


"""
Flask是基于werkzeug三方包，搭建的wsgi应用开发框架
底层逻辑由第三方搭建，flask实际就是一个较完善的wsgi应用

http连接是一个无状态无连接的请求
每次请求资源都是固定的，由底层打包并传递environ环境量

flask实现了一种与threading.Local一样的【线程本地数据】
各个线程能够以全局变量的形式维护自己的数据
原理也还是比较简单的。确实有一个全局变量Local，但是在Local中，每一个线程都会维护自己的 本地数据
以字典作为基础的数据结构，以每个线程的线程ID作为唯一key，以每个线程需要维护的变量字典作为value

在flask中是一样，但是flask在此基础上推出了stack式本地变量。

threading.Local => local._local__impl.dicts
Flask => _request_ctx_stack._local.__storage__

???? 找到了数据存储的地方。但是问题还是存在，怎么就能够保存push/pop的数据不会混乱呢 ???


"""




