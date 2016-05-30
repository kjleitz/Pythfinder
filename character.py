class Character:

    def __init__(self, name="", race="", class_=""):
        self.name = name
        self.race = race
        self.class_ = class_

        self.abilityscores = {}
        self.level = 0
        self.feats = []
        self.skills = {}

    def get_desc(self):
        description = self.name + ", " + self.race + " " + self.class_ + ". Level: " + str(self.level)
        return description

    def level_up(self, inc=1):
        self.level += inc
        print(self.level)

    def add_feat(self, feat):
        self.feats.append(feat)

    def inc_skill(self, skill: str, inc=1):
        self.skills[skill] += inc

    def get_feats(self):
        return self.feats
