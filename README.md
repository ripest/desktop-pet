# Desktop pet python implementation

### Procedure description:

Table PET: the desktop pet implemented by Python plays an action in 10 seconds by default. Double click the left mouse button to activate the walking function, and click again to cancel the walking. The right mouse button has some simple system functions, which will be added later
The default image is reproduced from @ xgbghost (Weibo)
Of course, if you have your own pictures, you can replace them or add more actions

### Environment and usage

Based on Python 3.7, pyqt5

`Python run.py` can run the table pet, which is executed by the daemons by default. The input and output of the standard data are in the stderr, stdin, and stdout files

`--no-daemons` starts in a non daemons mode

`--tray`  tray function

### Document description
`core/action.py` file is every action of the table pet (the real file is under the 'img' folder),

You can add actions, you can also reduce actions
If you add actions, you can put the pictures of one frame in the 'img' folder, and then configure the address in 'action. Py', and the program will read it automatically

`core/setting.py` file is a configuration file. The description is as follows

```Yaml
MOVIE_TIME_INTERVAL: the playback interval of each animation, in seconds

INIT_PICTURE: the default picture when the table pet is still

TRAY_ICON: system tray icon

ICON: picture of program

MOUSE_TO_LEFT_*: the action of mouse sliding left, three frames in total

MOUSE_TO_RIGHT_*: the action of right mouse slide, three frames in total

Walk: the action of walking, 2 frames in total, the redundant will not be played
```



###Contact information

QQ: 469554659

email: 469554659@qq.com

If you have new ideas or problems with the operation, please contact me



# 桌面宠物 python实现

### 程序说明:
桌宠:python实现的桌面宠物 默认10秒播放一个动作, 鼠标双击左键 激活行走功能, 再次单击可以取消行走, 右键有一些简单的系统功能,后续会增加
 默认的图片是转载自 @XGBGHOST (微博)
当然, 如果你有自己的图片,可以进行替换, 也可以增加动作

### 环境及使用
基于python3.7, PyQt5

`python run.py` 即可运行 桌宠默认以守护进程来执行, 标椎输入输出在 stderr, stdin, stdout 文件里
`--no-daemon`  用非守护进程方式启动
`--tray` 启动托盘功能

### 文件说明
`core/action.py` 文件下是 桌宠每一个动作(真正的文件在`img`文件夹下), 
可以加动作,也可以减少动作
如果加动作,可以把一帧帧的图片放在`img`文件夹下, 然后再`action.py`里配置好地址,程序自动读取

`core/setting.py` 文件 是配置,说明如下

```Yaml
MOVIE_TIME_INTERVAL: 每个动画的播放间隔, 单位 秒
INIT_PICTURE: 桌宠静止时默认的图片
TRAY_ICON: 系统托盘的图标
ICON: 程序的图片
MOUSE_TO_LEFT_*: 鼠标左滑时的动作, 一共三帧
MOUSE_TO_RIGHT_*: 鼠标右滑时的动作, 一共三帧
WALK: 行走的动作, 一共2 帧, 多余的不会播放
```

### 联系方式
QQ: 469554659  
email: 469554659@qq.com  
如果有新的想法,或者运行有问题,可联系我  
