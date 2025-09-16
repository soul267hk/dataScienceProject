import pandas as pd
import dash

from dash import callback, dcc
from dash import html
from dash.dependencies import Input,Output

import plotly.express as px


app = dash.Dash(__name__)
server = app.server

#Import Data




# App Layout

app.layout = html.Div([
    html.H1("Universities and higher Education"),
    html.P("A data science project on how universities and higher education in germany evolved over the last decade and how germany compares to other european countries."),

    dcc.Tabs(id="tabs",value="tab-1",children=[
        dcc.Tab(label = "Tab 1",value="tab-1"),
        dcc.Tab(label = "Tab 2",value="tab-2"),
        dcc.Tab(label = "Tab 3",value="tab-3"),
        dcc.Tab(label = "Tab 4",value="tab-4"),
    ])
    
])

@callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == "tab-3":
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == "tab-4":
        return html.Div([
            html.H3('Tab content 2')
        ])

if __name__ == '__main__':
    app.run(debug=True)