import pandas as pd
import plotly
import argparse
import plotly.graph_objs as go

def parse_args():
    """
    Parse command-line arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Visualisation script for colocalisation analysis.")
    parser.add_argument(
        "-f", "--file", 
        type=str, 
        required=True, 
        help="Path to the input CSV file containing the data."
    )
    return parser.parse_args()

args = parse_args()

df = pd.read_csv(args.file, sep=",")

def identify_interest_zones(dataframe):
    """
    This function identifies the zones of interest in the dataframe, i.e. the provirus for which defenseFinder has found a system nearby.
    Args:
        dataframe (pd.DataFrame): The dataframe containing the defenseFinder and geNomad data.
    Returns:
        pd.DataFrame: A dataframe containing the zones of interest.
    """
    tolerance = 0.01 * row["end"]
    zones_of_interest = []

    for index, row in dataframe.iterrows():
        overlaps = dataframe[
            (dataframe['origin'].str.lower() == 'defensefinder') | 
            (dataframe['origin'].str.lower() == 'phastest')
        ]
        overlaps = overlaps[
            (overlaps['begin'] <= row['end'] + tolerance) & 
            (overlaps['end'] >= row['begin'] - tolerance) & 
            (overlaps['nom'] == row['nom'])
        ]
        if not overlaps.empty:
            zones_of_interest.append(row)

    return pd.DataFrame(zones_of_interest)

zones_of_interest = identify_interest_zones(df)
print(zones_of_interest)
