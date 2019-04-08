import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QMovie
import res_rc

(form_class, qtbase_class) = uic.loadUiType('Function.ui')

class MainWindow(qtbase_class, form_class):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        move = QMovie('image/auto.gif')
        self.picLeft.setMovie(move)
        self.picRight.setMovie(move)
        move.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
