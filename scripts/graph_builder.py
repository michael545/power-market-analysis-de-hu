import os
import sys
import pandas as pd
import networkx as nx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.config import graph_config

def build_flow_graph(data_directory):
    """
    nx.DiGraph: time-series flow data as edges.
    """
    G = nx.DiGraph()
    for country, neighbors_list in graph_config.NEIGHBORS.items():
        G.add_node(country, pos=graph_config.NODE_POSITIONS.get(country))
        for neighbor in neighbors_list:
            G.add_edge(country, neighbor)

    print(f"base graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} vertices.")

    for filename in os.listdir(data_directory):
            
            parts = filename.replace("flows_", "").replace(".csv", "").split('_')
            sender = None
            recipient = None

            if len(parts) == 2:
                sender, recipient = parts[0], parts[1]
            elif len(parts) == 3:# edge case
                if parts[0] == 'DE' and parts[1] == 'LU':
                    # DE_LU is the sender --> flows_DE_LU_PL.csv
                    sender = "DE_LU"
                    recipient = parts[2]
                elif parts[1] == 'DE' and parts[2] == 'LU':
                    # DE_LU is the getter --> flows_PL_DE_LU.csv
                    sender = parts[0]
                    recipient = "DE_LU"
            
            if not sender or not recipient:
                print(f"Warning: Could not parse sender/recipient from filename: {filename}. Skipping.")
                continue
            
            df = pd.read_csv(os.path.join(data_directory, filename), index_col=0, parse_dates=True)
            
            if df.index.tz is None:
                df.index = df.index.tz_localize('UTC')
            # standard UTC for consistency
            else:
                df.index = df.index.tz_convert('UTC')
                
            flow_data = df.iloc[:, 0].to_dict()
            # merge flow data to right vertex ---
            if G.has_edge(sender, recipient):
                existing_flows = G.edges[sender, recipient].get('flows', {})
                existing_flows.update(flow_data)
                nx.set_edge_attributes(G, {(sender, recipient): {"flows": existing_flows}})
            
            elif G.has_edge(recipient, sender):
                negated_flow_data = {timestamp: -value for timestamp, value in flow_data.items()}
                existing_flows = G.edges[recipient, sender].get('flows', {})
                existing_flows.update(negated_flow_data)
                nx.set_edge_attributes(G, {(recipient, sender): {"flows": existing_flows}})

    print("built graph with flow data.")
    return G


# build_flow_graph("C:\\Users\\micha\\code\\power-market-analysis-de-hu\\data\\processed\\flows")