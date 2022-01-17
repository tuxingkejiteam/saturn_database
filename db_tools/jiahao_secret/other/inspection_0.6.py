import argparse
import os
import platform
import xml.etree.ElementTree as ET
import time
import sys
# 将脚本按照下面的方式摆放：
# ----inspection_0.5.py
# ----标注文档  ----图片1.xml
#              ----图片1.xml
# 下面提供普通的和文艺的两种运行方式：
# 1、普通青年的方式：在IDE下运行脚本，需手动修改文件名
# 在pycharm下打开此脚本，将下面这个名字修改为存放xml文件的文件夹
file_name = '标注文档'
# 运行程序。

# 2、文艺青年的方式（推荐）：通过命令行传入参数，无需修改脚本，无需配置anaconda环境，无需等待IDE启动和选择环境
# 按住键盘shift，在空白处单击鼠标右键，点击：在此处打开powershell窗口。这样就进入了windows控制命令行。
# 输入命令：python inspection_0.4.py --name 标注文档
# 其中'标注文档' 为存放xml文件的文件夹名
# 按回车，即可运行程序

'''
版本号：0.6
运行环境：只需python，无需其他依赖
以实现如下功能，如有其他需求，跟老张说，我会不定期更新。
功能1：检查标注是否为xyxy格式，因为有时会误标为xywh格式
功能2：检查标注框的长宽是否大于1，因为有时候会误点一下，就变成了一个框。
功能3：生成类别统计信息，交付数据时，应同时向工程师反馈数据集的分布情况
如程序输出：'xml文件检查完成'，未发现错误。 说明xml检查无误。如输出其他文字，则按照文字提示修改。

0.6版本更新：增加了类别数量统计。给使用界面增加了进度条。修复了文档过多时的显示错误。
即将到来的功能：
1、斜框检测
2、无目标警告
'''


def main(args):
    print('当前python 版本为{}'.format(platform.python_version()), end=', ')
    xml_names = os.listdir(args.name)
    cls_dict = {}
    num = len(xml_names)
    print('共有{}个标注文件正在检测...'.format(num))
    i = 0
    no_cls_name = []
    for xml_name in xml_names:  # 遍历xml文件名

        print("\r", end="")
        print("检测进度：{}%: ".format(int(i / num * 101)), "▋" * (int(i / num * 101) // 2), end="")
        sys.stdout.flush()
        i += 1
        time.sleep(0.001)

        xml_path = args.name + '/' + xml_name  # 拼接xml路径
        tree = ET.parse(xml_path)  # 打开xml文件
        root = tree.getroot()
        for obj in root.findall('object'):  # 遍历object属性
            assert obj.find("bndbox"), '{}，缺少标注框'.format(xml_name)
            assert obj.find("name") is not None, '{}，缺少类别属性'.format(xml_name)
            bbox = obj.find("bndbox")  # 读取box的信息
            name = obj.find("name").text
            if name in cls_dict:
                cls_dict[name] += 1
            else:
                cls_dict[name] = 1
                if name is None:
                    no_cls_name.append(xml_name)

            test = 0
            for xmin in bbox.findall('xmin'):
                test += 1
            assert test == 1, '{}，无xmin标注'.format(xml_name)
            for xmax in bbox.findall('xmax'):
                test += 1
            assert test == 2, '{}，无xmax标注'.format(xml_name)
            for ymin in bbox.findall('ymin'):
                test += 1
            assert test == 3, '{}，无ymin标注'.format(xml_name)
            for ymax in bbox.findall('ymax'):
                test += 1
            assert test == 4, '{}，无ymax标注'.format(xml_name)

            xmin = int(float(bbox.find("xmin").text))
            ymin = int(float(bbox.find("ymin").text))
            xmax = int(float(bbox.find("xmax").text))
            ymax = int(float(bbox.find("ymax").text))

            if (xmax - xmin) < 2 or (ymax - ymin) < 2:
                print('{}，标注框变成一个点啦！'.format(xml_name))
                return -1
    print('\n数据集分布：')
    for key in cls_dict:
        print(key, '=', cls_dict[key])
    if len(no_cls_name) == 0:
        print('xml文件检查完成，未发现错误。')
    else:
        print('无类别名称:', end=' ')
        for no_cls in no_cls_name:
            print(no_cls)


parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, default=file_name)  # 图片地址
opt = parser.parse_args()
main(opt)
