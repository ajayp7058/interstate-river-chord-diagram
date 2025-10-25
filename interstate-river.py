import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load river flow data
data = pd.read_csv("river_flow_data.csv")

# Get all unique states involved in flows
from_states = data['From_State'].unique()
to_states = data['To_State'].unique()
all_states = pd.unique(np.concatenate((from_states, to_states)))

# Map each state to a unique index
state_to_index = {}
for index in range(len(all_states)):
    state_name = all_states[index]
    state_to_index[state_name] = index

# Assign colors to each basin
basin_names = data['Basin'].unique()
color_list = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]
basin_to_color = {}
for i in range(len(basin_names)):
    basin_name = basin_names[i]
    color = color_list[i % len(color_list)]
    basin_to_color[basin_name] = color

# Prepare Sankey link data
source_indices = []
target_indices = []
flow_values = []
link_colors = []
hover_texts = []

for row_index in range(len(data)):
    row = data.iloc[row_index]

    from_state = row['From_State']
    to_state = row['To_State']
    flow_amount = row['Flow_TMC']
    basin_name = row['Basin']
    river_name = row['River']
    flow_type_raw = row['Flow_Type']
    notes = row['Notes']

    # Skip rows with missing critical data
    if pd.isna(from_state) or pd.isna(to_state) or pd.isna(flow_amount):
        continue

    source_index = state_to_index[from_state]
    target_index = state_to_index[to_state]

    # Use default color if basin is unknown
    if basin_name in basin_to_color:
        color = basin_to_color[basin_name]
    else:
        color = "#cccccc"

    # Customize flow type label
    if flow_type_raw == "Seasonal":
        flow_type = "Seasonal Flow"
    else:
        flow_type = "Perennial Flow"

    hover_text = (
        "River: " + river_name + "<br>" +
        "Basin: " + basin_name + "<br>" +
        "Flow: " + str(flow_amount) + " TMC<br>" +
        "Type: " + flow_type + "<br>" +
        "Notes: " + notes
    )

    source_indices.append(source_index)
    target_indices.append(target_index)
    flow_values.append(flow_amount)
    link_colors.append(color)
    hover_texts.append(hover_text)

# Define Sankey diagram structure
link_data = {
    'source': source_indices,
    'target': target_indices,
    'value': flow_values,
    'color': link_colors,
    'hovertemplate': hover_texts
}

node_data = {
    'label': all_states,
    'pad': 20,
    'thickness': 20,
    'color': "#bbbbbb"
}

# Create and display the Sankey diagram
sankey_diagram = go.Figure(go.Sankey(link=link_data, node=node_data))
sankey_diagram.update_layout(
    title_text="Inter-State River Water Flow in India",
    font_size=12,
    height=800
)
sankey_diagram.show()
