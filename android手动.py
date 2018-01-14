import os
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math

os.environ['path'] += ";" + os.path.abspath("adb/")
print(os.environ['path'])


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
img = np.array(Image.open('autojump.png'))
im = plt.imshow(img, animated=True)

update = True
click_count = 0
cor = []


def updatefig(*args):
    global update
    if update:
        time.sleep(1.5)
        pull_screenshot()
        im.set_array(np.array(Image.open('autojump.png')))
        update = False
    return im,


def on_click(event):
    global update
    global ix, iy
    global click_count
    global cor

    ix, iy = event.xdata, event.ydata
    print('now = ', ix, iy)
    cor.append((ix, iy))

    click_count += 1
    if click_count > 1:
        click_count = 0
        distance = math.hypot(cor[0][0] - cor[1][0], cor[0][1] - cor[1][1])
        jump(distance)
        update = True
        cor = []


fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
