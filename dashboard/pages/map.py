import dash
from dash import dcc, html, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from functools import lru_cache

# Import necessary functions and data at the top level
from scripts.graph_builder import build_flow_graph
from scripts.config.graph_config import NODE_POSITIONS

dash.register_page(__name__, path='/map')

# --- Data Loading Function with Caching ---
@lru_cache(maxsize=None)
def get_flow_graph():
    """
    Loads and returns the flow graph, caching the result so it runs only once.
    """
    print("--- Loading and building the flow graph... ---")
    data_dir = r"C:\Users\micha\code\power-market-analysis-de-hu\data\processed\flows"
    try:
        graph = build_flow_graph(data_dir)
        print("--- Flow graph built successfully. ---")
        return graph
    except Exception as e:
        print(f"!!! Failed to build flow graph: {e} !!!")
        return None

# --- Helper function to get timestamps and labels ---
def get_time_data(flow_graph):
    """
    Extracts timestamps and labels from the flow graph.
    """
    if not flow_graph or not flow_graph.edges:
        return [], {}

    # Find the first edge that has flow data
    edge_with_data = next((e for e in flow_graph.edges(data=True) if 'flows' in e[2] and e[2]['flows']), None)
    
    if not edge_with_data:
        return [], {}

    timestamps = list(edge_with_data[2]['flows'].keys())
    
    # Create user-friendly labels for the timestamps
    if timestamps and isinstance(timestamps[0], str):
        time_labels = {i: pd.to_datetime(ts).strftime('%Y-%m-%d %H:%M') for i, ts in enumerate(timestamps)}
    elif timestamps:
        time_labels = {i: ts.strftime('%Y-%m-%d %H:%M') for i, ts in enumerate(timestamps)}
    else:
        time_labels = {}
        
    return timestamps, time_labels

# --- Load data once ---
flow_graph = get_flow_graph()
timestamps, time_labels = get_time_data(flow_graph)

# --- Page Layout ---
def layout():
    """
    Defines the layout of the page.
    """
    if not flow_graph or not timestamps:
        return html.Div([
            html.H2("Error: Could Not Load Graph Data"),
            html.P("The application was unable to load or process the flow data. Please check the terminal for error messages from the 'build_flow_graph' script.")
        ])

    return html.Div([
        html.H2("Electricity Flow Map"),
        dcc.Graph(id='network-map', style={'height': '70vh'}),
        dcc.Dropdown(
            id='time-dropdown',
            options=[{'label': label, 'value': i} for i, label in time_labels.items()],
            value=0,
            style={'marginBottom': '20px'},
            clearable=False
        ),
        dcc.Slider(
            id='time-slider',
            min=0,
            max=len(timestamps) - 1,
            value=0,
            marks={i: label for i, label in time_labels.items() if pd.to_datetime(label).minute == 0},
            step=1
        )
    ])

# --- Callbacks ---
@callback(
    Output('network-map', 'figure'),
    Input('time-slider', 'value')
)
def update_map(time_index):
    """
    Updates the map figure when the time slider's value changes.
    """
    if time_index is None:
        return dash.no_update

    selected_timestamp = timestamps[time_index]

    edge_traces = []
    mid_lons, mid_lats, hover_texts = [], [], []

    for u, v, data in flow_graph.edges(data=True):
        if 'flows' in data and selected_timestamp in data['flows']:
            flow_value = data['flows'].get(selected_timestamp, 0)
            
            if flow_value == 0:
                continue

            source, target = (u, v) if flow_value > 0 else (v, u)
            arrow_color = 'green' if flow_value > 0 else 'red'
            line_width = max(1.5, np.log10(abs(flow_value) + 1))
            
            edge_traces.append(go.Scattermapbox(
                lon=[NODE_POSITIONS[source][1], NODE_POSITIONS[target][1]],
                lat=[NODE_POSITIONS[source][0], NODE_POSITIONS[target][0]],
                mode='lines',
                line=dict(width=line_width, color=arrow_color),
                hoverinfo='none'
            ))

            mid_lons.append((NODE_POSITIONS[u][1] + NODE_POSITIONS[v][1]) / 2)
            mid_lats.append((NODE_POSITIONS[u][0] + NODE_POSITIONS[v][0]) / 2)
            hover_texts.append(f'Flow from {source} to {target}: {abs(flow_value):.2f} MW')

    hover_trace = go.Scattermapbox(
        lon=mid_lons, lat=mid_lats, text=hover_texts, mode='markers',
        marker=dict(size=20, opacity=0), hoverinfo='text'
    )

    node_trace = go.Scattermapbox(
        lon=[pos[1] for pos in NODE_POSITIONS.values()],
        lat=[pos[0] for pos in NODE_POSITIONS.values()],
        text=list(NODE_POSITIONS.keys()),
        mode='markers+text',
        marker=dict(size=14, color='rgb(235, 0, 100)'),
        hoverinfo='text',
        textposition='top center'
    )

    fig = go.Figure(data=edge_traces + [node_trace, hover_trace])
    fig.update_layout(
        title=f'Electricity Flow at {time_labels.get(time_index, "")}',
        showlegend=False,
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=50, lon=15),
            zoom=3
        ),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    return fig

@callback(
    Output('time-slider', 'value', allow_duplicate=True),
    Output('time-dropdown', 'value', allow_duplicate=True),
    Input('time-slider', 'value'),
    Input('time-dropdown', 'value'),
    prevent_initial_call=True
)
def sync_inputs(slider_value, dropdown_value):
    """
    Synchronizes the slider and dropdown components.
    """
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'time-slider':
        return slider_value, slider_value
    elif trigger_id == 'time-dropdown':
        return dropdown_value, dropdown_value
    
    return dash.no_update, dash.no_update
