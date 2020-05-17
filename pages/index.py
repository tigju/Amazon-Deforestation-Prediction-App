# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd
import geojson
import shapely.geometry
import json
import plotly.graph_objects as go

# Imports from this application
from app import app

########### getting data
annual_increase_deforestation_2008_2018 = pd.read_csv('./amazon/df_2008_2018.csv')
states_amazon = gpd.read_file('./amazon/states_amazon/states_amazon_biome.shp')

# coordinate referene system WGS84 Latitude/Longitude: "EPSG:4326"

def coord_ref(df):
    # copy df
    X = df.copy()
    
    # convert coordinates
    X = X.to_crs("EPSG:4326")
    
    return X

df_samps = [states_amazon]

for df in df_samps:
    coord_ref(df)

#############################################################

# Working with polygons

# convert to json and make it str
states = json.dumps(shapely.geometry.mapping(states_amazon))
# convert str to geojson
states_geojson = geojson.loads(states)

# set the locations id matching to polygon id length
states_names_locations_id = [k for k in range(0,9)]

#######################################################

## for chloropleth mapbox usage
mapboxt = open("./amazon/token.txt").read()

####### Data Preparation and break down 

df_2008_2018 = annual_increase_deforestation_2008_2018.copy()
areakm_by_year = pd.DataFrame([df_2008_2018.groupby('year')['areakm_squared'].sum()])
areakm_by_year = areakm_by_year.T
areakm_by_state = pd.DataFrame([df_2008_2018.groupby('states')['areakm_squared'].sum()])
areakm_by_state = areakm_by_state.T
areakm_by_state = areakm_by_state.reset_index()
areakm_by_state_year = pd.DataFrame([df_2008_2018.groupby(['states', 'year'])['areakm_squared'].sum()])
areakm_by_state_year = areakm_by_state_year.stack()
areakm_by_state_year = areakm_by_state_year.T
areakm_by_state_year = areakm_by_state_year.reset_index()

areakm_by_state_year = pd.DataFrame({'states': ['Acre', 'Amapa', 'Amazonas', 'Maranhao', 'Mato Grosso', 'Para', 'Rondonia', 'Roraima', 'Tocantins'],
                                    '2008': areakm_by_state_year[('areakm_squared', 2008)],
                                     '2009': areakm_by_state_year[('areakm_squared', 2009)],
                                     '2010': areakm_by_state_year[('areakm_squared', 2010)],
                                     '2011': areakm_by_state_year[('areakm_squared', 2011)],
                                     '2012': areakm_by_state_year[('areakm_squared', 2012)],
                                     '2013': areakm_by_state_year[('areakm_squared', 2013)],
                                     '2014': areakm_by_state_year[('areakm_squared', 2014)],
                                     '2015': areakm_by_state_year[('areakm_squared', 2015)],
                                     '2016': areakm_by_state_year[('areakm_squared', 2016)],
                                     '2017': areakm_by_state_year[('areakm_squared', 2017)],
                                     '2018': areakm_by_state_year[('areakm_squared', 2018)]
                   })

areakm_states_years = areakm_by_state_year.merge(areakm_by_state, on='states', left_index=True) 

# df_2008 = df_2008_2018[df_2008_2018['year'] == 2008]
# df_2008_2009 = df_2008_2018[df_2008_2018['year'] <= 2009]
# df_2008_2010 = df_2008_2018[df_2008_2018['year'] <= 2010]
# df_2008_2011 = df_2008_2018[df_2008_2018['year'] <= 2011]
# df_2008_2012 = df_2008_2018[df_2008_2018['year'] <= 2012]
# df_2008_2013 = df_2008_2018[df_2008_2018['year'] <= 2013]
# df_2008_2014 = df_2008_2018[df_2008_2018['year'] <= 2014]
# df_2008_2015 = df_2008_2018[df_2008_2018['year'] <= 2015]
# df_2008_2016 = df_2008_2018[df_2008_2018['year'] <= 2016]
# df_2008_2017 = df_2008_2018[df_2008_2018['year'] <= 2017]

# df_2009 = df_2008_2018[df_2008_2018['year'] <= 2009]
# df_2010 = df_2008_2018[df_2008_2018['year'] == 2010]
# df_2011 = df_2008_2018[df_2008_2018['year'] == 2011]
# df_2012 = df_2008_2018[df_2008_2018['year'] == 2012]
# df_2013 = df_2008_2018[df_2008_2018['year'] == 2013]
# df_2014 = df_2008_2018[df_2008_2018['year'] == 2014]
# df_2015 = df_2008_2018[df_2008_2018['year'] == 2015]
# df_2016 = df_2008_2018[df_2008_2018['year'] == 2016]
# df_2017 = df_2008_2018[df_2008_2018['year'] == 2017]
# df_2018 = df_2008_2018[df_2008_2018['year'] == 2018]


areakm_2008_2009 = areakm_states_years['2008'] + areakm_states_years['2009']
areakm_2008_2010 = areakm_2008_2009 + areakm_states_years['2010']
areakm_2008_2011 = areakm_2008_2010 + areakm_states_years['2011']
areakm_2008_2012 = areakm_2008_2011 + areakm_states_years['2012']
areakm_2008_2013 = areakm_2008_2012 + areakm_states_years['2013']
areakm_2008_2014 = areakm_2008_2013 + areakm_states_years['2014']
areakm_2008_2015 = areakm_2008_2014 + areakm_states_years['2015']
areakm_2008_2016 = areakm_2008_2015 + areakm_states_years['2016']
areakm_2008_2017 = areakm_2008_2016 + areakm_states_years['2017']
areakm_2008_2018 = areakm_2008_2017 + areakm_states_years['2018']


# increasing_areakm = pd.DataFrame({'states': areakm_states_years['states'],
#                                   '2008': areakm_states_years['states'],
#                                   '2008_2009': areakm_2008_2009,
#                                   '2008_2010': areakm_2008_2010,
#                                   '2008_2011': areakm_2008_2011,
#                                   '2008_2012': areakm_2008_2012,
#                                   '2008_2013': areakm_2008_2013,
#                                   '2008_2014': areakm_2008_2014,
#                                   '2008_2015': areakm_2008_2015,
#                                   '2008_2016': areakm_2008_2016,
#                                   '2008_2017': areakm_2008_2017,
#                                   '2008_2018': areakm_2008_2018}
#                                   )
#################################################################

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Can We predict Amazon Deforestation?


            ### Introduction
            Deforestation is the clearing, destroying, or otherwise removal of trees due to farming, 
            mostly cattle due to its quick turn around, logging, for materials and development, mining, 
            and drilling combined responsible for more than half of all deforestation.
            
            Over the past 50 years, nearly 17 percent of the Amazon rainforest has been lost and losses 
            have recently been on the rise.

            There is a tendency that deforestation is happening close to deforested areas in the past, and we 
            will try to predict the locations of future area where deforestation is most likely to occur.


            """
        ),
        dcc.Link(dbc.Button('Lets Predict', color='primary'), href='/predictions')
    ],
    md=4,
)

trace = [
        go.Choroplethmapbox(z=areakm_2008_2018,
                            locations=states_names_locations_id,
                            colorscale='blues',
                            name='Deforested area by state in km^2',
                            showlegend=True,
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson=states_geojson,
                            text=areakm_states_years['states'],
                            hoverinfo='all',
                            marker_line_width=0.1, marker_opacity=0.7),
                            
         
        go.Scattermapbox(lat=df_2008_2018['lat'],
                          lon=df_2008_2018['lon'], 
                          name='Location of deforested area',
                          showlegend=True,
                          mode='markers',
                          text=df_2008_2018['areakm_squared'],
                          hoverinfo='all',
                          marker=go.scattermapbox.Marker(
                          size=2,
                          color='#E51313',
                          opacity=1))
        ]
                            
                            
layout = go.Layout(title_text= 'Amazon Deforestation 2008-2018',
                   title_x=0.1, width = 800, height=580,
                   mapbox = dict(center= dict(lat=-5.977402,  lon=-58.97948),
                                 accesstoken= mapboxt,
                                 zoom=3.7,
                               ))

fig = go.Figure(data=trace, layout =layout)

fig.data[0].hovertemplate =  '<b>State</b>: <b>%{text}</b>'+\
                              '<br> <b>Total deforestation in km^2</b>: %{z}<br>'
fig.data[1].hovertemplate =  '<b>Area deforested in km^2</b>: <b>%{text:.4f}</b>'+\
                              '<br>'
fig.update_layout(mapbox_style = "streets")
fig.update_layout(showlegend=True, legend=dict(x=0.7, y=1.17))

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ],
    md=6,
)

layout = dbc.Row([column1, column2])