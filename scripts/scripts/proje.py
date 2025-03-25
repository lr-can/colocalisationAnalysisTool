import pandas as pd
import json
from functools import reduce
import glob

def defense_function(defense_finder_path):
    with open(defense_finder_path) as fichier: 
        output_dict = {}
        for ligne in fichier:
            if not ligne.startswith(">"):
                continue
            splitted_ligne = ligne.split(" # ")
            reference = splitted_ligne[0].strip(">")
            begin = splitted_ligne[1]
            end = splitted_ligne[2]
            output_dict.update({
                reference: {"begin": begin, "end": end}
            })
        return output_dict

def finder(defense_finder_tsv, defense_finder_prt):
    correspondance = defense_function(defense_finder_prt)
    defense = pd.read_csv(defense_finder_tsv, sep="\t")
    
    defense["beg_pos"] = defense["sys_beg"].map(lambda x: correspondance.get(x, {}).get("begin", None))
    defense["end_pos"] = defense["sys_end"].map(lambda x: correspondance.get(x, {}).get("end", None))
    
    return defense

def main(path_to_defense_finder_result_folder, path_to_genomad_result_folder, base_name, path_to_phastest_result_folder=None):
    # Charger les résultats de Defense Finder
    defense_finder_tsv = glob.glob(f"{path_to_defense_finder_result_folder}/{base_name}/*_defense_finder_systems.tsv")
    defense_finder_prt = glob.glob(f"{path_to_defense_finder_result_folder}/{base_name}/*.fa.prt")
    defense_df = finder(defense_finder_tsv, defense_finder_prt)
    
    # Charger les résultats de Genomad
    genomad_path = glob.glob(f"{path_to_genomad_result_folder}/{base_name}*_summary/*_virus_summary.tsv")[0]
    genomad_df = pd.read_csv(genomad_path, sep="\t")
    
    genomad_df["sys_beg"] = genomad_df["coordinates"].apply(lambda x: int(x.split("-")[0]))
    genomad_df["sys_end"] = genomad_df["coordinates"].apply(lambda x: int(x.split("-")[1]))
    
    # Fusionner les résultats Defense Finder et Genomad
    merged_df = pd.merge(defense_df, genomad_df, on=["sys_beg", "sys_end"], how="outer")
    
    # Charger et fusionner les résultats de Phastest si fournis
    if path_to_phastest_result_folder:
        phastest_path = f"{path_to_phastest_result_folder}/{base_name}/predicted_phage_regions.json"
        phastest_df = pd.read_csv(phastest_path, sep="\t")
        merged_df = pd.merge(merged_df, phastest_df, on=["sys_beg", "sys_end"], how="outer")
    
    return merged_df
