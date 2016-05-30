import csv
import os


FEATS_OGL ="PFSRDScraper/feats_ogl.csv"

class OGLFeatsTable:

    def __init__(self):
        self.featsfile = FEATS_OGL

    def get_feat_names(self):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)
            featnamelist = []
            for row in reader:
                featnamelist.append(row["name"])
            return featnamelist

    def get_feat_desc(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["description"]
            return "Feat not found."

    def get_feat_type(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["type"]
            return "Feat not found."

    def get_feat_basic_prereq(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["prerequisites"]
            return "Feat not found."

    def get_feat_feats_prereq(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["prerequisite_feats"]
            return "Feat not found."

    def get_feat_benefits(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["benefit"]
            return "Feat not found."

    def get_feat_normal(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["normal"]
            return "Feat not found."

    def get_feat_extra_info(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["special"]
            return "Feat not found."

    def get_feat_source(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["source"]
            return "Feat not found."

    def get_feat_link(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    return row["fulltext"]
            return "Feat not found."

    def get_feat_dict(self, featname):
        with open(self.featsfile, "r") as f:
            # Turns out, csv.DictReader will use the first line of the csv as
            # the fieldnames by default, so this is simple
            reader = csv.DictReader(f)

            for row in reader:
                if row["name"] == featname:
                    featdict = {"name": row["name"],
                                "type": row["type"],
                                "desc": row["description"],
                                "prereq_b": row["prerequisites"],
                                "prereq_f": row["prerequisite_feats"],
                                "benefits": row["benefit"],
                                "normal": row["normal"],
                                "extra_info": row["special"],
                                "source": row["source"],
                                "link": row["fulltext"]}
                    return featdict
            return "Feat not found."


if __name__ == "__main__":
    ft = OGLFeatsTable()
    featname = "Tower Shield Proficiency"
    desc = ft.get_feat_type(featname)
    type_ = ft.get_feat_desc(featname)
    prereq_b = ft.get_feat_basic_prereq(featname)
    prereq_f = ft.get_feat_feats_prereq(featname)
    benefits = ft.get_feat_benefits(featname)
    normal = ft.get_feat_normal(featname)
    extrainfo = ft.get_feat_extra_info(featname)
    source = ft.get_feat_source(featname)
    link = ft.get_feat_link(featname)
    print(featname + "\n")
    print(type_ + "\n")
    print(desc + "\n")
    print(prereq_b + "\n")
    print(prereq_f + "\n")
    print(benefits + "\n")
    print(normal + "\n")
    print(extrainfo + "\n")
    print(source + "\n")
    print(link + "\n")
    featdict = ft.get_feat_dict(featname)
    print(featdict)
