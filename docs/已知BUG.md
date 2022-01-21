（1）断开连接时会报错，但程序可正常完成功能。目前没让他报出来错误。也可通过手动del来解决。
        try:
            self.database.close()
        except TypeError:
            pass
