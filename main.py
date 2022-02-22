import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox

from gui import Ui_DynamicBackground

Ui_Triangle_Plain, _ = uic.loadUiType("gui/triangle_plain_color.ui")
Ui_Triangle_Linear, _ = uic.loadUiType("gui/triangle_linear_gradient.ui")
Ui_Triangle_Exponential, _ = uic.loadUiType("gui/triangle_exponential_gradient.ui")
Ui_Triangle_Discrete, _ = uic.loadUiType("gui/triangle_discrete_gradient.ui")

class Window(QMainWindow, Ui_DynamicBackground):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.triangle_choose_ui(0)
        self.triangle_type_combo_box.currentIndexChanged.connect(self.triangle_choose_ui)

    def triangle_choose_ui(self, index):
        if index == 0:
            self.triangle_ui = Ui_Triangle_Plain()
        elif index == 1:
            self.triangle_ui = Ui_Triangle_Linear()
        elif index == 2:
            self.triangle_ui = Ui_Triangle_Exponential()
        elif index == 3:
            self.triangle_ui = Ui_Triangle_Discrete()
        self.triangle_ui.setupUi(self.triangle_args)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
