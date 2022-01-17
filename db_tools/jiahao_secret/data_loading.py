import argparse
from rename import load_data
import pymysql
from update_objects import update_objects
from PIL import Image


def main(args):
     path =r'F:\20220104泰州部署\jyzPS\inputImg'
     path1 = r'F:\20220104泰州部署\jyzPS\output'
     path2 =r'F:\20220104泰州部署\jyzPS\output_json'
     load_data(path,path1, path2)
    #load_data(args.img_org_dir,args.img_output_dir,args.json_output_dir) #入库脚本目录下的data目录中的数据（data目录中可包含xml，json等标注文件）
    #update_objects(args.img_org_dir,args.json_output_dir)              #已入库数据标注后将xml,json内容合并在图片关联json中


    # xml_path=r'E:\入库器\已入库的xml更新'
    # json_path=r'C:\Users\zzc\Desktop\待更新json\json'
    # update_objects(xml_path, json_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_org_dir', type=str, default='data1')            #导入数据原始目录
    parser.add_argument('--img_output_dir', type=str, default='output1')       #导出重命名图片所在目录
    parser.add_argument('--json_output_dir', type=str, default='output_json1') #导出重命名图片对应json所在目录
    opt = parser.parse_args()
    assert opt.img_output_dir != opt.img_org_dir, "请检查输出目录是否正确！"
    main(opt)