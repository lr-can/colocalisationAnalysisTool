import pandas as pd
import plotly
import argparse
import plotly.graph_objs as go
from createReport import addPlot

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
    parser.add_argument("-b", "--basename", type=str, help="Base name of the output directory.", required=True)
    return parser.parse_args()

args = parse_args()

df = pd.read_csv(args.file, sep=",")
tolerance = 0.05 * max(df['end'])

def identify_interest_zones(dataframe, tolerance):
    """
    This function identifies the zones of interest in the dataframe, i.e. the provirus for which defenseFinder has found a system nearby.
    Args:
        dataframe (pd.DataFrame): The dataframe containing the defenseFinder and geNomad data.
    Returns:
        pd.DataFrame: A dataframe containing the zones of interest.
    """
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

zones_of_interest = identify_interest_zones(df, tolerance)
print(f"\033[96mZones where genomad results overlap with defensefinder and/or phastest results, including a {tolerance} bp tolerance:\033[0m")
print(zones_of_interest)

# Plot the data
import plotly.figure_factory as ff

def plot_data(zones_of_interest, tolerance):
    """
    Plot the data in the zones_of_interest dataframe.
    Args:
        zones_of_interest (pd.DataFrame): The dataframe containing the zones of interest.
        tolerance (float): The tolerance to use for the plot.
    Returns:
        list: A list of dictionaries containing the HTML strings for the plots.
    
    """

    result_buffer = []
    if zones_of_interest.empty:
        print("\033[91mWARNING: no colocalisation found for this analysis\033[0m")
        return []
    
    # Group by unique GeNomad sys_ids
    unique_sys_ids = zones_of_interest[zones_of_interest['origin'].str.lower() == 'genomad']['sys_id'].unique()
    print(f"Unique sys_ids: {unique_sys_ids}")
    if len(unique_sys_ids) == 0:
        print("\033[91mWARNING: no colocalisation found for this analysis\033[0m")
        return []

    for sys_id in unique_sys_ids:
        # Filter rows for the current sys_id
        genomad_rows = zones_of_interest[
            (zones_of_interest['origin'].str.lower() == 'genomad') & 
            (zones_of_interest['sys_id'] == sys_id)
        ]
        defense_rows = zones_of_interest[
            (zones_of_interest['origin'].str.lower() == 'defensefinder') & 
            (
            ((zones_of_interest['begin'] <= genomad_rows['end'].max() + tolerance) & 
             (zones_of_interest['end'] >= genomad_rows['begin'].min() - tolerance))
            )
        ]
        phastest_rows = zones_of_interest[
            (zones_of_interest['origin'].str.lower() == 'phastest') & 
            (
            ((zones_of_interest['begin'] <= genomad_rows['end'].max() + tolerance) & 
             (zones_of_interest['end'] >= genomad_rows['begin'].min() - tolerance))
            )
        ]

        # Determine plot range
        if genomad_rows.empty:
            print(f"No GeNomad rows found for sys_id {sys_id}. Skipping plot.")
            continue

        plot_start = min(genomad_rows['begin']) - tolerance
        plot_end = max(genomad_rows['end']) + tolerance

        # Create traces for the plot
        traces = []

        # Define base colors for each origin
        base_colors = {
            'genomad': 'blue',
            'defensefinder': 'red',
            'phastest': 'green'
        }

        # Add GeNomad elements
        for i, (_, row) in enumerate(genomad_rows.iterrows()):
            traces.append(go.Scatter(
            x=[row['begin'], row['end']],
            y=[1, 1],
            mode='lines',
            line=dict(color=f"rgba(0, 0, 255, {0.5 + 0.5 * (i / len(genomad_rows))})", width=15),
            name=f"GeNomad: {row['type']}"
            ))

        # Add DefenseFinder elements
        for i, (_, row) in enumerate(defense_rows.iterrows()):
            traces.append(go.Scatter(
            x=[row['begin'], row['end']],
            y=[0.5, 0.5],
            mode='lines',
            line=dict(color=f"rgba(255, 0, 0, {0.5 + 0.5 * (i / len(defense_rows))})", width=15),
            name=f"DefenseFinder: {row['type']}"
            ))

        # Add Phastest elements
        for i, (_, row) in enumerate(phastest_rows.iterrows()):
            traces.append(go.Scatter(
            x=[row['begin'], row['end']],
            y=[1.5, 1.5],
            mode='lines+text',
            line=dict(color=f"rgba(0, 255, 0, {0.5 + 0.5 * (i / len(phastest_rows))})", width=5),
            text=row['sys_id'],
            textposition='top center',
            name=f"Phastest: {row['sys_id']}"
            ))

        # Create the layout
        layout = go.Layout(
            title=f"Visualization for sys_id: {sys_id}",
            xaxis=dict(title="Position", showticklabels=True, range=[plot_start, plot_end]),
            yaxis=dict(title=None, showticklabels=False, showgrid=False, zeroline=False),
            showlegend=True
        )

        # Create the figure
        fig = go.Figure(data=traces, layout=layout)

        # Get the HTML string for the figure
        html_string = plotly.io.to_html(fig, full_html=True)
        print(f"HTML string for sys_id {sys_id} generated.")
        result_buffer.append({"plot":html_string, "sys_id":f"{genomad_rows.iloc[0]['nom']}_{sys_id}"})
    return result_buffer

result = plot_data(zones_of_interest, tolerance)


for plot in result:
    addPlot(args.basename, plot["plot"], tolerance, plot["sys_id"])

print(f"\033[92mPlots added to the final report.\033[0m")



