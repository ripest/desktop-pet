import pexpect
import os
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

