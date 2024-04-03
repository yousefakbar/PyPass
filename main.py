from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import PyPassUI
import sys

def main():
    app = QApplication(sys.argv)

    win = QMainWindow()
    gui = PyPassUI(win)
    win.show()

    sys.exit(app.exec_())

main()
