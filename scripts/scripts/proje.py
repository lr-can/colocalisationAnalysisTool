import pandas as pd
import json
from functools import reduce
import glob
import argparse

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

def finder(result_file, defense_finder_prt):
    correspondance = defense_function(defense_finder_path=defense_finder_prt)
    defense = pd.read_csv(result_file, sep= "\t")
    begin_position = [correspondance[sys_beg]["begin"] for sys_beg in defense["hit_id"]]
    end_position = [correspondance[sys_end]["end"] for sys_end in defense["hit_id"]]
    defense["beg_pos"] = begin_position
    defense["end_pos"] = end_position

    nc_list = []
    sys_beg_list = []
    sys_id = []
    sys_end_list = []
    type_list = []
    origin_list = []

    for row in defense.itertuples():
        nc_list.append(row.replicon)
        sys_beg_list.append(int(row.beg_pos))
        sys_end_list.append(int(row.end_pos))
        type_list.append(row.subtype)
        sys_id.append(row.sys_id.replace(f"{row.replicon}_", ""))
    
    origin_list = ["DefenseFinder"] * len(sys_beg_list)
  
    return pd.DataFrame({"nom": nc_list, "type": type_list, "origin": origin_list, "begin": sys_beg_list, "end": sys_end_list, "sys_id": sys_id, 'origin_identifier': nc_list})

def genomad(genomad_path):

    df = pd.read_csv(genomad_path, sep= "\t")
    
    nc_list = []
    sys_beg_list = []
    sys_end_list = []
    taxonomy = []
    topology_list = []
    identifier_list = []
    sys_id = []

    for row in df.itertuples():
        """
        identifier, coordinates, tax, topology = row.seq_name, row.coordinates, row.taxonomy, row.topology 
        splitted_coords = coordinates.split("-")
        sys_beg = int(splitted_coords[0])
        sys_end = int(splitted_coords[1])"
        """
        identifier, sys_beg, sys_end, tax, annotation_accessions, annotation_description = row.gene, row.start, row.end, row.taxname, row.annotation_accessions, row.annotation_description

        identifier_ = identifier.split("|")
        identifier__= identifier_[1].split("_") if len(identifier_) > 1 else [identifier_[0]]
        sys_id.append(identifier__[0] + "_" + identifier__[1] + "_" + identifier__[2] if len(identifier__) > 2 else identifier_[0])
        nc_value = identifier_[0]
        identifier_list.append(identifier)

        nc_list.append(nc_value)
        sys_beg_list.append(sys_beg)
        sys_end_list.append(sys_end)
        taxonomy.append(tax)
        if not pd.isna(annotation_accessions) and annotation_accessions != "NA":
            if not pd.isna(annotation_description) and annotation_description != "NA":
                topology = f"{annotation_description} ({annotation_accessions.split(';')[0]})" 
            else:
                topology = f"{annotation_accessions.split(';')[0]}"
        else:
            topology = identifier.replace(nc_value, "").replace("|", "")
        topology_list.append(topology)
    
    origin_list = ["GeNomad"] * len(topology_list)
    
    
    return pd.DataFrame({"nom": nc_list, "type": topology_list, "origin": origin_list, "begin": sys_beg_list, "end": sys_end_list, "sys_id": sys_id, 'origin_identifier': identifier_list})

def phastest(phastest_path):

    with open(phastest_path) as file:
        data = json.load(file)
    
    nc_list = []
    sys_id = []
    sys_beg_list = []
    sys_end_list = []
    type_list = []
    origin_list = []
    
    for region in data:
        sys_beg = region["start"] 
        sys_end = region["stop"]
    
        nc_value = region["most_common_phage"]
    
        nc_list.append(nc_value)
        sys_id.append(nc_value)
        sys_beg_list.append(int(sys_beg))
        sys_end_list.append(int(sys_end))
        type_list.append("phage")
        origin_list.append("Phastest")
    
    
    return pd.DataFrame({"nom": nc_list, "type": type_list, "origin": origin_list, "begin": sys_beg_list, "end": sys_end_list, "sys_id": sys_id, 'origin_identifier': nc_list})
 
 

def main(path_to_defense_finder_result_folder, path_to_genomad_result_folder, base_name, path_to_phastest_result_folder=None):
    # Charger les résultats de Defense Finder
    defense_finder_tsv = glob.glob(f"{path_to_defense_finder_result_folder}/{base_name}/*_defense_finder_genes.tsv")[0]
    defense_finder_prt = glob.glob(f"{path_to_defense_finder_result_folder}/{base_name}/*.prt")[0]
    defense_df = finder(defense_finder_tsv, defense_finder_prt)
    
    # Charger les résultats de Genomad
    genomad_path = glob.glob(f"{path_to_genomad_result_folder}/{base_name}/*_summary/*_virus_genes.tsv")[0]
    genomad_df = genomad(genomad_path)

    # Charger et fusionner les résultats de Phastest si fournis
    if path_to_phastest_result_folder != "":
        phastest_path = f"{path_to_phastest_result_folder}/{base_name}/predicted_phage_regions.json"
        phastest_df = phastest(phastest_path)
    else:
        phastest_df = pd.DataFrame(columns=["nom", "type", "origin", "begin", "end", "sys_id", "origin_identifier"])
    
    # Fusion des dataframes
    dfs = [genomad_df, phastest_df, defense_df]
    merged_df = reduce(lambda left, right: pd.merge(left, right, on=None, how='outer'), dfs)
    merged_df.to_csv(path_or_buf="./merged_res.csv", sep=",", index=False)
    print("Merged results saved to ./merged_res.csv")
    return merged_df

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process defense finder, genomad, and optionally phastest results.")
    parser.add_argument("path_to_defense_finder_result_folder", type=str, help="Path to the folder containing Defense Finder results")
    parser.add_argument("path_to_genomad_result_folder", type=str, help="Path to the folder containing Genomad results")
    parser.add_argument("base_name", type=str, help="Base name for the result files")
    parser.add_argument("--path_to_phastest_result_folder", type=str, help="Path to the folder containing Phastest results", default="")

    args = parser.parse_args()
    result = main(
        args.path_to_defense_finder_result_folder,
        args.path_to_genomad_result_folder,
        args.base_name,
        args.path_to_phastest_result_folder
    )

    print(f"\033[96mThe unfiltered merging results in {len(result['nom'])} rows.\033[0m")
