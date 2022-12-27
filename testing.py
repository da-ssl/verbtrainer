from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

class MenuButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Erstelle ein QMenu-Objekt und füge Einträge hinzu
        menu = QMenu(self)
        for i in range(5):
            menu.addAction(f'Eintrag {i+1}')
        
        # Weise das QMenu dem Button mit der Methode setMenu zu
        self.setMenu(menu)

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.menubutton = MenuButton()
        self.setCentralWidget(self.menubutton)
        self.show()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()