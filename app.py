import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
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
##fig = px.scatter_3d(df2, x='Temp', y='Laser_Detuning', z='Laser_Power',
##                   color='V/nT')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
## PP slider values
S_MIN = min(df2['PP'])
S_MAX = max(df2['PP'])
S_STEP = (S_MIN+S_MAX)/1000

## MSE slider values
MSE_MIN = min(df2['MSE'])
MSE_MAX = max(df2['MSE'])
MSE_STEP = (MSE_MIN+MSE_MAX)/1000

#Empty layout
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                   html.Div(className='three columns div-for-charts',
                                            children = [
                                                html.H6('Filters'),
                                                html.P('Parameter Range:'),
                                                html.Div(id='TEMP_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                                                dcc.RangeSlider(
                                                   id='temp-range-slider',
                                                   min=df2['Temp'].min(),
                                                   max=df2['Temp'].max(),
                                                   step=1,
                                                   value=[df2['Temp'].min(), df2['Temp'].max()],
                                                   marks={
                                                       60: {'label': '60 °C', 'style': {'color': '#77b0b1'}},
                                                       80: {'label': '80 °C'},
                                                       100: {'label': '100 °C'},
                                                       120: {'label': '120°C', 'style': {'color': '#f50'}}
                                                   }
                                                ),
                                                html.Div(id='LP_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                                                dcc.RangeSlider(
                                                   id='LP-range-slider',
                                                   min=df2['Laser_Power'].min(),
                                                   max=df2['Laser_Power'].max(),
                                                   step=1,
                                                   value=[df2['Laser_Power'].min(), df2['Laser_Power'].max()],
                                                   marks={
                                                       70: {'label': '70', 'style': {'color': '#77b0b1'}},
                                                       140: {'label': '140'},
                                                       210: {'label': '210'},
                                                       280: {'label': '280'},
                                                       350: {'label': '350', 'style': {'color': '#f50'}}
                                                   }
                                                ),
                                                html.Div(id='LD_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                                                dcc.RangeSlider(
                                                   id='LD-range-slider',
                                                   min=-35,
                                                   max=(df2['Laser_Detuning'].max())+1,
                                                   step=1,
                                                   value=[df2['Laser_Detuning'].min(), 15],
                                                   marks={
                                                       -35: {'label': '-35', 'style': {'color': '#77b0b1'}},
                                                       -22.5: {'label': '-22.5'},
                                                       -10: {'label': '-10'},
                                                       2.5: {'label': '2.5'},
                                                       15: {'label': '15', 'style': {'color': '#f50'}}
                                                   }
                                                ),
                                                html.Div(id='vnt_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                                                dcc.RangeSlider(
                                                   id='vnt-range-slider',
                                                   min=df2['V/nT'].min(),
                                                   max=df2['V/nT'].max(),
                                                   step=1,
                                                   value=[df2['V/nT'].min(), df2['V/nT'].max()],
                                                   marks={
                                                       df2['V/nT'].min(): {'label': 'Min', 'style': {'color': '#77b0b1'}},
                                                       df2['V/nT'].max(): {'label': 'Max', 'style': {'color': '#f50'}}
                                                   }
                                                ),
                                                html.Br(), #new line
                                                html.P('Error:'),
                                                html.Div(id='PP_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                                               dcc.Slider(id='PP-slider',
                                                          min=S_MIN,
                                                          max=S_MAX,
                                                          step=S_STEP,
                                                          value=S_MAX,
                                                          marks={
                                                              S_MIN: {'label': '0 %', 'style': {'color': '#77b0b1'}},
                                                              S_MAX*0.25: {'label': '25 %'},
                                                              S_MAX*0.5: {'label': '50 %'},
                                                              S_MAX*0.75: {'label': '75 %'},
                                                              S_MAX: {'label': '100%', 'style': {'color': '#f50'}}
                                                          }
                                                         ),
                                               html.Div(id='MSE_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                                               dcc.Slider(id='MSE-slider',
                                                          min=MSE_MIN,
                                                          max=MSE_MAX,
                                                          step=MSE_STEP,
                                                          value=MSE_MAX,
                                                          marks={
                                                              0: {'label': '0 °C', 'style': {'color': '#77b0b1'}},
                                                              MSE_MAX*0.25: {'label': '25 %'},
                                                              MSE_MAX*0.5: {'label': '50 %'},
                                                              MSE_MAX*0.75: {'label': '75 %'},
                                                              MSE_MAX: {'label': '100%', 'style': {'color': '#f50'}}
                                                          }
                                                         )
                                            ]),  # Define the 1st column
                                  html.Div(className='nine columns div-for-charts',
                                           children = [
                                               html.H6('All Data'),
                                               dcc.Graph(id='graph-with-slider',config={'displayModeBar': False}),
                                               html.H6('Selected Data'),
                                               html.Div(id='click-data', style={'fontSize': 12}),
                                               html.P('Fit Values'),
                                               dash_table.DataTable(id='my-table',
                                                                    style_cell={'textAlign': 'left', 'font_size': '10px'},
                                                                    columns=[{"name": i, "id": i} for i in df2.columns[0:14]]),
                                                                    #data=row.to_dict('records')),
                                               html.Br(), #new line
                                               html.P('Raw Data'),
                                               dcc.Graph(id='facet',config={'displayModeBar': False})

                                           ])  # Define the 3rd column
                                  ])
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

## Call back for PP slider indicator
@app.callback(Output('PP_slider-drag-output', 'children'),
              [Input('PP-slider', 'value')])
def display_value(value):
    return 'PP Value = {}'.format(value)

## Call back for MSE slider indicator
@app.callback(Output('MSE_slider-drag-output', 'children'),
              [Input('MSE-slider', 'value')])
def display_value(value):
    return 'MSE Value = {}'.format(value)

## Call back for TEMP slider indicator
@app.callback(Output('TEMP_slider-drag-output', 'children'),
              [Input('temp-range-slider', 'value')])
def display_value(value):
    low = value[0]
    high = value[1]
    return 'Temperature = {} to {}°C'.format(low, high)

## Call back for lp slider indicator
@app.callback(Output('LP_slider-drag-output', 'children'),
              [Input('LP-range-slider', 'value')])
def display_value(value):
    low = value[0]
    high = value[1]
    return 'Laser Power = {} to {}μW'.format(low, high)

## Call back for LD slider indicator
@app.callback(Output('LD_slider-drag-output', 'children'),
              [Input('LD-range-slider', 'value')])
def display_value(value):
    low = value[0]
    high = value[1]
    return 'Laser Detuning = {} to {}GHz'.format(low, high)

## Call back for LD slider indicator
@app.callback(Output('vnt_slider-drag-output', 'children'),
              [Input('vnt-range-slider', 'value')])
def display_value(value):
    low = value[0]
    high = value[1]
    return 'V/nt = {} to {}'.format(low, high)

## Call back for updating the 3D graph
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('PP-slider', 'value'),
    Input('MSE-slider', 'value'),
    Input('temp-range-slider', 'value'),
    Input('LP-range-slider', 'value'),
    Input('LD-range-slider', 'value'),
    Input('vnt-range-slider', 'value'))
def update_figure(PP, MSE, TEMP, LP, LD, vnt):
    filtered_df = df2[(df2['PP']< PP)&(df2['MSE']< MSE)&
                      (df2['Temp']<= TEMP[1])&(df2['Temp']>= TEMP[0])&
                      (df2['V/nT']<= vnt[1])&(df2['V/nT']>= vnt[0])&
                      (df2['Laser_Power']<= LP[1])&(df2['Laser_Power']>= LP[0])&
                      (df2['Laser_Detuning']<= LD[1])&(df2['Laser_Detuning']>= LD[0])]
    fig = px.scatter_3d(filtered_df, y='Temp', z='Laser_Detuning', x='Laser_Power', color='V/nT')
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_layout(transition_duration=500)
    fig.update_layout(height=300)
    return fig

## Callback for table
@app.callback(
    Output("my-table", "data"),
    Input('graph-with-slider', 'clickData'))
def on_trace_click(clickData):
    if clickData!= None:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
        vnt = clickData['points'][0]['marker.color']
        x = clickData['points'][0]['pointNumber']
        filtered_df = df2[(df2['Temp']== temp)&
                      (df2['Laser_Power']== lp)&
                      (df2['Laser_Detuning']== ld)]
        row = filtered_df
        return row.to_dict('records')

if __name__ == '__main__':
    app.run_server()
