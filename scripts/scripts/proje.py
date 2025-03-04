import pandas as pd
import json
from functools import reduce
def defense_function():
    with open ("colocalisationAnalysisTool/scripts/results/result_Finder/GCF_000006765/GCF_000006765.1.fa.prt") as fichier: 
        output_dict = {}
        for ligne in fichier:
            if not ">" in ligne:
                continue
            splitted_ligne = ligne.split(" # ")
            reference = splitted_ligne[0].strip(">")
            begin = splitted_ligne[1]
            end = splitted_ligne[2]
            output_dict.update({
                reference:{"begin": begin, "end": end}
            })
        return output_dict

def finder():
    correspondance = defense_function()
    defense = pd.read_csv("/data/home/melkhattabi/Projet_S2/colocalisationAnalysisTool/scripts/results/result_Finder/GCF_000006765/GCF_000006765.1_defense_finder_systems.tsv", sep= "\t")
    begin_position = [correspondance[sys_beg]["begin"] for sys_beg in defense["sys_beg"]]
    end_position = [correspondance[sys_end]["end"] for sys_end in defense["sys_end"]]
    defense["beg_pos"] = begin_position
    defense["end_pos"] = end_position
 
    return defense
# vamos a cargar la tabla de genomad
df = pd.read_csv("colocalisationAnalysisTool/scripts/results/results_genomad/GCF_000006765/GCF_000006765.1_summary/GCF_000006765.1_virus_summary.tsv", sep= "\t")


# Listas vacías para almacenar los valores procesados
nc_list = []
sys_beg_list = []
sys_end_list = []
taxonomy = []
topology_list = []

# Recorrer cada fila de la columna "coordinates"
for row in df.itertuples():
    identifier, coordinates, tax, topology = row.seq_name, row.coordinates, row.taxonomy, row.topology  # Extraer valores
    splitted_coords = coordinates.split("-")  # Separar sys_beg y sys_end
    sys_beg = int(splitted_coords[0])
    sys_end = int(splitted_coords[1])
    
    # Extraer solo el nombre base (antes del "|")
    nc_value = identifier.split("|")[0]  # Se queda con "NC_002516.2"

    # Guardar en las listas
    nc_list.append(nc_value)
    sys_beg_list.append(sys_beg)
    sys_end_list.append(sys_end)
    taxonomy.append(tax)
    topology_list.append(topology)

origin_list = ["GeNomad"] * len(topology_list)


# Crear un nuevo DataFrame solo con las columnas deseadas
df_genomad = pd.DataFrame({"nom": nc_list, "type": topology_list, "origin": origin_list, "begin": sys_beg_list, "end": sys_end_list})

# Mostrar la tabla final
print(df_genomad.to_string(index=False))  # Muestra sin índice




#PHASTEST:

with open("colocalisationAnalysisTool/scripts/results/results_phastest/ZZ_47ea6e6e39/predicted_phage_regions.json") as file:
    data = json.load(file)

# Listas vacías para almacenar los valores
nc_list = []
sys_beg_list = []
sys_end_list = []
type_list = []
origin_list = []

# Recorremos cada región del JSON
for region in data:
    sys_beg = region["start"]  # Extraer el inicio
    sys_end = region["stop"]    # Extraer el final

    nc_value = region["most_common_phage"]  # Como no está en el JSON, lo asignamos manualmente

    # Guardamos los valores en las listas
    nc_list.append(nc_value)
    sys_beg_list.append(int(sys_beg))
    sys_end_list.append(int(sys_end))
    type_list.append("phage")
    origin_list.append("Phastest")


# Crear un DataFrame con la estructura deseada
df_phastest = pd.DataFrame({"nom": nc_list, "type": type_list, "origin": origin_list, "begin": sys_beg_list, "end": sys_end_list})

# Mostrar el DataFrame
print(df_phastest.to_string(index=False))

df_finder = finder()
nc_list = []
sys_beg_list = []
sys_end_list = []
type_list = []
origin_list = []

print(df_finder.columns)
print(df_finder)
for row in df_finder.itertuples():
    nc_list.append("_".join(row.sys_id.split("_")[:2]))
    sys_beg_list.append(int(row.beg_pos))
    sys_end_list.append(int(row.end_pos))
    type_list.append(row.subtype)

origin_list = ["DefenseFinder"] * len(sys_beg_list)

df_DF = pd.DataFrame({"nom": nc_list, "type": type_list, "origin": origin_list, "begin": sys_beg_list, "end": sys_end_list})

print(df_DF.to_string(index=False))

dfs = [df_genomad, df_phastest, df_DF]

merged_df = reduce(lambda left, right: pd.merge(left, right, on=None, how='outer'), dfs)

merged_df.to_csv(path_or_buf="./merged_res.csv", sep=",", index=False)

print(merged_df)