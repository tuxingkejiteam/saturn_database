import argparse
import os
import platform
import xml.etree.ElementTree as ET
import time
import sys
import shutil

# 将脚本按照下面的方式摆放：
# ----inspection_0.8.py
# ----标注文档  ----图片1.xml
#              ----图片1.xml
# 下面提供普通的和文艺的两种运行方式：
# 1、普通青年的方式：在IDE下运行脚本，需手动修改文件名
# 在pycharm下打开此脚本，将下面这个名字修改为存放xml文件的文件夹
file_name = '标注文档'
# 运行程序。

# 2、文艺青年的方式（推荐）：通过命令行传入参数，无需修改脚本，无需配置anaconda环境，无需启动pycharm
# 按住键盘shift，在空白处单击鼠标右键，点击：在此处打开powershell窗口。这样就进入了windows控制命令行。
# 输入命令：python inspection_0.8.py --name 标注文档
# 其中'标注文档' 为存放xml文件的文件夹名
# 按回车，即可运行程序
# 如程序输出：'xml文件检查完成，未发现错误。' 说明xml检查无误。如输出其他文字，则按照文字提示修改。

'''
版本号：0.8
运行环境：只需python，无需其他依赖
作者：张一，如有其他需求，跟老张说，我会不定期更新。
功能列表：
功能1：检查标注是否为xyxy格式，因为有时会误标为xywh格式。
功能2：检查标注框的长宽是否大于1，因为有时候会误点一下，就变成了一个框。
功能3：生成类别统计信息，交付数据时，应同时向工程师反馈数据集的分布情况。
功能4：检查文件后缀，但不会作为错误写入检测报告，仅作输出展示。
功能5：检测被误标为斜框的的xml文件。

0.8版本更新：增加了检查文件后缀的功能。增加了误标为斜框的检测。修复了一些文字错误。未通过检测的文件会在终端进行输出展示。
已知问题：
1、当一个xml中有多个错误时，错误描述会在检测报告中重复输出。
2、文件后缀错误，不会出现在检测报告中。
即将到来的功能：
1、常见目标的中文对照
'''


def main(args):
    if os.path.exists("检测报告") is False:
        os.makedirs("检测报告")
    txt_path = '检测报告/检测报告.txt'
    file = open(txt_path, 'w')

    print('当前python 版本为{}'.format(platform.python_version()), end=', ')
    xml_names = os.listdir(args.name)
    cls_dict = {}
    wrong_dict = {}
    num = len(xml_names)
    print('共有{}个标注文件正在检测...'.format(num))
    file.write('### 共计检测文件{}个 ###'.format(num))
    i = 0
    other = 0
    for xml_name in xml_names:  # 遍历xml文件名
        if not xml_name.endswith('.xml'):
            other += 1
            if other == 1:
                print('\nxml里面混入了一个奸细：{}'.format(xml_name))
            else:
                print('\nxml里面又混入了一个奸细：{}'.format(xml_name))
            continue
        wrong_str = ''
        i += 1
        print("\r", end="")
        print("已检测{}个文件，检测进度：{}%: ".format(i, int(i / num * 100)), "▋" * (int(i / num * 101) // 2), end="")
        sys.stdout.flush()
        time.sleep(0.001)

        xml_path = args.name + '/' + xml_name  # 拼接xml路径
        tree = ET.parse(xml_path)  # 打开xml文件
        root = tree.getroot()
        for obj in root.findall('object'):  # 遍历object属性
            assert obj.find("name") is not None, '{}，缺少类别属性'.format(xml_name)
            if obj.find('robndbox'):
                wrong_str += '误标为斜框啦！'
                continue
            else:
                bbox = obj.find("bndbox")  # 读取box的信息
                name = obj.find("name").text
                if name in cls_dict:
                    cls_dict[name] += 1
                else:
                    cls_dict[name] = 1

                test = 0
                for xmin in bbox.findall('xmin'):
                    test += 1
                if test != 1:
                    wrong_str += '无xmin标注 '
                    continue
                for xmax in bbox.findall('xmax'):
                    test += 1
                if test != 2:
                    wrong_str += '无xmax标注 '
                    continue
                for ymin in bbox.findall('ymin'):
                    test += 1
                if test != 3:
                    wrong_str += '无ymin标注 '
                    continue
                for ymax in bbox.findall('ymax'):
                    test += 1
                if test != 4:
                    wrong_str += '无ymax标注 '
                    continue

                xmin = int(float(bbox.find("xmin").text))
                ymin = int(float(bbox.find("ymin").text))
                xmax = int(float(bbox.find("xmax").text))
                ymax = int(float(bbox.find("ymax").text))

                if (xmax - xmin) < 2 or (ymax - ymin) < 2:
                    wrong_str += '标注框变成一个点啦！'

        if len(wrong_str) != 0:
            wrong_dict[xml_name] = wrong_str

    print('\n数据集分布：')
    file.write('\n数据集分布：\n')
    for key in cls_dict:
        print(key, '=', cls_dict[key])
        file.write(key + '=' + str(cls_dict[key]) + '\n')

    if len(wrong_dict) != 0:
        print('共有{}个文件未通过检测，请在检测报告中查看详情！'.format(len(wrong_dict)))
        file.write('\n问题xml列表：\n')
        for key in wrong_dict:
            print(key, ' ', wrong_dict[key])
            file.write(key + '    ' + str(wrong_dict[key]) + '\n')
            wrong_path = args.name + '/' + key
            shutil.copy(wrong_path, '检测报告/' + key)
    else:
        print('xml文件检查完成，未发现错误。')
        file.write('未发现文件错误。')


parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, default=file_name)  # 图片地址
opt = parser.parse_args()
main(opt)
