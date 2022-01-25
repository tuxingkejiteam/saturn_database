import os
import hashlib
import cv2
from PIL import Image
import numpy as np
from tqdm import tqdm


def difference(image):
    # 计算图片的差值。
    # 入参：传入一张PIL图片
    # 出参：差值数组，0，1组成。
    resize_width = 9
    resize_height = 8
    smaller_image = image.resize((resize_width, resize_height))  # 图片缩放至9*8
    gray_image = smaller_image.convert("L")  # 灰度化

    # 比较相邻像素
    pixels = list(gray_image.getdata())
    diff = []
    for row in range(resize_height):
        row_start_index = row * resize_width
        for col in range(resize_width - 1):
            left_pixel_index = row_start_index + col
            diff.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
    return diff


def hamming_distance(first, second):
    # 计算两张图片的汉明距离(基于dHash算法)
    # 入参：传入两张PIL图片
    # 出参: hamming distance. 值越大,说明两张图片差别越大,反之,则说明越相似

    hm_distance = 0
    image1_difference = difference(first)
    image2_difference = difference(second)
    for index, img1_pix in enumerate(image1_difference):
        img2_pix = image2_difference[index]
        if img1_pix != img2_pix:
            hm_distance += 1
    return hm_distance


if __name__ == '__main__':
    img_match_path = '图片/7.JPG'
    img_match = Image.open(img_match_path)

    img_dir = '图片'
    for img_name in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img_name)
        img = Image.open(img_path)
        HM_distance1 = hamming_distance(img_match, img)
        print(HM_distance1)
