import os
import time

import cv2
import matplotlib.animation as animation
import matplotlib.pyplot as plt

"""
opencv模板匹配法求小人位置，因为没有对图片进行颜色过滤，小人位置识别准确率较低
每次只需要点击目标点即可，无需点击小人位置
"""
os.environ['path'] += ";" + os.path.abspath('adb')
print(os.environ['path'])
# 图片缩放比例，将图片缩放之后，识别速度会提升
scale = 0.25
template = cv2.imread('person.jpg')
template = cv2.resize(template, (0, 0), fx=scale, fy=scale)


def search(img):
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    cv2.rectangle(
        img,
        (min_loc[0], min_loc[1]),
        (min_loc[0] + template.shape[1], min_loc[1] + template.shape[0]),
        (255, 0, 0),
        4)
    return img, min_loc[0] + template.shape[1] / 2, min_loc[1] + template.shape[0]


def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')


def jump(distance):
    press_time = distance * 2.00
    press_time = int(press_time)
    cmd = 'adb shell input swipe 320 410 320 410 ' + str(press_time)
    print(cmd)
    os.system(cmd)


fig = plt.figure()
pull_screenshot()
img = cv2.imread('autojump.png')
img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
im = plt.imshow(img, animated=True)

update = True


def updatefig(*args):
    global update
    global src_x, src_y

    if update:
        time.sleep(1)
        pull_screenshot()
        img = cv2.imread('autojump.png')
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
        img, src_x, src_y = search(img)
        im.set_array(img)
        update = False
    return im,


def on_click(event):
    global update
    global src_x, src_y

    dst_x, dst_y = event.xdata, event.ydata

    distance = (dst_x - src_x) ** 2 + (dst_y - src_y) ** 2
    distance = (distance ** 0.5) / scale
    print('distance = ', distance)
    jump(distance)
    update = True


fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, updatefig, interval=5, blit=True)
plt.show()
