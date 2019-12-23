import importlib
import os
import random
import sys
import time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QWidget, QMenu, qApp, QApplication, QSystemTrayIcon

from conf import settings


class newWindow(QWidget):
    def __init__(self, parent=None):
        super(newWindow, self).__init__(parent)
        self.setMouseTracking(False)  # 设置鼠标移动跟踪是否有效
        self.runing = False
        self.busy = False
        self.initUI()
        self.startMovie()
        self.trayMenu()   # 系统托盘
        self.hide()

    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件
        self.hide()  # 隐藏窗体

    def trayMenu(self):
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(settings.TRAY_ICON))
        tray.show()

    def initUI(self):
        self.setWindowIcon(QIcon(settings.ICON))
        self.welcomePage()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明

    def startMovie(self):
        self.allActions = Action().getAllAction()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.action)
        self.timer.start(settings.MOVIE_TIME_INTERVAL * 1000)

    def action(self):
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
        self.setPix(settings.INIT_PICTURE)

    def welcomePage(self):
        self.desktop = QApplication.desktop()
        rect = self.desktop.availableGeometry()
        self.move(rect.right()-200, rect.height()-200)
        self.setPix(settings.INIT_PICTURE)

    def mousePressEvent(self, event):
        if self.busy:
            return
        if event.button() == Qt.LeftButton:
            self.runing = False     # 单击 关闭跑步
            self.busy = True
            self.mDragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.runing is False:
            self.setPix(settings.INIT_PICTURE)
            self.busy = False

    def mouseMoveEvent(self, event):  # 鼠标键移动时调用
        if Qt.LeftButton:
            self.move(event.globalPos() - self.mDragPosition)
            moveDistance = (self.mDragPosition - event.pos()).x()
            if -1 <= moveDistance < 0:
                self.setPix(settings.MOUSE_TO_RIGHT_1)
            elif -2 <= moveDistance < -1:
                self.setPix(settings.MOUSE_TO_RIGHT_2)
            elif moveDistance < -2:
                self.setPix(settings.MOUSE_TO_RIGHT_3)

            elif 0 < moveDistance <= 1:
                self.setPix(settings.MOUSE_TO_LEFT_1)
            elif 1 < moveDistance <= 2:
                self.setPix(settings.MOUSE_TO_LEFT_2)
            elif 2 < moveDistance:
                self.setPix(settings.MOUSE_TO_LEFT_3)

    def mouseDoubleClickEvent(self, QMouseEvent):
        if self.busy:
            return
        if Qt.LeftButton == QMouseEvent.button():
            self.runing = True
            self.run()


    def run(self):

        walk = settings.WALK
        i = 0
        while self.runing is True:
            self.move(self.pos().x() - 5, self.pos().y())
            if self.pos().x() < -100:
                self.move(self.desktop.availableGeometry().bottomRight().x(), self.pos().y())
            self.setPix(walk[i])
            QApplication.processEvents()
            time.sleep(0.5)
            if i == 1:
                i = 0
            else:
                i += 1

    def contextMenuEvent(self, e):
        """右键菜单"""
        cmenu = QMenu(self)
        act4 = cmenu.addAction("关机")
        act5 = cmenu.addAction("退出")
        act6 = cmenu.addAction("待续")
        action = cmenu.exec_(self.mapToGlobal(e.pos()))
        if action == act5:
            qApp.quit()
        elif action == act4:
            os.system("shutdown -p")
        elif action == act6:
            self.parent_window.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing, True)
        if hasattr(self, "pix"):
            painter.drawPixmap(self.rect(), self.pix)

    def setPix(self, pix):
        if isinstance(pix, QPixmap):
            self.pix = pix
        else:
            self.pix = QPixmap(pix)
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())
        self.update()


class Action(object):
    def __init__(self):
        self.imgDir = "./img"
        self.actionList = []
        self.picturesList = []

    def createPicture(self):
        module = importlib.import_module("action")
        for i in dir(module):
            if i.startswith("__"):
                continue
            pictures = getattr(module, i)
            self.picturesList.append(pictures)

    def createQpixmap(self):
        for indexI, i in enumerate(self.picturesList):
            for indexJ, j in enumerate(i):
                self.picturesList[indexI][indexJ] = QPixmap(f"{self.imgDir}/{j}")

    def getAllAction(self):
        self.createPicture()
        self.createQpixmap()
        return self.picturesList


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = newWindow()
    demo.show()
    sys.exit(app.exec())


