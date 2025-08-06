import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Power Market Flow Analysis'),
    dcc.Link('Map', href='/map'),
    html.Hr(),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
