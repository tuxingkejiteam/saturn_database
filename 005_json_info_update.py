# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# (1) 指定要修改的 uc_list (2) 指定要修改的属性 （3）opt.update （4）提交到数据库 update json

# fixme 使用 labelimg 去标注 xml 之后，xml 之前的 id 信息就会消失了，要好好处理这个问题

#

self.org_name = None
self.unique_code = None
self.size = None
self.H = None
self.W = None
self.MD5 = None
self.trace = None
self.objects = []
self.mode = None  # 输配变模式, 输电，配电还是变点
self.train_info = None
self.extra_info = None
self.json_path = json_path


# fixme 更新 obj 但是不更新重要属性
    # （更新）obj 信息，
    # （不更新）属性信息如 org_name，unique_code，H, W, MD5, trace, mode, train_info, extra_info, json_path



















