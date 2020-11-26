import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from ui_files.main_gui import Ui_MainWindow
from ui_files.image_window_gui import Ui_MainWindow as Ui_ImageWindow
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.new_window_button.clicked.connect(self.new_image_window)

        self.window_list = []

    def clean(self):
        print("clean: START")

        cleaned = 0
        for item in self.window_list:
            if item["del"] == True:
                print("FOUND TRUE!")
                #print(type(item["mem_adress"]))
                #print(item["mem_adress"])
                #del item["mem_adress"]
                self.window_list.remove(item)
                cleaned = cleaned + 1
            else:
                pass

        print("clean: cleaned {0} windows".format(cleaned))
        print("clean: END")


    def new_image_window(self):
        print("new_image_window: START")
        self.clean()
        w = ImageWindow(self)
        self.window_list.append({"mem_adress": w, "del": False})
        w.show()
        print("new_image_window: END")



class ImageWindow(QMainWindow):
    def __init__(self, parent):
        super(ImageWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = Ui_ImageWindow()
        self.ui.setupUi(self)

        self.parent = parent

        # Image setup
        file = "{0}/a.tif".format(Path(__file__).parent.absolute())
        self.ui.image_label.setPixmap(QPixmap(file).scaled(1024, 1024, QtCore.Qt.KeepAspectRatio))

    def closeEvent(self, event):
        print("closEvent detected")
        print(self.parent.window_list)
        for item in self.parent.window_list:
            print(item)
            print(item["mem_adress"])
            print(self)
            if item["mem_adress"] == self:
                print("FOUND SELF!")
                item.update({"del": True})
            else:
                pass
        event.accept()
        print("closEvent accepted")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
