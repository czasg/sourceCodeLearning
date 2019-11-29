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

每一个线程存储数据的地方就是一个stack，也就是一个列表，两个方法一个push一个pop，也就是仅在顶部进行插入或者删除
* 队列FIFO -> 先入先出
* 堆栈LIFO -> 先入后出
每一个线程都会在 线程本地数据 维护一个自己的堆栈，用来存放RequestContext和AppContext上下文
所以我们平常使用的全局对象request/session/g是安全的。
这里的g是当前请求的全局变量，仅在一次请求中起作用


用户发起请求 --> 通过werkzeug获取environ和start_response --> Flask创建两个对象 --> 创建Response之后AppContext和RequestContext都将销毁
                                                            -> AppContext  --> 内部包含app和g
                                                            -> RequestContext  --> 内部包含request和session
                                                                -> request: 在RequestContext内部由environ创建的，将RequestContext推到本地线程数据堆栈中，调用request就直接从这里面取出来即可
                                                                -> session: 神奇的session. flask的session和平常的不太一样
                                                                    -> server slide session: session信息保存在server端. 我会传递里面的某些值，渗入salt组成一个无法解读的秘钥。
                                                                    -> client slide session: session是完整的数据串。只要我们能够拿到salt，我们就可以轻易的逆解数据，这其实是一个比较危险的。
                                                                -> app: AppContext 每一次请求都会创建. 包含g
                                                                -> g: _AppCtxGlobals 每一次请求都会创建，而且是在新线程内创建的，仅对当前线程表示为全局可见. 这个对象非常普通，没有任何技术含量




"""
