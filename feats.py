import sqlite3


class FeatsTable():

    def __init__(self, featsFile="feats.db"):
        self.featsFile = featsFile
        self.createFeatsTable()

    def createFeatsTable(self):
        conn = sqlite3.connect(self.featsFile)
        conn.execute('''CREATE TABLE IF NOT EXISTS Feats (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, DESCRIPTION TEXT NOT NULL);''')
        conn.commit()
        conn.close()

    def add_feat(self, feat, desc):
        conn = sqlite3.connect(self.featsFile)
        c = conn.cursor()

        c.execute("SELECT * FROM Feats")
        currentLength = len(c.fetchall())
        c.execute("INSERT INTO feats VALUES (?, ?, ?);", (currentLength + 1, feat, desc))

        print("\nAdding feat...\nFeats currently consist of:")
        for row in c.execute("SELECT * FROM Feats;"):
            print(row)

        # c.execute("SELECT * FROM Feats;")
        # print(len(c.fetchall()))

        conn.commit()
        conn.close()

    def clearFeats(self):
        conn = sqlite3.connect(self.featsFile)
        conn.execute("DROP TABLE Feats")
        conn.execute('''CREATE TABLE Feats (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, DESCRIPTION TEXT NOT NULL);''')
        conn.commit()
        conn.close()
