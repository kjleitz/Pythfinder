import sys
import PyQt5.QtWidgets as q
from character import Character
from featspage import FeatsPage
from featspagecsv import FeatsPageCSV
from charpage import CharPage
import os


class TabbedUI(q.QTabWidget):

    def __init__(self, char=Character()):
        self.char = char
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTabShape(q.QTabWidget.Rounded)

        chartab = CharPage(self.char)
        featstab1 = FeatsPage(self.char)
        featstab2 = FeatsPageCSV(self.char)

        self.addTab(chartab, "Character")
        self.addTab(featstab1, "Feats (sqlite3)")
        self.addTab(featstab2, "Feats (csv)")

        self.setGeometry(300, 100, 600, 600)
        self.setWindowTitle("PythFinder v0.1")


if __name__ == "__main__":
    app = q.QApplication(sys.argv)
    banjo = Character("Banjo", "Human", "Fighter")
    # banjo.add_feat("Power Attack")
    # banjo.add_feat("Point-Blank Shot")
    tUI = TabbedUI(banjo)
    tUI.show()
    sys.exit(app.exec_())
