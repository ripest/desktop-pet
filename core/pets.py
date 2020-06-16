import random
import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QMenu, QApplication, QSystemTrayIcon, QAction, QMainWindow

from core import action
from core.ability import Ability
from core.conf import settings


class DesktopPet(QMainWindow):
    """桌宠核心类"""

    def __init__(self, parent=None, tray=False):
        super(DesktopPet, self).__init__(parent)
        self.imgDir = settings.SETUP_DIR / "img"
        self.walking = False
        self.playing = False
        self.draging = False
        self.autoFalling = False
        self.contenting = False
        self.tray = tray
        self.initUI()
        self.startMovie()

    def initUI(self):
        """初始化窗口"""
        self.setWindowIcon(QIcon(str(self.imgDir / settings.ICON)))
        self.desktop = QApplication.desktop()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明

        if self.tray:
            self.trayMenu()  # 系统托盘

    def trayMenu(self):
        """显示系统托盘"""
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(str(self.imgDir / settings.TRAY_ICON)))
        tray.show()

    def mousePressEvent(self, event):
        """鼠标单击事件"""
        if self.playing:
            return
        if event.button() == Qt.LeftButton:
            self.walking = False  # 单击 关闭跑步
            self.draging = True
            self.mDragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        # 双击鼠标 启动walk, 所以释放的时候要判断是否是双击的情况
        if self.walking is False:
            if self.autoFalling:
                self.fallingBody((event.globalPos() - self.mDragPosition).x(), event.globalPos().y())
            else:
                self.setPix(str(self.imgDir / settings.INIT_PICTURE))

            self.draging = False

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.playing or self.walking:
            return
        if Qt.LeftButton:
            self.move(event.globalPos() - self.mDragPosition)
            moveDistance = (self.mDragPosition - event.pos()).x()
            if -1 <= moveDistance < 0:
                self.setPix(str(self.imgDir / settings.MOUSE_TO_RIGHT_1))
            elif -2 <= moveDistance < -1:
                self.setPix(str(self.imgDir / settings.MOUSE_TO_RIGHT_2))
            elif moveDistance < -2:
                self.setPix(str(self.imgDir / settings.MOUSE_TO_RIGHT_3))

            elif 0 < moveDistance <= 1:
                self.setPix(str(self.imgDir / settings.MOUSE_TO_LEFT_1))
            elif 1 < moveDistance <= 2:
                self.setPix(str(self.imgDir / settings.MOUSE_TO_LEFT_2))
            elif 2 < moveDistance:
                self.setPix(str(self.imgDir / settings.MOUSE_TO_LEFT_3))

    def mouseDoubleClickEvent(self, QMouseEvent):
        """鼠标双击事件, 进行walk"""
        if self.playing:
            return
        if Qt.LeftButton == QMouseEvent.button():
            self.walking = True
            self.walk()

    def closeEvent(self, QCloseEvent):
        """关闭事件"""
        #  如何在walk 的时候关闭, 会导致程序坞的图标不消失,所以要先停掉walk
        self.walking = False

    def contextMenuEvent(self, e):
        """右键菜单"""
        if self.walking or self.playing or self.draging:
            return
        self.contenting = True
        menu = QMenu(self)
        ability = Ability(self)

        wechat = menu.addAction("打开微信")
        wechat.triggered.connect(ability.openWechat)
        wechat.setIcon(QIcon(str(self.imgDir / settings.WECHAT)))

        fall = menu.addAction("关闭自由落体" if self.autoFalling else "开启自由落体")
        fall.triggered.connect(ability.fall)
        fall.setIcon(QIcon(str(self.imgDir / settings.FALL)))

        close = menu.addAction("退出")
        close.triggered.connect(self.close)
        close.setIcon(QIcon(str(self.imgDir / settings.EXIT)))

        menu.exec_(e.globalPos())
        self.contenting = False

    def paintEvent(self, QPaintEvent):
        """绘图"""
        painter = QPainter(self)
        if hasattr(self, "pix"):
            painter.drawPixmap(self.rect(), self.pix)

    def setPix(self, pix):
        """设置帧"""
        if isinstance(pix, QPixmap):
            self.pix = pix
        else:
            self.pix = QPixmap(pix)
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())
        self.update()

    def startMovie(self):
        """定义定时器,通过定时器完成动画功能"""
        self.allActions = Action().getAllAction()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.action)
        self.timer.start(settings.MOVIE_TIME_INTERVAL * 1000)

    def action(self):
        """加载动作"""
        if self.draging or self.walking or self.contenting:
            return
        self.timer.stop()
        self.playing = True
        currentMovie = random.choice(self.allActions)
        for i in range(len(currentMovie)):
            pix = currentMovie[i]
            self.setPix(pix)
            QApplication.processEvents()
            time.sleep(0.5)
        self.timer.start()
        self.playing = False
        self.setPix(str(self.imgDir / settings.INIT_PICTURE))

    def welcomePage(self):
        """欢迎页面"""
        self.fallingBody(self.desktop.availableGeometry().bottomRight().x() - 300, 0)

    def walk(self):
        """桌宠 走路"""
        walk = settings.WALK
        i = 0
        while self.walking is True:
            self.move(self.pos().x() - 5, self.pos().y())
            if self.pos().x() < -128:
                self.move(
                    self.desktop.availableGeometry().bottomRight().x() - 50,
                    self.pos().y(),
                )
            self.setPix(str(self.imgDir / walk[i]))
            QApplication.processEvents()
            time.sleep(0.5)
            if i == 1:
                i = 0
            else:
                i += 1

    def fallingBody(self, posX, posY):
        """宠物自由落体, posX, posY 是起始的位置"""
        rect = self.desktop.availableGeometry()
        while self.pos().y() < rect.height() - 200:
            self.move(posX, posY)
            self.setPix(str(self.imgDir / "shime4.png"))
            QApplication.processEvents()
            time.sleep(0.01)
            posY += 10
        self.setPix(str(self.imgDir / settings.INIT_PICTURE))


class Action(object):
    """动作类, 读取action.py下的列表, 去img文件下下寻找对应的图片"""

    def __init__(self):
        self.imgDir = settings.SETUP_DIR / "img"
        self.actionList = []
        self.picturesList = []

    def createPicture(self):
        """读取图片"""
        module = action
        for i in dir(module):
            if i.startswith("__"):
                continue
            pictures = getattr(module, i)
            self.picturesList.append(pictures)

    def createQpixmap(self):
        """将图片转成Pixmap"""
        for indexI, i in enumerate(self.picturesList):
            for indexJ, j in enumerate(i):
                self.picturesList[indexI][indexJ] = QPixmap(str(self.imgDir / j))

    def getAllAction(self):
        """获取所有的动作集, 返回嵌套列表"""
        self.createPicture()
        self.createQpixmap()
        return self.picturesList
