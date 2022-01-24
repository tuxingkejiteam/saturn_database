# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
* pip install opencv-python : 安装 cv2
* conda install shapely : 安装 shapely, pip 安装比较容易报错
"""



from setuptools import setup, find_packages

setup(

    name='SaturnDatabase',                                                                 # 打包起来的包的文件名
    version='0.0.1',                                                                        # 版本
    description='a tools for saturn database',                                              # 描述
    author='jokker|zhangyi',                                                                # 作者
    author_email='18761609908@163.com',                                                     # 邮箱

    requires=['numpy', 'pillow', 'pandas', 'easydict', 'matplotlib', 'imagehash', 'prettytable', 'progress',
              'progressbar', 'requests', 'imageio', 'pyexiv2', 'cv2', 'exifread', 'whatimage', 'pyheif',
              'pymysql', 'pytesseract', 'beautifulsoup4', 'Crypto', 'flask'
              ],          # 定义依赖哪些模块

    # 打包的python文件夹
    packages=['SaturnDatabase', 'SaturnDatabase/core', 'SaturnDatabase/db_tools', 'SaturnDatabase/db_tools/CRUD', 'SaturnDatabase/db_tools/tools',],
    # packages=find_packages('JoTools'),          # 包含所有 JoTools 中的包
    package_data={
        'SaturnDatabase/db_tools/MySQL': ['data/*.sql'],
    },
    )


# 打包的命令
# 切换到 setup.py 文件所在文件夹
# python setup.py bdist_wheel

# 注意
# 需要将用到的包全部写到 packages 参数后
# 需要在 setup.py 同级目录创建一个 test.py 文件用于测试
# requires 不能出现 *-* 格式的写法 如 scikit-image，否则会报错

# setuptools 的进一步学习参考：https://www.jianshu.com/p/ea9973091fdf



