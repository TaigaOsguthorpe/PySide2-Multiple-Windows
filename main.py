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

        # When the "new_window_button" is clicked fire off the function "new_image_window"
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
        # Clean the window_list to free up a tiny bit of memory that does not need to be used.
        self.clean()

        # Create the new window itself via the ImageWindow class
        w = ImageWindow(self)

        # Keep the window in reference so that Garbadge Collection does not snap it up and remove it.
        self.window_list.append({"mem_adress": w, "del": False})

        # Render the new window on screen
        w.show()
        print("new_image_window: END")

    def closeEvent(self, event):
        # Capture the close event of the main window and quit the aplication, forcing all other windows to close with it and free up their used memory.
        # This event capture ("closeEvent") can be removed and allow each new window to act semi independantly but this could cause unknown errors to ocour.
        app.quit()



class ImageWindow(QMainWindow):
#class ImageWindow(MainWindow):
    def __init__(self, parent):
        # inherit all the things a QMainWindow can do.
        # This in its current form also has the side effect of the main window not truly being a main window meaning that all windows created (this one)
        # from it act as independant windows, this has its ups and downs but for now we are going to ignore it as you will see no differnece right now,
        # but just keep this in mind.
        super(ImageWindow, self).__init__()

        # WA_DeleteOnClose means that this window's memory shall be removed when it is exited even if the main window of our gui is not.
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui = Ui_ImageWindow()
        self.ui.setupUi(self)

        # (currently a placeholder of doing it in a differnet way)
        # reference our parent window to be able to acess the list to remove the one reference keeping this window alive and safe from Garbadge Collection
        self.parent = parent

        # Image setup
        file = "{0}/a.tif".format(Path(__file__).parent.absolute())
        self.ui.image_label.setPixmap(QPixmap(file).scaled(1024, 1024, QtCore.Qt.KeepAspectRatio))

    def closeEvent(self, event):
        # Capture the close event and remove ourself from the parent's window_list
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
    # Run the aplication
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Start the main loop of the program
    sys.exit(app.exec_())
