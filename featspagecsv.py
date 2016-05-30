import sys
import PyQt5.QtWidgets as q
from character import Character
import sqlite3
from PFSRDScraper.pfsrdscraper import OGLFeatsTable

class FeatsPageCSV(q.QWidget):

    def __init__(self, char=Character()):
        super().__init__()
        self.char = char
        self.initUI()

    def initUI(self):

        # This gives you access to the feats table
        self.featsdb = OGLFeatsTable()

        # These are the description labels of the feat
        self.namelbl = q.QLabel("Name : [no known feat name]")
        self.typelbl = q.QLabel("Type: [no known feat type]")
        self.desclbl = q.QLabel("Description: \n[no known feat description]")
        self.prereqblbl = q.QLabel("Prerequisites (basic): \n[no known feat prerequisites (basic)]")
        self.prereqflbl = q.QLabel("Prerequisites (feats): \n[no known feat prerequisites (feats)]")
        self.benefitslbl = q.QLabel("Explicit benefits: \n[no known feat 'benefits']")
        self.normallbl = q.QLabel("Normal behavior: \n[no known 'normal behavior']")
        self.extrainfolbl = q.QLabel("Extra info: \n[no known 'extra info']")
        self.sourcelbl = q.QLabel("Source: [no known feat source]")

        self.desclbl.setWordWrap(True)
        self.prereqblbl.setWordWrap(True)
        self.prereqflbl.setWordWrap(True)
        self.benefitslbl.setWordWrap(True)
        self.normallbl.setWordWrap(True)
        self.extrainfolbl.setWordWrap(True)

        # Push this button to take this feat and apply it to your character
        applybutton = q.QPushButton("Apply feat")

        # TODO: make this a scrollable list where you have the name in bold
        # above a greyed out/italicized description, so you can browse & click.
        # Adding a drop-down box for feat selection
        featnamelist = self.featsdb.get_feat_names()
        self.featsdropdown = q.QComboBox(self)
        self.featsdropdown.addItems(featnamelist)

        featselectbox = q.QHBoxLayout()
        featselectbox.addWidget(self.featsdropdown, 1)
        featselectbox.addWidget(applybutton)

        # TODO: Get this fucker to stop resizing every goddamn time you
        # select a new goddamn feat.
        leftbox = q.QVBoxLayout()
        leftbox.addWidget(self.namelbl)
        leftbox.addWidget(self.typelbl)
        leftbox.addWidget(self.desclbl)
        leftbox.addWidget(self.prereqblbl)
        leftbox.addWidget(self.prereqflbl)
        leftbox.addWidget(self.benefitslbl)
        leftbox.addWidget(self.normallbl)
        leftbox.addWidget(self.extrainfolbl)
        leftbox.addWidget(self.sourcelbl)
        leftbox.addStretch()
        leftbox.addLayout(featselectbox)

        # TODO: Remove this example feat list
        for i in range(30):
            self.char.add_feat("Example Feat {0}".format(i))

        self.show_feat_info(self.featsdropdown.currentText())

        self.featSA = FeatScrollArea(self.char)

        featscrollbox = q.QVBoxLayout()
        featscrollbox.addWidget(self.featSA)

        hbox = q.QHBoxLayout()
        hbox.addLayout(leftbox)
        hbox.addLayout(featscrollbox)

        self.setLayout(hbox)

        # Button and dropdown logic
        self.featsdropdown.activated[str].connect(self.show_feat_info)
        applybutton.pressed.connect(self.applyFeat)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Feats Page")


    def fetch_feat_names(self):
        conn = sqlite3.connect(self.featsdb.featsFile)
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM feats")
        fetch = cur.fetchall()
        conn.close()

        return fetch

    def show_feat_info(self, featname):
        # The dropdown signal can be taken as an argument to the slot, I guess

        fd = self.featsdb.get_feat_dict(featname)
        if fd["name"] != "":
            self.namelbl.setText("Name: " + fd["name"])
        if fd["type"] != "":
            self.typelbl.setText("Type: " + fd["type"])
        if fd["desc"] != "":
            self.desclbl.setText("Description: \n" + fd["desc"])
        if fd["prereq_b"] != "":
            self.prereqblbl.setText("Prerequisites (basic): \n" + fd["prereq_b"])
        if fd["prereq_f"] != "":
            self.prereqflbl.setText("Prerequisites (feats): \n" + fd["prereq_f"])
        if fd["benefits"] != "":
            self.benefitslbl.setText("Explicit benefits: \n" + fd["benefits"])
        if fd["normal"] != "":
            self.normallbl.setText("Normal behavior: \n" + fd["normal"])
        if fd["extra_info"] != "":
            self.extrainfolbl.setText("Extra info: \n" + fd["extra_info"])
        if fd["source"] != "":
            self.sourcelbl.setText("Source: " + fd["source"])


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
    fp = FeatsPageCSV(banjo)
    fp.show()
    sys.exit(app.exec_())
