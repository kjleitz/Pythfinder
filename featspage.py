import sys
import PyQt5.QtWidgets as q
from character import Character
from feats import FeatsTable
import sqlite3

class FeatsPage(q.QWidget):

    def __init__(self, char=Character()):
        super().__init__()
        self.char = char
        self.initUI()

    def initUI(self):

        # This gives you access to the feats table
        self.featsdb = FeatsTable()

        # This is the description of the feat
        self.featslbl = q.QLabel("[feat description]")
        self.featslbl.setWordWrap(True)

        # Push this button to take this feat and apply it to your character
        applybutton = q.QPushButton("Apply feat")

        # Adding a drop-down box for feat selection
        fetch = self.fetch_feat_names()
        self.featsdropdown = q.QComboBox(self)
        featslist = []
        for row in fetch:
            featslist.append(row[0])
        self.featsdropdown.addItems(featslist)

        featselectbox = q.QHBoxLayout()
        featselectbox.addWidget(self.featsdropdown, 1)
        featselectbox.addWidget(applybutton)

        leftbox = q.QVBoxLayout()
        leftbox.addStretch()
        leftbox.addWidget(self.featslbl)
        leftbox.addLayout(featselectbox)

        # TODO: Remove this example feat list
        for i in range(30):
            self.char.add_feat("Example Feat {0}".format(i))

        self.show_feat_desc(self.featsdropdown.currentText())

        self.featSA = FeatScrollArea(self.char)

        featscrollbox = q.QVBoxLayout()
        featscrollbox.addWidget(self.featSA)

        hbox = q.QHBoxLayout()
        hbox.addLayout(leftbox)
        hbox.addStretch()
        hbox.addLayout(featscrollbox)

        self.setLayout(hbox)

        # Button and dropdown logic
        self.featsdropdown.activated[str].connect(self.show_feat_desc)
        applybutton.pressed.connect(self.applyFeat)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Feats Page")

    def fetch_feat_names(self):

        self.featsdb.clearFeats()
        # for testing
        self.featsdb.add_feat("Power Attack", "-1 to attack for +1 to hit.")
        self.featsdb.add_feat("Cleave", "Follow through to another enemy, -1 to AC next turn.")

        conn = sqlite3.connect(self.featsdb.featsFile)
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM feats")
        fetch = cur.fetchall()
        conn.close()

        return fetch

    def show_feat_desc(self, text):
        # The dropdown signal can be taken as an argument to the slot, I guess
        name = text

        # Connect to the feats database
        conn = sqlite3.connect(self.featsdb.featsFile)
        cur = conn.cursor()

        # Grab the description (if you end up using this function to fill in other info from the
        # row, do "SELECT * FROM feats WHERE NAME LIKE (?)", (name,) and then use desc[0-9] or
        # whatever to grab the relevant item from the row. I think it may work as a dictionary
        # possibly...? where you could specify desc["DESCRIPTION"], but I'll have to play around
        # with it. Update: doesn't work like that, but that functionality might be somewhere else.
        cur.execute("SELECT DESCRIPTION FROM feats WHERE NAME LIKE (?)", (name,))
        desc = cur.fetchone()
        print("\n"+desc[0])
        conn.close()
        self.featslbl.setText(desc[0])  # NEED TO SET FROM featsDB.db WHERE NAME = TEXT FROM DROPDOWN

    def applyFeat(self):

        featname = self.featsdropdown.currentText()
        print(featname, self.char.feats)

        if featname not in self.char.feats:
            add = q.QMessageBox.question(self, "Apply feat?", "Add {fn} to your feats?".format(fn=featname),
                                       q.QMessageBox.Yes | q.QMessageBox.No, q.QMessageBox.Yes)
            if add == q.QMessageBox.Yes:
                self.char.add_feat(featname)
                self.featSA.add_feat(featname)
        elif featname in self.char.feats:
            q.QMessageBox.critical(self, "Feat Found!", "{cn} already knows {fn}.".format(cn=self.char.name, fn=featname))


class FeatScrollArea(q.QScrollArea):

    def __init__(self, char):
        super().__init__()
        self.char = char
        self.initUI()

    def initUI(self):
        # Make a list of QLabels for easy addition to the list
        featlbllist = []
        for f in self.char.feats:
            flbl = q.QLabel(f)
            featlbllist.append(flbl)

        # Make a vertical box layout containing your QLabels
        self.vbox = q.QVBoxLayout()
        for lbl in featlbllist:
            self.vbox.addWidget(lbl)

        # Create a widget to set to your scroll area. Think of this widget as a
        # standalone window with a vbox that is a list of QLabels.
        # Docs say you have to set the layout of the widget before setting the
        # widget in the scroll area or it won't show up
        scrollwidget = q.QWidget()
        scrollwidget.setLayout(self.vbox)

        '''
        Set self (scroll area) to the widget containing the list of QLabels;
        basically, as far as I understand it, this wraps the widget in the
        scroll area (self), and now self is essentially the widget,
        just scrollable. Use .setWidgetResizable = True so the labels
        are able to be added and continue to scroll rather than make them
        all squeeze together (It's weird: you have a scroll area that is
        over-populated so it puts a scroll bar there, and it looks normal
        and scrolls fine, but then when you add stuff to it it squeezes them
        together vertically, and you can still scroll, just the same, like,
        "interior size" as before. If you set it to True, it acts like you
        would expect it to, increasing the "interior size", not squeezing
        the labels together for space.)
        '''
        self.setWidget(scrollwidget)
        self.setWidgetResizable(True)

        self.setGeometry(200, 200, 500, 500)

    # This gives the ability to add a QLabel to the top of the list in this
    # scroll widget, even after an instance of this scroll widget has been
    # called and set up and shown on the screen.
    def add_feat(self, featname):
        newfeat = q.QLabel(featname)
        self.vbox.insertWidget(0, newfeat)


if __name__ == "__main__":
    app = q.QApplication(sys.argv)
    banjo = Character("Banjo", "Human", "Fighter")
    # banjo.add_feat("Power Attack")
    # banjo.add_feat("Point-Blank Shot")
    fp = FeatsPage(banjo)
    fp.show()
    sys.exit(app.exec_())
