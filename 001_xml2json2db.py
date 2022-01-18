# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from core.jsonInfo import JsonInfo
from core.opt import Opt



# 读取 xml 中的内容，存放到数据库中


xml_path = r""
img_path = r""
json_path = r""
conf_path = r"D:\Algo\saturn_database\config.ini"
#
# a = JsonInfo()
# a.parse_xml(xml_path=xml_path)
# a.save_to_json(json_path)
# 存入数据库

opt = Opt(conf_path)


# Opt.add_json(json_path)





