import sys

from PyQt5.QtWidgets import QApplication

from core.daemon import daemonize
from core.pets import DesktopPet

if __name__ == '__main__':
    argv = sys.argv
    if "--daemon" in argv:
        daemonize()
    if "--tray" in argv:
        tray = True
    else:
        tray = False
    app = QApplication(argv)
    pet = DesktopPet(tray=tray)
    pet.show()
    pet.welcomePage()
    sys.exit(app.exec())

