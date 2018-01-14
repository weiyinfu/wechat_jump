import os
import time

import numpy as np
from skimage import io, feature

"""
只需要求出小人的位置，和屏幕中心的位置，就可以实现自动跳跃
万变不离其宗，不论目标方块如何变化，中心法则肯定是正确的
"""
# 把adb命令添加到环境变量
os.environ['path'] += ";" + os.path.abspath("./adb/")
# 是否调试，如果调试，保存截图
debug = True
img_count = 0  # 图片编号
person = (63, 53, 81)  # 小人的颜色
center = (650, 373)  # 中心的位置
# 小人底部中心的偏移量
delta = np.array([601, 216]) - (731, 238)
k = 2.0  # 弹性系数


def pull_screenshot():
    # 拉取截图并保存
    global img_count
    os.system('adb shell screencap -p /sdcard/autojump.png')
    if debug:
        img_count += 1
    filename = "img/" + str(img_count) + ".png"
    os.system('adb pull /sdcard/autojump.png ' + filename)
    return io.imread(filename)


def filt_color(img):
    # 颜色过滤，只识别小人的颜色
    p = np.linalg.norm(img - person, ord=2, axis=2) < 30
    grey = np.zeros(img.shape[:2])
    grey[p] = 1
    return grey


def jump(distance):
    # 跳一段距离
    press_time = distance * k
    cmd = 'adb shell input swipe 320 410 320 410 ' + str(int(press_time))
    print(cmd)
    os.system(cmd)


def getperson(img, tem):
    # 获取小人的位置
    img = img[:, :, :3]  # 去掉RGBA中的A
    img[:200, :, :] = (0, 0, 0)  # 去掉顶部
    img[1100:, :, :] = (0, 0, 0)  # 去掉底部
    # 找到与小人颜色相近的像素
    grey = filt_color(img)
    # 模板匹配寻找小人的头部
    res = feature.match_template(grey, tem)
    pos = np.unravel_index(np.argmax(res), res.shape)
    pos = pos - delta
    return pos


tem = io.imread("person.jpg")  # 小人模板图片RGB形式
tem = filt_color(tem)
while 1:
    time.sleep(3)
    img = pull_screenshot()
    person_pos = getperson(img, tem)
    distance = np.linalg.norm((np.array(person_pos) - center) * 2, ord=2)
    jump(distance)
