import pandas as pd
import dash

from dash import dcc
from dash import html
from dash.dependencies import Input,Output

import plotly.express as px


app = dash.Dash(__name__)
server = app.server