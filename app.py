import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
########### Define your variables
tabtitle='SERF: Systematic Testing'
#### Import Fit Data
ALL_data_fit_values = pd.read_csv('https://raw.githubusercontent.com/rach6230/Dash_app_Systematic_Testing/main/Full_fit_Data.csv')
# Create col of A/C:
ALL_data_fit_values["V/nT"] =  abs(ALL_data_fit_values['A'])/abs(ALL_data_fit_values['C'])
## Load data
df2 = ALL_data_fit_values
## PP slider values
S_MIN = min(df2['PP'])
S_MAX = max(df2['PP'])
S_STEP = (S_MIN+S_MAX)/1000
## MSE slider values
MSE_MIN = min(df2['MSE'])
MSE_MAX = max(df2['MSE'])
MSE_STEP = (MSE_MIN+MSE_MAX)/1000
## Colour values
colors = {
    'background': '#f2f2f2',
    'text': '#7FDBFF'
}
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
                      style={'backgroundColor': colors['background']},
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
                          marks={60: {'label': '60 °C', 'style': {'color': '#77b0b1'}},
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
                          marks={70: {'label': '70', 'style': {'color': '#77b0b1'}},
                                 140: {'label': '140'},
                                 210: {'label': '210'},
                                 280: {'label': '280'},
                                 350: {'label': '350', 'style': {'color': '#f50'}}
                                }
                        ),
                        html.Div(id='LD_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                        dcc.RangeSlider(id='LD-range-slider',
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
                        dcc.RangeSlider(id='vnt-range-slider',
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
                                     marks={S_MIN: {'label': '0 %', 'style': {'color': '#77b0b1'}},
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
                      ]
                     ),  # Define the 1st column
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
                        html.Br(), #new lin
                      ]
                     )  # Define the 3rd column
           ]
          )
]
)
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
@@ -227,7 +230,22 @@
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
