import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
from scripts.graph_builder import build_flow_graph

dash.register_page(__name__, path='/map')

data_dir = r"C:\Users\micha\code\power-market-analysis-de-hu\data\processed\flows"
flow_graph = build_flow_graph(data_dir)

#the layout
layout = html.Div([
    dcc.Graph(id='network-graph'),
    dcc.Slider(
        id='time-slider',
        min=0,
        max=len(list(flow_graph.edges(data=True))[0][-1]['flow']) - 1,
        value=0,
        step=1
    )
])

@callback(
    Output('network-graph', 'figure'),
    Input('time-slider', 'value')
)

def update_graph(time_index):
    fig = go.Figure()

    for u, v, data in flow_graph.edges(data=True):
        fig.add_trace(go.Scatter(
            x=[flow_graph.nodes[u]['pos'][0], flow_graph.nodes[v]['pos'][0]],
            y=[flow_graph.nodes[u]['pos'][1], flow_graph.nodes[v]['pos'][1]],
            mode='lines',
            line=dict(width=data['flow'][time_index] / 1000)
        ))

    for node, data in flow_graph.nodes(data=True):
        fig.add_trace(go.Scatter(
            x=[data['pos'][0]],
            y=[data['pos'][1]],
            mode='markers+text',
            text=[node],
            marker=dict(size=10)
        ))

    return fig
