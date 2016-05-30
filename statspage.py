import sys
import PyQt5.QtWidgets as q
from character import Character

'''
Graphical:
hbox (hp, hit dice[char.class_], roll button, current hp, nonlethal,
        damage reduction)
hbox (ac, armor[char.armor], shield[char.armor], dex[char.abilityscores],
        dodge[char.feats?], size[char.size], natural[not sure],
        deflect [not sure], misc[not sure], info button)
vbox (hbox ())

Logic:
- Hit dice derived from char

'''
class StatsPage(q.QWidget):

    def __init__(self, char=Character()):
        super().__init__()
        self.char = char
        self.initUI()

    def initUI(self):
        # Labels go here!
        namelbl  = q.QLabel("Name: ")
        racelbl  = q.QLabel("Race: ")
        classlbl = q.QLabel("Class: ")
        lvllbl   = q.QLabel("Level: ")
        self.desclbl = q.QLabel(self.char.get_desc())
        strlbl = q.QLabel("STR ")
        dexlbl = q.QLabel("DEX ")
        conlbl = q.QLabel("CON ")
        intlbl = q.QLabel("INT ")
        wislbl = q.QLabel("WIS ")
        chalbl = q.QLabel("CHA ")

        # Edit boxes go here!
        nameedit  = q.QLineEdit()
        raceedit  = q.QLineEdit()
        classedit = q.QLineEdit()
        stredit   = q.QLineEdit()
        conedit   = q.QLineEdit()
        dexedit   = q.QLineEdit()
        intedit   = q.QLineEdit()
        wisedit   = q.QLineEdit()
        chaedit   = q.QLineEdit()

        # Miscellaneous unitary widgets go here!
        self.lvllcd = q.QLCDNumber()
        lvlbtn = q.QPushButton("Level up!")

        # VBoxLayout/HBoxLayout version:

        # nameBox  = QHBoxLayout()
        # raceBox  = QHBoxLayout()
        # classBox = QHBoxLayout()
        # descBox  = QHBoxLayout()
        #
        # vbox = QVBoxLayout()
        #
        # nameBox.addWidget(namelbl)
        # nameBox.addWidget(nameedit)
        # nameBox.addStretch(1)
        #
        # raceBox.addWidget(racelbl)
        # raceBox.addWidget(raceedit)
        # raceBox.addStretch(1)
        #
        # classBox.addWidget(classlbl)
        # classBox.addWidget(classedit)
        # classBox.addStretch(1)
        #
        # descBox.addWidget(self.desclbl)
        #
        #
        # vbox.addLayout(nameBox)
        # vbox.addLayout(raceBox)
        # vbox.addLayout(classBox)
        # vbox.addLayout(descBox)
        #
        #
        # self.setLayout(vbox)


        # Grid layout version:

        grid = q.QGridLayout()

        grid.addWidget(namelbl,  1, 1);    grid.addWidget(nameedit,  1, 2);    grid.setColumnStretch(3, 1)
        grid.addWidget(racelbl,  2, 1);    grid.addWidget(raceedit,  2, 2);    #grid.addWidget(raceedit,  2, 3)
        grid.addWidget(classlbl, 3, 1);    grid.addWidget(classedit, 3, 2);    #grid.addWidget(classedit, 3, 3)

        grid.addWidget(strlbl,   5, 1);    grid.addWidget(stredit,   5, 2);    #grid.addWidget(stredit,   5, 3)
        grid.addWidget(dexlbl,   6, 1);    grid.addWidget(dexedit,   6, 2);    #grid.addWidget(dexedit,   6, 3)
        grid.addWidget(conlbl,   7, 1);    grid.addWidget(conedit,   7, 2);    #grid.addWidget(conedit,   7, 3)
        grid.addWidget(intlbl,   8, 1);    grid.addWidget(intedit,   8, 2);    #grid.addWidget(intedit,   8, 3)
        grid.addWidget(wislbl,   9, 1);    grid.addWidget(wisedit,   9, 2);    #grid.addWidget(wisedit,   9, 3)
        grid.addWidget(chalbl,  10, 1);    grid.addWidget(chaedit,  10, 2);    #grid.addWidget(chaedit,  10, 3)

        grid.addWidget(self.desclbl, 12, 1, 1, 3)

        self.setLayout(grid)

        nameedit.setText(self.char.name)
        raceedit.setText(self.char.race)
        classedit.setText(self.char.class_)

        # Interaction goes here!
        nameedit.textChanged.connect(self.add_name)
        raceedit.textChanged.connect(self.add_race)
        classedit.textChanged.connect(self.add_class)
        lvlbtn.clicked.connect(self.level_up)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Char Page")

    def level_up(self):
        self.char.level_up()
        self.desclbl.setText(self.char.get_desc())
        self.lvllcd.display(self.char.level)

    def add_name(self):
        sender = self.sender()
        text = sender.text()
        self.char.name = text
        self.desclbl.setText(self.char.get_desc())

    def add_race(self):
        sender = self.sender()
        text = sender.text()
        self.char.race = text
        self.desclbl.setText(self.char.get_desc())

    def add_class(self):
        sender = self.sender()
        text = sender.text()
        self.char.class_ = text
        self.desclbl.setText(self.char.get_desc())


if __name__ == "__main__":
    app = q.QApplication(sys.argv)
    banjo = Character("Banjo", "Human", "Fighter")
    # banjo.add_feat("Power Attack")
    # banjo.add_feat("Point-Blank Shot")
    cp = CharPage(banjo)
    cp.show()
    sys.exit(app.exec_())
