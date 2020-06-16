import os
import subprocess

from PyQt5.QtCore import QThread


class Ability(object):
    def __init__(self, pet):
        self.pet = pet
        self.system = os.name

    def fall(self):
        if self.pet.sender().text() == "开启自由落体":
            self.pet.autoFalling = True
            self.pet.sender().setText("关闭自由落体")

        elif self.pet.sender().text() == "关闭自由落体":
            self.pet.autoFalling = False
            self.pet.sender().setText("开启自由落体")

    def openWechat(self):
        if self.system == "posix":
            self.pet.thread = Thread(app="wechat")
            self.pet.thread.start()

class Thread(QThread):
    def __init__(self, app=None):
        super(Thread, self).__init__()
        self.app = app

    def run(self):
        if self.app == "wechat":
            subprocess.call(["nohup", "/Applications/WeChat.app/Contents/MacOS/WeChat", "&&", "exit"])
