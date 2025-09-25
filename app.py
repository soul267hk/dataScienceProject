import pandas as pd
import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx

from dash import State, callback, dcc , no_update
from dash import html
from dash.dependencies import Input,Output
from dash_extensions.enrich import DashProxy ,html
from dash_extensions.javascript import arrow_function, assign
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import plotly.express as px


app = dash.Dash(__name__)
server = app.server

#Import Data

ger_entranceQual = pd.read_csv("assets/EntranceQualification.csv",sep=";")
ger_entranceRate = pd.read_csv("assets/EntranceRate.csv",sep=";")
ger_gradRate = pd.read_csv("assets/GraduationRate.csv",sep=";")
europe_enrolled = pd.read_csv("assets/enrolled.csv")
europe_enrolledMaster = pd.read_csv("assets/enrolled_master.csv")
enrolled_age = pd.read_csv("assets/age_enrolled.csv")


rq1 = pd.read_csv("assets/rq1.csv")
rq1_sum = pd.read_csv("assets/rq1_sum.csv")

rq3 = pd.read_csv("assets/rq3.csv")
#Setup Figures

ger_fig_entQual = px.line(ger_entranceQual,x="Year",y=["Entrance qualification for univ. of appl. sciences","University entrance qualification","Total"],title="Entrance qualification rate").update_layout(xaxis= dict(dtick =1))
ger_fig_entRate = px.line(ger_entranceRate,x="Year",y=["male","female","total"],title="Entrance Rate to higher education").update_layout(xaxis= dict(dtick =1))
ger_fig_gradRate = px.line(ger_gradRate,x="Year",y=["male","female","total"],title="graduation rate from first degree courses (bachelors)").update_layout(xaxis= dict(dtick =1))

NameToCode ={
    'Belgium':'BE',
    'Bulgaria':'BG',
    'Czechia':"CZ",
    'Denmark':"DK",
    'Germany':"DE",
    'Estonia':"EE",
    'Ireland':"IE",
    'Greece':"GR",
    'Spain':"ES",
    'France':"FR" ,
    'Croatia':"HR",
    'Italy':"IT",
    'Cyprus':"CY",
    'Latvia':"LV",
    'Lithuania':"LT",
    'Luxembourg':"LU",
    'Hungary':"HU",
    'Malta':"MT",
    'Netherlands':"NL",
    'Austria':"AT",
    'Poland':"PL",
    'Portugal':"PT",
    'Romania':"RO",
    'Slovenia':"SI",
    'Slovakia':"SK",
    'Finland':"FI",
    'Sweden':"SE",
    'Iceland':"IS",
    'Liechtenstein':"LI",
    'Norway':"NO",
    'Switzerland':"CH",
    'United Kingdom':"UK",
    'Bosnia and Herzegovina':"BA",
    'Montenegro':"ME",
    'North Macedonia':"MK",
    'Georgia':"GR",
    'Albania':"AL",
    'Serbia':"RS",
    'Türkiye':"TR"
}






#Functions 
def updateCountry(feature=None):
    if not feature:
        return html.H4("")
    
    dcc.Store(id="country",data=feature["properties"]["name"])
    dcc.St
    return [html.H4("Statistics for " + (feature["properties"]["name"]))] + []
    
def get_info(feature=None):
    header = [html.H4("Countries of Europe")]
    if not feature:
        return header + [html.P("Hoover over a country")]
    return header + [
        html.Br(),
        " Click to reveal statistics for " + (feature["properties"]["name"]),
        
    ]
def updatePlot(feature=None,category=None):
    if not feature :
        return 
    if not category:
        return
    name = feature["properties"]["name"]
    return html.H1(f"Youve selected {name} for category {category}")


#GEOJSON Interactive Map
classes = [0, 10000, 20000, 50000, 100000, 200000, 500000, 1000000,2000000,5000000]
colorscale = ["#FDD8A8", "#FDC792", "#FDB37C", "#FD9C67", "#FE8251", "#FE653A", "#FF4424", "#E63F18","#CD3A0E","#B43606"]
style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
ctg = ["0","10k","20k","50k","100k","200k","500k","1M","2M","5M"]
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
geojson = dl.GeoJSON(url="/assets/export.json",
                     style =style_handle,
                     zoomToBounds=True,
                     zoomToBoundsOnClick=True,
                     
                     hoverStyle=arrow_function(dict(weight=5,color="#666",dashArray="")),
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="value"),
                     
                     id="geojson",
                     )

             
# App Layout Elements
seperator30px = html.Div(style={"height":"30px"})

def block(markdown,plot): ## Produce a block for findings 
        return html.Div([
                html.Div([
                    markdown
                ],className="roundedCorners",style={"display":"inline-block","width":"40vw","margin-left":"30px","backgroundColor":"#ffffff"}),
                html.Div(style={"width":"40px"}),
                html.Div([html.Div([plot],style={"margin":"20px"})
                    
                ],className="roundedCorners",style={"display":"inline-block","width":"50vw","margin-right":"30px","backgroundColor":"#ffffff"}),
            ],style={"display":"flex"})

dropdown = dcc.Dropdown([
    "Enrollment by field (Bachelor)", #done 
    "Enrollment by field (Master)",
    "Enrollment by Gender (Bachelor)",
    "Enrollment by Gender (Master)",
    "Enrollment by Age Group (Bachelor)",
    "Enrollment by Age Group (Master)",
    "Rate of master's to bachelor's graduates by field"
],
"Enrollment by field (Bachelor)",id = "memory-field",style={"width":"350px","margin-right":"40vw","margin-left":"auto"})

info = html.Div(
    children=get_info(),
    id="info",
    className="info",
    style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"},
)

Map = dl.Map(children=[dl.TileLayer(),geojson,colorbar,info],className="roundedCorners",style={"display":"inline-block","height": "60vh","width":"80vh"},maxZoom=5,minZoom=3 ,maxBounds=[[70,-35],[34,50]],center=[54, 10], zoom=4)


topics ={
    0:"Rate of master’s to bachelor’s degree graduates by field", #done
    1:"Differences in enrollment by gender across different countries", #done
    2:"Differences between Germany and Europe in enrollment rate in academic fields", #done
    3:"Differences in age groups enrolled between countries", #done
    4:"How does Germany compare in the percentage of Female students by different academic fields?",
    5:"Increase in enrollments into bachelor (or similar) degrees in Germany.",
}
topicSlider = html.Div([dcc.Slider(0,5,value=0,step=1,id="sliderQuestions",className="SliderResearchQuestions",marks=None)],className="roundedCorners",style={"height":"50px","alignContent": "center","width":"60vw","marginLeft":"40px","backgroundColor":"#20282a"},)
statistics = html.Div(children=updatePlot(),
                      id="'country-statistics'",
                      className="'country-statistics'")
header = [
            html.Div(style={"height":"10px"}),
            html.H1("Universities and higher Education",style={"marginLeft":"50px","color":"#ffffff"}),
            html.Div(style={"height":"10px"}),
            html.Div(style={"height":"5px","backgroundColor":"#640650"}),
            ]
tab1 = html.Div([
                html.Div([
                html.H3('Interactive map of europe',style={"margin-left":"30px"}),

            ]),
            dropdown,
            html.Div([
                html.Div(style={"width":"40px"}),
                Map,
                html.Div(style={"width":"40px"}),
                
                html.Div([
                    
                    dcc.Graph(id='memory-graph',style={"margin":"30px","height":"50vh","width":"50vw",})

                ],style={"display":"inline-block","backgroundColor":"#ffffff"},className="roundedCorners")],style={"display":"flex"},)])

tab2 = html.Div([
                html.H3('Use the slider below to navigate between our findings.',style={"marginLeft":"40px"}),
                topicSlider,
                html.Div(id="findings"),

        ])

# App Layout

app.layout = html.Div([
            dcc.Store(id='memory-output'),
            html.Div(header,style={"backgroundColor":"#9b0a7d"}),
            html.P("A data science project on how universities and higher education in germany evolved over the last decade and how germany compares to other european countries."),
            dcc.Tabs(id="tabs",value="tab-1",children=[
                dcc.Tab(label = "Discover Europe",value="tab-1"),
                dcc.Tab(label = "Findings",value="tab-2"),

            ]),
            html.Div(id="tabs-content"),
            html.Div([
                html.P("All statistics that seperate by gender only include male and female since the datasets we used did not provide data about people identifying as diverse.",style={"margin-left":"30px"}),
                html.P("Statisical annomalies can be explained by differences in educational systems .",style={"margin-left":"30px"})
            ],style={"margin-top":"auto","margin-bottom":"0px","display":"flex"})
            
    
],style={"margin":"0","border":"0","width":"100vw","height":"100vh"})


@callback(Output("findings","children"),Input("sliderQuestions","value"))
def update_findings(value):
    




    header = html.H1(topics[value],style={"text-align":"center"})

    match value:

        case 0:
            df = rq1_sum
            df = df[df["Field of Education"] != "Generic programmes and qualifications"]
            df = df.groupby(["Field of Education","Degree"]).sum().reset_index()
            markdown =  dcc.Markdown("""
                                * Rate of students graduating with a master’s degree to the students graduating with a bachelor’s degree between 2011 and 2022.
                                * Students in the field of Services, pursue a master’s degree significantly less often than students of other fields.
                                * Education is a special case since not every country offers a bachelor’s degree in Education, resulting in a high rate of master’s degrees.
                """)
            fig = px.bar(df,x="Field of Education",y="Value",color="Degree")




            dff = rq1_sum

            sum_bach= dff[dff["Degree"]=="Bachelor"]
            sum_mast= dff[dff["Degree"]=="Master"]
            join = pd.merge(sum_bach,sum_mast,on=["Country","Field of Education"],how="inner")

            join = join.groupby(["Field of Education","Degree_x","Degree_y"]).sum().reset_index()
            join["Rate"] = join["Value_y"] / join["Value_x"] 
            
            fig2  = px.bar(join,x="Field of Education",y=(join["Rate"]*100),labels={"y":"Rate of master to bachelor graduates [%]"})

            markdown2 = dcc.Markdown("""
            * First
                """)
            plot2 = dcc.Graph(figure=fig2)


            plot = dcc.Graph(figure=fig)
            middle = html.Div([block(markdown=markdown,plot=plot),seperator30px,block(markdown=markdown2,plot=plot2),
                               ])
        case 1:
            markdown = dcc.Markdown()

            dfb = europe_enrolled
            dfm = europe_enrolledMaster
            dft = pd.concat([dfb,dfm])

            dft
            
            dft = dft.groupby(["sex","geo"]).sum().reset_index()
            dft = pd.merge(dft[dft["sex"] !="Total"],dft[dft["sex"] =="Total"],on=["geo"],suffixes=["","_total"])

            dft["%"] = (dft["value"] / dft["value_total"])*100
            dft = dft.sort_values(by="%",ascending=False)
            fig1 = px.bar(dft,x="geo",y="%",color="sex",labels={"%":"Percentage of enrolled Students [%]","geo":""}).add_hline(y= 53,annotation_text="Average",annotation_position="right").update_layout(yaxis=dict(dtick=10),legend_title = "")

            plot = dcc.Graph(figure=fig1)
            middle = html.Div([block(markdown,plot)

            ])
        case 2:
            RQ5 =rq3
            
            RQ5 = RQ5.groupby(['Field of Education', 'Country']).sum(['Bachlor', 'Master', 'Total']).reset_index()
            RQ5_ger = RQ5[RQ5.Country == 'DE'].groupby(['Field of Education']).sum(['Bachlor', 'Master', 'Total']).reset_index()
            RQ5_rest = RQ5[RQ5.Country != 'DE'].groupby(['Field of Education']).sum(['Bachlor', 'Master', 'Total']).reset_index()

            fig_RQ5_PIES = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

            fig_RQ5_PIES.add_trace(
                go.Pie(
                    labels= RQ5_rest['Field of Education'],
                    values= RQ5_rest['Total'],
                    name = 'Rest of Europe',
                    title = dict(text='Rest of Europe',
                                font = dict(size=24)
                                ),
                    textfont=dict(size=12),
                    hole = 0.4,
                    sort = True,
                    direction="clockwise"
                ), 1, 1)

            fig_RQ5_PIES.add_trace(
                go.Pie(
                    labels= RQ5_ger['Field of Education'],
                    values= RQ5_ger['Total'],
                    name = 'Germany',
                    title = dict(text='Germany',
                                font=dict(size=24)
                                ),
                    textfont=dict(size=12),
                    hole = 0.4,
                    sort=True,
                    direction="clockwise"
                ), 1, 2)

            markdown = dcc.Markdown()
            plot = dcc.Graph(figure=fig_RQ5_PIES)
            middle = html.Div([block(markdown,plot)])
        case 3:
            markdown = dcc.Markdown()

            df = enrolled_age
            df = df.groupby(["geo","age","age_numeric"]).sum().reset_index()

            t = df[df["geo"] != "Germany"]
            tg = df[df["geo"] == "Germany"]

            tg["value"] = -tg["value"]

            tg = pd.concat([t,tg])
            tg= tg.sort_values(by="age_numeric").reset_index(drop=True)

            data_plot = px.bar( tg,x="value", y="age",color="geo", orientation = "h", range_y=[8, 52],labels={"value":"students","age":"age group"},title="Enrollment by Age per Country (2019)")
            data_plot.update_layout(yaxis=dict(dtick=2),)
            data_plot.add_hrect(y0="48.5", y1="52", 
                        annotation_text="groups of 5 years",
                        fillcolor="gray", opacity=0.25, line_width=0)
            plot = dcc.Graph(figure=data_plot)
            middle = html.Div([block(markdown,plot)])
        case 4:

            dfb = europe_enrolled
            dfm = europe_enrolledMaster

            dfk = pd.concat([dfb,dfm])
            dfk = dfk.drop(columns=["isced11"])

            dfg = dfk[dfk["geo"] == "Germany"]
            dfr = dfk[dfk["geo"] != "Germany"]
            
            dfg = dfg.groupby(by=["sex","iscedf13"]).sum().reset_index()
            dfr = dfr.groupby(by=["sex","iscedf13"]).sum().reset_index()

            dfg["geo"] = "Germany"          
            dfr["geo"] = "Europe"
            
            dfk = pd.concat([dfg,dfr])
            
            dfk = dfk[dfk["sex"] != "Males"]

            dfk = pd.merge(dfk[dfk["sex"] != "Total"],dfk[dfk["sex"] == "Total"],on=["geo","iscedf13"],suffixes=("","_Total"))

            dfk["%"] = dfk["value"] / dfk["value_Total"]

            dfk = dfk[dfk["iscedf13"] != "Generic programmes and qualifications"]


            fig = px.line_polar(dfk,r=(dfk["%"]*100),
                                theta="iscedf13",
                                color ="geo",
                                line_close=True,
                                title="Females in academic fields [%]").update_traces(fill="toself").update_polars(
                                    angularaxis_color="blue",
                                    angularaxis_showgrid=True,
                                    radialaxis_gridwidth=1,
                                    gridshape='linear',
                                    radialaxis_showticklabels=True,
                                    angularaxis_tickfont_color="black",
                                    angularaxis_tickfont_size=12,
                                    radialaxis_color="black",
                                    radialaxis=dict(
                                        showline=True,
                                        linecolor="black",   
                                        gridcolor="black",    
                                        tickfont_size= 10),                    
                                    angularaxis=dict(
                                        showline=True,
                                        linecolor="black",  
                                        gridcolor="black",    
                                ))







            markdown = dcc.Markdown()
            plot = dcc.Graph(figure = fig)
            middle = html.Div([block(markdown,plot)])
        case 5:
            markdown = dcc.Markdown()
            plot = dcc.Graph()
        case _:
            markdown = dcc.Markdown()
            plot = dcc.Graph()

        
    return [] + [header] + [middle] 

@callback(Output('memory-output', 'data'), Input('geojson', 'clickData'))
def filter_country(feature):
    if not feature:
        #dff = europe_enrolled[europe_enrolled['geo'] == "Germany"]
        return None
    countryName= feature["properties"]["name"]
    return {"records":countryName}


@callback(Output('memory-graph', 'figure'), Input('memory-output', 'data'), Input('memory-field', 'value'))
def update_graph(data, field):
    if data is None:
        return no_update
    
    match field:
        case "Enrollment by field (Bachelor)":
            dff = europe_enrolled[europe_enrolled['geo'] == data["records"]] 
            dff = dff[dff["sex"] == "Total"]
            dff = dff[dff["time"] == 2023 ]
            dff = dff[dff["iscedf13"] != "Total"]
            return px.pie(
                dff,
                names="iscedf13",
                values="value",
                title= "Enrollment rate by field (2023)",
            )
        case "Enrollment by field (Master)":
            dff = europe_enrolledMaster[europe_enrolledMaster['geo'] == data["records"]] 
            dff = dff[dff["sex"] == "Total"]
            dff = dff[dff["time"] == 2023 ]
            dff = dff[dff["iscedf13"] != "Total"]
            return px.pie(
                dff,
                names="iscedf13",
                values="value",
                title= "Enrollment rate by field (2023)",
            )        
        case "Enrollment by Gender (Bachelor)":
            dff = europe_enrolled[europe_enrolled['geo'] == data["records"]] 
            dff = dff[dff["iscedf13"] == "Total"]
            dff = dff[dff["sex"] != "Total"]
            return px.bar(
                dff,
                x= "time",
                y="value",
                color="sex",
                barmode="group",
                range_y=[0,1300000],
                title="Total number of enrolled students by gender",
                labels={"time":"year","value":"enrolled students"}
            ).update_layout(xaxis= dict(dtick =1))
        case "Enrollment by Gender (Master)":
            dff = europe_enrolledMaster[europe_enrolledMaster['geo'] == data["records"]] 
            dff = dff[dff["iscedf13"] == "Total"]
            dff = dff[dff["sex"] != "Total"]
            return px.bar(
                dff,
                x= "time",
                y="value",
                color="sex",
                barmode="group",
                range_y=[0,1300000],
                title="Total number of enrolled students by gender",
                labels={"time":"year","value":"enrolled students"}
            ).update_layout(xaxis= dict(dtick =1))
        
        case "Enrollment by Age Group (Bachelor)":
            df = enrolled_age[enrolled_age["geo"]==data["records"]]
            df = df[df["isced11"] == "Bachelor's or equivalent level"]
            df = df[df["sex"] != "Total"]
            data_plot = px.bar( df,x="value", y="age",color="sex", orientation = "h", range_y=[8, 52],labels={"value":"students","age":"age group"},title="Enrollment by Age (Bachelor level ,2019)")
            data_plot.update_layout(yaxis=dict(dtick=2),)
            data_plot.add_hrect(y0="48.5", y1="52", 
                        annotation_text="groups of 5 years",
                        fillcolor="gray", opacity=0.25, line_width=0)
            return data_plot
        
        case "Enrollment by Age Group (Master)":
            df = enrolled_age[enrolled_age["geo"]==data["records"]]
            df = df[df["isced11"] == "Master's or equivalent level"]
            df = df[df["sex"] != "Total"]
            data_plot = px.bar( df,x="value", y="age",color="sex", orientation = "h", range_y=[8, 52],labels={"value":"students","age":"age group"},title="Enrollment by Age (Master level ,2019)")
            data_plot.update_layout(yaxis=dict(dtick=2),)
            data_plot.add_hrect(y0="48.5", y1="52", 
                        annotation_text="groups of 5 years",
                        fillcolor="gray", opacity=0.25, line_width=0)
            return data_plot
        
        case "Rate of master's to bachelor's graduates by field":

            countryCode = NameToCode[data["records"]]
            rq = rq1
            rq = rq[rq["Country"] == countryCode]
            rq= rq.transpose()[1:]
            rq= rq.rename(columns={rq.columns[0]:"snd"})

            return px.bar(rq,x=rq.index,y=(rq["snd"]*100),labels={"y":"Rate [%]","index":"Field"},title="Rate of master's to bachelor's graduates (2019)",range_y=[0,150])
            

    

@callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return tab1
    elif tab == 'tab-2':
        return tab2



@callback(Output("info", "children"), Input("geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)

@callback(Output("europe_stats","children"),Input("geojson","clickData"))
def country_click(feature):
    return updateCountry(feature)



if __name__ == '__main__':
    app.run(debug=True)
    