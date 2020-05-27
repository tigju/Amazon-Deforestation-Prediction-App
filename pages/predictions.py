from joblib import load
pipeline1 = load('assets/xgb1.joblib')
pipeline2 = load('assets/xgb2.joblib')
# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import category_encoders as ce
import plotly.graph_objects as go

# Imports from this application
from app import app

## for chloropleth mapbox usage
mapboxt = open("./amazon/token.txt").read()

# style for controls
style = {'padding': '1.5em'}

# controls start here 
layout = html.Div([
    dcc.Markdown("""
        ### Predict
        Use the controls below to update your predicted location, based on 
        area in km^2, day, month, year and state.
        *(Predictions based on sample dataset using XGboost model. Check the [Process](https://amazon-deforestation.herokuapp.com/process) page why.)*
    """),
html.Div([
        dcc.Markdown('###### Area in km^2'),
        dcc.Slider(
            id='area',
            min=0.062,
            max=1.440,
            step=0.040,
            value=0.090,
            marks={n: f'{n:.2f}' for n in np.arange(0.006, 1.440, 0.040)}
        ),
    ], style=style),
html.Div([
        dcc.Markdown('###### Day'),
        dcc.Slider(
            id='day',
            min=1,
            max=30,
            step=1,
            value=25,
            marks={n: str(n) for n in range(1, 31, 1)}
        ),
    ], style=style),
html.Div([
        dcc.Markdown('###### Month'),
        dcc.Slider(
            id='month',
            min=1,
            max=12,
            step=1,
            value=7,
            marks={n: str(n) for n in range(1, 13, 1)}
        ),
    ], style=style),
html.Div([
        dcc.Markdown('###### Year'),
        dcc.Slider(
            id='year',
            min=2008,
            max=2025,
            step=1,
            value=2017,
            marks={n: str(n) for n in range(2008, 2025, 1)}
        ),
    ], style=style),
html.Div([
        dcc.Markdown('###### State'),
        dcc.Dropdown(
            id='state',
            options=[{'label': state, 'value': state} for state in ['Para', 'Mato Grosso', 'Rondonia', 'Amazonas','Maranhao', 'Acre', 'Roraima', 'Amapa', 'Tocantins']],
            value='Para'
        ),
    ], style=style),
# Scatter mapbox plot with predictions
html.Div([
        dcc.Graph(id='graph')
    ],
    style=style)
])

# get the inputs
@app.callback(
    # Output(component_id='prediction-content',  component_property='children'),
    Output(component_id='graph',  component_property='figure'),
    [Input(component_id='area', component_property='value'),
     Input(component_id='day', component_property='value'),
     Input(component_id='month', component_property='value'),
     Input(component_id='year', component_property='value'),
     Input(component_id='state', component_property='value')])
# apply model

def predict(area, day, month, year, state):

    df = pd.DataFrame(
        columns=['areakm_squared', 'day', 'month', 'year', 'states'],
        data=[[area, day, month, year, state]])

    
    y_pred_1 = pipeline1.predict(df)[0]
    y_pred_2 = pipeline2.predict(df)[0]
    # print(y_pred_1)
    # print(y_pred_2)

    results = [y_pred_1, y_pred_2]
    graphing = {
            'data': [{
                'type': 'scattermapbox',
                'lat': [results[0]],
                'lon': [results[1]],
                'name':'Predicted location of deforested area',
                'showlegend': True,
                'mode': 'markers',
                'hoverinfo': 'all',
                'text':f'predicted location latitude:{results[0]}, longitude:{results[1]}',
                'marker':go.scattermapbox.Marker(
                          size=30,
                          color='#E51313',
                          opacity=0.8),
                'hovertemplate': f'Predicted location: latitude:{results[0]:.4f}, longitude:{results[1]:.4f} with {area} km^2'
            }],
            'layout': go.Layout(title_text= f'Predictions for state <b>{state}</b><br> latitude:<b>{results[0]:.4f}</b>, longitude:<b>{results[1]:.4f}</b> with <b>{area}</b> km^2',
                    title_x=0.05, width =1000, height=660,
                    mapbox = dict(center= dict(lat=-5.977402,  lon=-58.97948),
                                  accesstoken= mapboxt,
                                  pitch=0,
                                  zoom=4,
                                  style='light'
                                ),
                    mapbox_style = "streets",
                    showlegend=True,
                    legend=dict(x=0.7, y=1.15))

            
        }
    return go.Figure(data=graphing['data'], layout=graphing['layout'])
 