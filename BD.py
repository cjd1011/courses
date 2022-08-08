#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#video es : 

import pandas as pd #(version 0.24.2)
import datetime as dt
import dash         #(version 1.0.0)
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly       #(version 4.4.1)
import plotly.express as px

df = pd.read_excel("BD Ventas.xlsx",sheet_name = "BD") #groupby 


app = dash.Dash(__name__)

app.layout = html.Div([

        html.Div([
            html.Pre(children= "TECH SAS - TOTAL SALES", 
            style={"text-align": "center", "font-size":"100%", "color":"black"}) #Title
        ]),

        html.Div([
            html.Label(['X-axis categories to compare:'],style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[
                         {'label': 'Year', 'value': 'Año'},
                         {'label': 'Month', 'value': 'Mes'},
                         {'label': 'Customer', 'value': 'Cliente'},
                         {'label': 'Product', 'value': 'Producto'},
                ],
                value='Año',
                style={"width": "50%"} #X- Axis
            ),
        ]),
    
        html.Div([
            html.Br(),
            html.Label(['Y-axis values to compare:'], style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='yaxis_raditem',
                options=[
                         {'label': 'Quantity', 'value': 'Compras'},
                         {'label': 'Total Value', 'value': 'Valor'},
                         
                ],
                value='Valor',
                style={"width": "50%"} #Y - Axis
            ),
        ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)

def update_graph(x_axis, y_axis):

    dff = df
    # print(dff[[x_axis,y_axis]][:1])

    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+': by '+x_axis,
            #facet_col='Cliente',
            color='Producto',
            #barmode='group',
            )

    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})

    return (barchart)

if __name__ == '__main__':
    app.run_server(debug=True)

