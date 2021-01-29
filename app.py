import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px

########### Define your variables
mytitle='Beer Comparison'
tabtitle='SERF: Systematic Testing'
myheading='Flying Dog Beers'

#### Import Fit Data
ALL_data_fit_values = pd.read_csv('https://raw.githubusercontent.com/rach6230/Dash_app_Systematic_Testing/main/Full_fit_Data.csv')
# Create col of A/C:
ALL_data_fit_values["V/nT"] =  abs(ALL_data_fit_values['A'])/abs(ALL_data_fit_values['C'])
## Load data
df2 = ALL_data_fit_values
######
fig = px.scatter_3d(df2, x='Temp', y='Laser_Detuning', z='Laser_Power',
                   color='V/nT')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle
########### Set up the layout
#Empty layout
app.layout = html.Div(children=[
  html.Div(className='row',  # Define the row elemen
           children=[
             html.Div(className='three columns div-for-charts',
                      children = [
                        html.H6('Filters'),
                        html.P('Parameter Range:'),
                      ]
                     ),  # Define the 1st column
             html.Div(className='nine columns div-for-charts',
                      children = [
                        html.H6('All Data'),
                        dcc.Graph(id='graph-with-slider',config={'displayModeBar': False}, figure = fig),
                        html.H6('Selected Data'),
                        html.Div(id='click-data', style={'fontSize': 12}),
                        html.P('Fit Values'),
                        html.Br(), #new lin
                      ]
                     )  # Define the 3rd column
           ]
          )
])

## Callback for selected data text
@app.callback(
  Output('click-data', 'children'),
  Input('graph-with-slider', 'clickData'))
def display_click_data(clickData):
  if clickData == None:
    A = "Select data point"
  else:
    temp = clickData['points'][0]['y']
    lp = clickData['points'][0]['x']
    ld = clickData['points'][0]['z']
    vnt = clickData['points'][0]['marker.color']
    A = 'Temperature ={}°C, Laser Power = {}μW, Laser Detuning = {}GHz, V/nT = {}'.format(temp, lp, ld, vnt)
return A

if __name__ == '__main__':
    app.run_server()
