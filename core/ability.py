from time import sleep

import pexpect
import os
import subprocess

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QInputDialog


class Ability(object):
    def __init__(self, pet):
        self.pet = pet
        self.system = os.name

    def shutdown(self):
        reply = QMessageBox.information(self.pet, 'shutdown', 'shutdown. Are you sure?',
                                     QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            if self.system == "posix":
                password, status = QInputDialog.getText(self.pet, "input password", "password")
                if not status:
                    return
                child = pexpect.spawn("sudo shutdown -h now")
                child.expect("Password")
                child.sendline(password)
            elif self.system == "nt":
                pexpect.spawn("sudo shutdown -s -t 0")

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

    def calculator(self):
        if self.system == "posix":
            self.pet.thread = Thread(app="calculator")
            self.pet.thread.start()


class Thread(QThread):
    def __init__(self, app=None):
        super(Thread, self).__init__()
        self.app = app

    def run(self):
        if self.app == "wechat":
            subprocess.call(["nohup", "/Applications/WeChat.app/Contents/MacOS/WeChat", "&&", "exit"])
        elif self.app == "calculator":
            subprocess.call(["nohup", "/Applications/Calculator.app/Contents/MacOS/Calculator", "&&", "exit"])
