#pwd
import pandas as pd
def tableau():
    dico={}
    with open("result_Finder/GCF_000006765.1.fa.prt", "r") as file:
        for line in file:
            if ">" not in line:
                continue
            colunm = line.split(' #')
            ref = colunm[0].strip(">")
            begin = colunm[1]
            end = colunm[2]
            dico.update({
                ref : {"begin" : begin, "end": end}
            })
        return dico
    

def defense_finder():
    correspondance = tableau()
    defense = pd.read_csv("result_Finder/GCF_000006765.1.fa_defense_finder_systems.tsv",sep = '\t')
    begin_positions = [correspondance[sys_beg]["begin"] for sys_beg in defense["sys_beg"]]
    end_positions = [correspondance[sys_end]["begin"] for sys_end in defense["sys_end"]]
    defense["beg_pos"] = begin_positions
    defense["end_pos"] = end_positions
    return defense

print(defense_finder())

"""
Pour genomad : split les coordonnées en deux 788542-797598 par "-" et appeler sys_beg et sys_end avec les données.
Pour phastest : à partir de la librairy json, et voir comment transformer en pandas dataframe.
"""


