（1）断开连接时会报错，但程序可正常完成功能。目前没让他报出来错误。也可通过手动del来解决。
        try:
            self.database.close()
        except TypeError:
            pass

（2）多用户访问罕见bug。
怀疑是这边还没写完，那边就已经开始查了。所以导致查询结果有问题，属于偶发现象。

(3)编码浪费bug
如果同一批次里面就有重复的，会导致重复数据的编码浪费。
目前限定了同一批次数据中，不允许出现重复的md5，否则会直接报错退出。