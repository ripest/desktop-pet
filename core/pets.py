import random
import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QMenu, QApplication, QSystemTrayIcon

from core import action
from core.ability import Ability
from core.conf import settings


class DesktopPet(QWidget):
    """桌宠核心类"""
    def __init__(self, parent=None, tray=False):
        super(DesktopPet, self).__init__(parent)
        self.imgDir = settings.SETUP_DIR / "img"
        self.walking = False
        self.busy = False
        self.initUI()
        self.startMovie()
        if tray:
            self.trayMenu()   # 系统托盘

    def trayMenu(self):
        """显示系统托盘"""
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(str(self.imgDir / settings.TRAY_ICON)))
        tray.show()

    def initUI(self):
        """初始化窗口"""
        self.setWindowIcon(QIcon(str(self.imgDir / settings.ICON)))
        self.desktop = QApplication.desktop()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明

        self.welcomePage()

    def startMovie(self):
        """定义定时器,通过定时器完成动画功能"""
        self.allActions = Action().getAllAction()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.action)
        self.timer.start(settings.MOVIE_TIME_INTERVAL * 1000)

    def action(self):
        """加载动作"""
        if self.busy:
            return
        self.timer.stop()
        self.busy = True
        currentMovie = random.choice(self.allActions)
        for i in range(len(currentMovie)):
            pix = currentMovie[i]
            self.setPix(pix)
            QApplication.processEvents()
            time.sleep(0.5)
        self.timer.start()
        self.busy = False
        self.setPix(str(self.imgDir / settings.INIT_PICTURE))

    def welcomePage(self):
        """开始"""
        rect = self.desktop.availableGeometry()
        self.move(rect.right()-200, rect.height()-200)
        self.setPix(str(self.imgDir / settings.INIT_PICTURE))

    def mousePressEvent(self, event):
        """鼠标单击事件"""
        if self.busy:
            return
        if event.button() == Qt.LeftButton:
            self.walking = False     # 单击 关闭跑步
            self.busy = True
            self.mDragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if self.walking is False:
            self.setPix(str(self.imgDir / settings.INIT_PICTURE))
            self.busy = False

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
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
        if self.busy:
            return
        if Qt.LeftButton == QMouseEvent.button():
            self.walking = True
            self.walk()

    def closeEvent(self, QCloseEvent):
        """关闭事件"""
        #  如何在walk 的时候关闭, 会导致程序坞的图标不消失,所以要先停掉walk
        self.walking = False

    def walk(self):
        """桌宠 走路"""
        walk = settings.WALK
        i = 0
        while self.walking is True:
            self.move(self.pos().x() - 5, self.pos().y())
            if self.pos().x() < -100:
                self.move(self.desktop.availableGeometry().bottomRight().x(), self.pos().y())
            self.setPix(str(self.imgDir / walk[i]))
            QApplication.processEvents()
            time.sleep(0.5)
            if i == 1:
                i = 0
            else:
                i += 1

    def contextMenuEvent(self, e):
        """右键菜单"""
        cmenu = QMenu(self)
        ability = Ability(self)
        act4 = cmenu.addAction("关机")
        act5 = cmenu.addAction("退出")
        action = cmenu.exec_(self.mapToGlobal(e.pos()))
        if action == act5:
            self.close()
        elif action == act4:
            ability.shutdown()

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


