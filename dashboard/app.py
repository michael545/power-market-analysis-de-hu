import dash
from dash import Dash, html, dcc
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.H1('power flow analysis'),
    html.P('WARNING !!!: All timestamps are in UTC_+00:00', style={'color': 'red', 'fontWeight': 'bold'}),
    dcc.Link('Map', href='/map'),
    html.Hr(),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
