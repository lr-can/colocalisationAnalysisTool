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
def merge_defense_and_genomad(defense_data, genomad_data, tolerance=100000):
    # Merge the two datasets based on overlapping coordinates with tolerance
    merged_data = []
    for _, defense_row in defense_data.iterrows():
        for _, genomad_row in genomad_data.iterrows():
            if not (int(defense_row["end"]) + tolerance < int(genomad_row["begin"]) or int(defense_row["begin"]) - tolerance > int(genomad_row["end"])):
                merged_data.append({
                    "defense_sys_id": defense_row["sys_id"],
                    "defense_type": defense_row["type"],
                    "genomad_sys_id": genomad_row["sys_id"],
                    "genomad_type": genomad_row["type"],
                    "overlap_begin": max(int(defense_row["begin"]), int(genomad_row["begin"])),
                    "overlap_end": min(int(defense_row["end"]), int(genomad_row["end"]))
                })
    return pd.DataFrame(merged_data)

# Example usage
defense_data = pd.read_csv("defense_data.csv")
genomad_data = pd.read_csv("genomad_data.csv")
merged_results = merge_defense_and_genomad(defense_data, genomad_data, tolerance=100000)
print(merged_results)


