现在跳一跳的外挂已经很多了，最火的比如：wangshub/wechat_jump_game

在这些外挂中，可以学到如下知识：

如何使用电脑抓取手机流量包
如何对手机进行截图（Android和苹果的不一样）
ADB的用法（ADB很小，超不过1M，功能却很强大，很丰富）
如何进行简单的图像识别
如何进行使用强化学习玩游戏
识别小人的位置是很简单的，因为小人颜色、形状比较特殊。但是识别其它形状就挺复杂了，有菱形的、蘑菇形的、圆柱形的，还有药瓶形的。

在玩跳一跳的过程中，我发现小人和目标跳板总是处在中心附近、近似对称。

如果真是这样，那么只需要找到小人的位置pos，知道中心的位置center，那么distance(pos,center)×2就相当于小人需要跳的距离。

一开始运行的时候，基本上每次都会稳稳地跳在目标平台的正中心，但是因为参数（中心位置，距离时间比）不够精确。最终死在了“药瓶”上。

使用这种方法默认前提是每次都跳在中心，如果没有跳在中心，那么随着误差的积累，早晚都要跪。

本程序的公式可以描述为：

`k×norm[(personX,personY)-(deltaX,deltaY)-(centerX,centerY)]`

其中personX，personY表示小人的坐标，这一步可以通过模板匹配法精确求得（基本上万无一失）。模板匹配除了使用opencv，还可以使用skimage，该库是纯Python实现的图像处理算法集。

deltaX，deltaY跟centerX，centerY都是常量，可以根据自己的机型进行设置。centerX和centerY并不是整个图片的中心，而是整个图片中心附近的某个点。

norm表示向量取范数，看上去跳一跳这个小程序所采用的就是二范数作为距离，距离与按压时间成正比。如果微信小程序设计成距离与按压时间不是线性关系而是其它的增函数，那就要多上一步：求按压时间和跳动距离之间的函数关系。

因为deltaX，deltaY跟centerX，centerY可以合并，所以公式可以简化为：

`k×norm[(personX,personY)-(dX,dY)]`

综上可知，微信跳一跳总共只需要3个参数：dX，dY，k。公式形式又已经求知，可以使用tensorflow实现梯度下降法求参数，这样这个问题就变成了强化学习。

一个强化学习的典型范例：NeuroEvolution : Flappy Bird。这个库纯粹使用JS实现，代码清晰简洁。它的神经网络调参采用的是遗传算法而非反向传播。FlappyBird这个游戏需要调整的参数也是非常少。

如果使用强化学习，可能需要加上一个分数识别功能。游戏失败之后，识别一下当前分数。然后自动再玩一局。把手机接上，看看它一晚上能学到啥程度。

==============================
原github地址：https://github.com/wangshub/wechat_jump_game


# 教你用 Python 来玩微信跳一跳
## 游戏模式

> 2017 年 12 月 28 日下午，微信发布了 6.6.1 版本，加入了「小游戏」功能，并提供了官方 DEMO「跳一跳」。这是一个 2.5D 插画风格的益智游戏，玩家可以通过按压屏幕时间的长短来控制这个「小人」跳跃的距离。分数越高，那么在好友排行榜更加靠前。通过 Python 脚本自动运行，让你轻松霸榜。

![](./resource/image/jump.gif)

可能刚开始上手的时候，因为时间距离之间的关系把握不恰当，只能跳出几个就掉到了台子下面。**如果能利用图像识别精确测量出起始和目标点之间测距离，就可以估计按压的时间来精确跳跃。**

## 原理说明

1. 将手机点击到《跳一跳》小程序界面

2. 用 ADB 工具获取当前手机截图，并用 ADB 将截图 pull 上来
```shell
adb shell screencap -p /sdcard/autojump.png
adb pull /sdcard/autojump.png .
```

3. 计算按压时间
  * 手动版：用 Matplotlib 显示截图，用鼠标先点击起始点位置，然后点击目标位置，计算像素距离；
  * 自动版：靠棋子的颜色来识别棋子，靠底色和方块的色差来识别棋盘；

4. 用 ADB 工具点击屏幕蓄力一跳
```shell
adb shell input swipe x y x y time(ms)
```

## 使用教程

- 方法 1：使用 app 进行一键操作。目前已适配 Win10 64位/macOS 平台 Android 一键操作，下载请移步 [STOP_jump](https://github.com/wangshub/wechat_jump_game/releases)

- 方法 2：相关软件工具安装和使用步骤请参考 [Android 和 iOS 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)

## FAQ

- 详见 [Wiki-FAQ](https://github.com/wangshub/wechat_jump_game/wiki/FAQ)

## 更新日志

- 详见 [changelog](https://github.com/wangshub/wechat_jump_game/blob/master/changelog.md)

## 开发者列表

- 详见 [contributors](https://github.com/wangshub/wechat_jump_game/graphs/contributors)

## QQ 交流

- 314659953 (1000人 已满)
- 176740763 (500人 已满)
- 89213434 (2000人 已满)
- 64389940 (2000人)
