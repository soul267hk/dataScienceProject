import pandas as pd
import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx

from dash import State, callback, dcc
from dash import html
from dash.dependencies import Input,Output
from dash_extensions.enrich import DashProxy ,html
from dash_extensions.javascript import arrow_function, assign

import plotly.express as px


app = dash.Dash(__name__)
server = app.server

#Import Data



#Dropdown Topic for europe
selected_country = ""

dropdown = dcc.Dropdown([
    "Graduation Rate",


],
"Graduation Rate",id = "topic_dropdown")
output_dropdown = html.Div(id="dd-output-copntainer")

@callback(
        Output("dd-output-copntainer","children"),
        Input("topic_dropdown","value")
)
def update_output(value):
    return f"You have selected {value}"

#Interactive Map



def get_info(feature=None):
    header = [html.H4("Countries of Europe")]
    if not feature:
        return header + [html.P("Hoover over a country")]
    return header + [
        html.Br(),
        " Click to reveal statistics for " + (feature["properties"]["name"]),
        
    ]

info = html.Div(
    children=get_info(),
    id="info",
    className="info",
    style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"},
)
#GEOJSON
classes = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ["#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#BD0026", "#800026"]
style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
ctg = [
    "{}+".format(
        cls,9
    )
    for i, cls in enumerate(classes[:-1])
] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")
geojson = dl.GeoJSON(url="/assets/custom.json",
                     style =style_handle,
                     zoomToBounds=True,
                     zoomToBoundsOnClick=True,
                     hoverStyle=arrow_function(dict(weight=5,color="#666",dashArray="")),
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="density"),
                     id="geojson",
                     )
Map = dl.Map(children=[dl.TileLayer(),geojson,colorbar,info],style={"display":"inline-block","height": "60vh","width":"80vh"},maxZoom=5,minZoom=3 ,maxBounds=[[70,-35],[34,50]],center=[54, 10], zoom=4)
             


@app.callback(Output("info", "children"), Input("geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)
# App Layout

app.layout = html.Div([
    html.Div([
            html.Div(style={"height":"10px"}),
            html.H1("Universities and higher Education",style={"marginLeft":"10px"}),
            html.Div(style={"height":"10px"}),
            html.Div(style={"height":"5px","backgroundColor":"#640650"}),
            ],style={"margin":"0","backgroundColor":"#9b0a7d"}),
            html.P("A data science project on how universities and higher education in germany evolved over the last decade and how germany compares to other european countries."),
            dcc.Tabs(id="tabs",value="tab-1",children=[
                dcc.Tab(label = "Education in Europe",value="tab-1"),
                dcc.Tab(label = "Germany only",value="tab-2"),

            ]),
            html.Div(id="tabs-content"),
    
],style={"margin":"0","border":"0","width":"100vw","height":"100vh"})

@callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                html.Div([
                html.H3('Tab content 1'),

            ]),
            html.Div([
                html.Div(style={"width":"40px"}),
                Map,
                html.Div(style={"width":"40px"}),
                html.Div([
                    dropdown,
                    output_dropdown,
                    html.Label("RightSideContent")
                ],style={"display":"inline-block"})],style={"display":"flex"})])

            
        
    
    elif tab == 'tab-2':
        return html.Div([
            html.H3('')
        ])



if __name__ == '__main__':
    app.run_server(debug=True)