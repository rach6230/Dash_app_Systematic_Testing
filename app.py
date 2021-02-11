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
#V2
ALL_data_fit_values_v2 = pd.read_csv('https://raw.githubusercontent.com/rach6230/Dash_app_Systematic_Testing/main/Full_fit_Data_V2.csv')

# Create col of A/C:
ALL_data_fit_values["V/nT"] =  abs(ALL_data_fit_values['A'])/abs(ALL_data_fit_values['C'])
ALL_data_fit_values["SE"] =  abs(ALL_data_fit_values['G2'])-abs(ALL_data_fit_values['G1'])
#V2
ALL_data_fit_values_v2["V/nT"] =  abs(ALL_data_fit_values_v2['A'])/abs(ALL_data_fit_values_v2['C'])
ALL_data_fit_values_v2["SE"] =  abs(ALL_data_fit_values_v2['G2'])-abs(ALL_data_fit_values_v2['G1'])

## Load data for sliders
df = ALL_data_fit_values

# File names
Github_urls_v1= pd.read_csv("https://raw.githubusercontent.com/rach6230/Dash_app_Systematic_Testing/main/Data_pt2/Github_urls_sorted.csv")
#v2
Github_urls_v2 = pd.read_csv("https://raw.githubusercontent.com/rach6230/Dash_app_Systematic_Testing/main/Version_2_Data_1/Github_urls_sortedV2.csv")


# Inital data to show (selected point)
x = 140

# PP slider values
if ALL_data_fit_values['PP'].max()>ALL_data_fit_values_v2['PP'].max():
    S_MAX = ALL_data_fit_values['PP'].max()
else:
    S_MAX = ALL_data_fit_values_v2['PP'].max()

if ALL_data_fit_values['PP'].min()<ALL_data_fit_values_v2['PP'].min():
    S_MIN = ALL_data_fit_values['PP'].min()
else:
    S_MIN = ALL_data_fit_values_v2['PP'].min()
S_STEP = (S_MIN+S_MAX)/1000

## MSE slider values
if ALL_data_fit_values['MSE'].max()>ALL_data_fit_values_v2['MSE'].max():
    MSE_MAX = ALL_data_fit_values['MSE'].max()
else:
    MSE_MAX = ALL_data_fit_values_v2['MSE'].max()

if ALL_data_fit_values['MSE'].min()<ALL_data_fit_values_v2['MSE'].min():
    MSE_MIN = ALL_data_fit_values['MSE'].min()
else:
    MSE_MIN = ALL_data_fit_values_v2['MSE'].min()
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
                          min=df['Temp'].min(),
                          max=df['Temp'].max(),
                          step=1,
                          value=[df['Temp'].min(), df['Temp'].max()],
                          marks={60: {'label': '60 °C', 'style': {'color': '#77b0b1'}},
                                 80: {'label': '80 °C'},
                                 100: {'label': '100 °C'},
                                 120: {'label': '120°C', 'style': {'color': '#f50'}}
                                }
                        ),
                        html.Div(id='LP_slider-drag-output', style={'margin-top': 20,'fontSize': 12}),
                        dcc.RangeSlider(
                          id='LP-range-slider',
                          min=df['Laser_Power'].min(),
                          max=df['Laser_Power'].max(),
                          step=1,
                          value=[df['Laser_Power'].min(), df['Laser_Power'].max()],
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
                                        max=(df['Laser_Detuning'].max())+1,
                                        step=1,
                                        value=[df['Laser_Detuning'].min(), 15],
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
                                        min=df['V/nT'].min(),
                                        max=df['V/nT'].max(),
                                        step=1,
                                        value=[df['V/nT'].min(), df['V/nT'].max()],
                                        marks={
                                          df['V/nT'].min(): {'label': 'Min', 'style': {'color': '#77b0b1'}},
                                          df['V/nT'].max(): {'label': 'Max', 'style': {'color': '#f50'}}
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
                                    ),
                          html.Br(), #new line
                          html.P('Data Set Details:'),
                          dcc.Markdown(id='Markdown_notes', style={'fontSize': 12}),
                      ]
                     ),  # Define the 1st column
             html.Div(className='five columns div-for-charts',
                      children = [
                        html.H6('All Parameter Space Data'),
                        dcc.Dropdown(
                            id='segselect',
                            options=[
                                {'label': 'Systematic Testing V1', 'value': 'ST1'},
                                {'label': 'Systematic Testing V2', 'value': 'ST2'},
                            ],
                            value='ST2'
                        ),     
                        dcc.RadioItems(
                            id='value_dropdown',
                            options=[{"label": i, "value": i} for i in df.columns[19:21]]+[{"label": i, "value": i} for i in df.columns[0:7]],
                            value='V/nT',
                            inputStyle={"margin-left": "20px"}, # add space between radio items
                            labelStyle={'display': 'inline-block'},
                            style={'fontSize': 12}
                        ),                            
                        dcc.Graph(id='graph-with-slider',config={'displayModeBar': False}),
                        html.Br(), #new line
                        html.H6('Single Parameter Space Point Data'),
                        html.Div(id='click-data', style={'fontSize': 12}),
                        html.P('Fit Values'),
                        dash_table.DataTable(id='my-table',
                                             style_cell={'textAlign': 'left', 'font_size': '10px'},
                                             columns=[{"name": i, "id": i} for i in df.columns[0:7]]),
                        html.Br(), #new line
                        html.P('Error Values'),  
                        dash_table.DataTable(id='my-table2',
                                             style_cell={'textAlign': 'left', 'font_size': '10px'},
                                             columns=[{"name": i, "id": i} for i in df.columns[7:14]]),  
                      ]
                     ),  # Define the 3rd column
               html.Div(className='four columns div-for-charts',
                        children = [
                            dcc.RadioItems(
                                id='value_dropdown_2',
                                options=[{"label": i, "value": i} for i in ["Hanle", "Plotter"]],
                                value='Hanle',
                                inputStyle={"margin-left": "20px"}, # add space between radio items
                                labelStyle={'display': 'inline-block'},
                                style={'fontSize': 12}
                                ), 
                            html.Div(id='hide_hanle_box',
                                     children = [
                                         html.H6('3-Axis Raw Data'),
                                         html.P('For Single Parameter Space Point', style={'fontSize': 12}),
                                         dcc.Graph(id='facet',config={'displayModeBar': False}),
                                         html.H6('Hanle'),
                                         html.Div(id='click-data-2', style={'fontSize': 12}),
                                         html.P('Transverse'),
                                         dcc.Graph(id='click-data-4',config={'displayModeBar': False}),
                                         html.P('Longitudinal'),
                                         dcc.Graph(id='click-data-3',config={'displayModeBar': False}),                           
                                         html.Br(), #new lin
                                     ]
                                    ),                            
                      ]
                     ),  # Define the 3rd column
           ]
          )
]
)

## Callback for hiding 3D hanle
@app.callback(
   Output('hide_hanle_box', 'style'),
   [Input('value_dropdown_2', 'value')])

def show_hide_element(visibility_state):
    if visibility_state == 'Hanle':
        return {'display': 'block'}
    if visibility_state == 'Plotter':
        return {'display': 'none'}

## Callbacks for selected data details
@app.callback(
  Output('Markdown_notes', 'children'),
  Input('segselect', 'value'))
def display_click_data(data_version):
  if data_version == 'ST1':
    A = '''
* **Testing type**: Systematic of all parameter space 
* **Heater Driver**: Audio Amp, 100kHz, Sine
* **Coil Drivers**: DAQ
* **Heaters**: 2x4.2 ohm thick film (magnetic)
* **Cell**: Cs
* **Notes**: Laser power not varying correctly during scans, all values taken at approx ~100uW'''
  else:
    A = '''
* **Testing type**: Systematic of all parameter space 
* **Heater Driver**: MOSFET, 150kHz, square
* **Coil Drivers**: DAQ
* **Heaters**: 2x4.2 ohm thick film (magnetic)
* **Cell**: Cs
* **Notes**: '''
  return A

## Callback for selected data text
@app.callback(
  Output('click-data', 'children'),
  Input('graph-with-slider', 'clickData'),
  Input('segselect', 'value'))
def display_click_data(clickData, data_version):
  if data_version == 'ST1':
    df2 = ALL_data_fit_values
  else:
    df2 = ALL_data_fit_values_v2
  if clickData == None:
    x = 140
    line = df2.iloc[x,] 
    lp = line[15]
    ld = line[16]
    temp = line[17]
    vnt = line[19]
    A = 'Temperature ={}°C, Laser Power = {}μW, Laser Detuning = {}GHz, V/nT = {}'.format(temp, lp, ld, vnt)
  else:
    temp = clickData['points'][0]['y']
    lp = clickData['points'][0]['x']
    ld = clickData['points'][0]['z']
    vnt = clickData['points'][0]['marker.color']
    A = 'Temperature ={}°C, Laser Power = {}μW, Laser Detuning = {}GHz, V/nT = {}'.format(temp, lp, ld, vnt)
  return A

## Call back for TEMP slider indicator
@app.callback(Output('TEMP_slider-drag-output', 'children'),
              [Input('temp-range-slider', 'value')]
             )
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
## Call back for vnt slider indicator
@app.callback(Output('vnt_slider-drag-output', 'children'),
              [Input('vnt-range-slider', 'value')])
def display_value(value):
  low = value[0]
  high = value[1]
  return 'V/nt = {} to {}'.format(low, high)
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
## Call back for updating the 3D graph
@app.callback(Output('graph-with-slider', 'figure'),
              Input('temp-range-slider', 'value'),
              Input('LP-range-slider', 'value'),
              Input('vnt-range-slider', 'value'),
              Input('LD-range-slider', 'value'),
              Input('PP-slider', 'value'),
              Input('MSE-slider', 'value'),
              Input('value_dropdown', 'value'),
              Input('segselect', 'value'))
def update_figure(TEMP, LP, vnt, LD, PP, MSE, col, data_version):
  if data_version == 'ST1':
    df2 = ALL_data_fit_values
  else:
    df2 = ALL_data_fit_values_v2    
  filtered_df = df2[(df2['PP']< PP)&(df2['MSE']< MSE)&
                    (df2['Temp']<= TEMP[1])&(df2['Temp']>= TEMP[0])&
                    (df2['Laser_Power']<= LP[1])&(df2['Laser_Power']>= LP[0])&
                    (df2['V/nT']<= vnt[1])&(df2['V/nT']>= vnt[0])&
                    (df2['Laser_Detuning']<= LD[1])&(df2['Laser_Detuning']>= LD[0])]
  fig = px.scatter_3d(filtered_df, y='Temp', z='Laser_Detuning', x='Laser_Power', color=col)
  fig.update_layout(margin={'l': 0, 'b': 0, 't': 10, 'r': 0}, hovermode='closest')
  fig.update_layout(transition_duration=500)
  fig.update_layout(height=300)
  fig.update_layout(scene = dict(
                    xaxis_title='Laser Power (μW)',
                    yaxis_title='Temperature (°C)',
                    zaxis_title='Laser_Detuning (GHz)'))
  return fig


## Callback for table
@app.callback(
    Output("my-table", "data"),
    Input('graph-with-slider', 'clickData'), 
    Input('segselect', 'value'))
def on_trace_click(clickData, data_version):
    if data_version == 'ST1':
        df2 = ALL_data_fit_values
    else:
        df2 = ALL_data_fit_values_v2
    if clickData== None:
        x = 140
        line = df2.iloc[x,] 
        lp = line[15]
        ld = line[16]
        temp = line[17]
        filtered_df = df2[(df2['Temp']== temp)&
                          (df2['Laser_Power']== lp)&
                          (df2['Laser_Detuning']== ld)]
        row = filtered_df
        return row.to_dict('records')
    else:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
        x = clickData['points'][0]['pointNumber']
        filtered_df = df2[(df2['Temp']== temp)&
                      (df2['Laser_Power']== lp)&
                      (df2['Laser_Detuning']== ld)]
        row = filtered_df
        return row.to_dict('records')
    
## Callback for error table
@app.callback(
    Output("my-table2", "data"),
    Input('graph-with-slider', 'clickData'), 
    Input('segselect', 'value'))
def on_trace_click(clickData, data_version):
    if data_version == 'ST1':
        df2 = ALL_data_fit_values
    else:
        df2 = ALL_data_fit_values_v2
    if clickData== None:
        x = 140
        line = df2.iloc[x,] 
        lp = line[15]
        ld = line[16]
        temp = line[17]
        filtered_df = df2[(df2['Temp']== temp)&
                          (df2['Laser_Power']== lp)&
                          (df2['Laser_Detuning']== ld)]
        row = filtered_df
        return row.to_dict('records')
    else:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
        x = clickData['points'][0]['pointNumber']
        filtered_df = df2[(df2['Temp']== temp)&
                      (df2['Laser_Power']== lp)&
                      (df2['Laser_Detuning']== ld)]
        row = filtered_df
        return row.to_dict('records')
    
## Call back for updating facet
@app.callback(
    Output('facet', 'figure'),
    Input('graph-with-slider', 'clickData'), 
    Input('segselect', 'value'))
def update_figure(clickData, data_version):
    if data_version == 'ST1':
        df2 = ALL_data_fit_values
        Github_urls = Github_urls_v1
    else:
        df2 = ALL_data_fit_values_v2 
        Github_urls = Github_urls_v2
    if clickData == None:
        x = 140
        line = df2.iloc[x,] 
        lp = line[15]
        ld = line[16]
        temp = line[17]
    else:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
    filtered_df = Github_urls[(Github_urls['Temp']== temp)]
    filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
    filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
    data_url = filtered_df3.iloc[0,0]
    df = pd.read_table(data_url)
    df.columns = df.iloc[0]
    df =df.iloc[1:]
    newdf = df.apply(pd.to_numeric)
    newdf["Z  Field (nT)"] = newdf["Z  Field (nT)"].round(2)
    fig = px.scatter(newdf, x="X  Field (nT)", y="Y  Field (nT)",
                     color="Photodiode Voltage (V)", facet_col="Z  Field (nT)",  facet_col_wrap=4, color_continuous_scale='aggrnyl')
    fig.update_layout(xaxis=dict(scaleanchor='y', constrain='domain')) #Make axis equal (squares)
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 10, 'r': 0}, hovermode='closest') #Change margins
    fig.update_layout(font=dict(size=8)) # Change font size
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Z  Field (nT)=", "Bz ="))) # change title of each facet
    fig['layout']['yaxis']['title']['text']=''
    fig['layout']['yaxis5']['title']['text']=''
    fig['layout']['yaxis13']['title']['text']=''
    fig['layout']['yaxis17']['title']['text']=''
    fig['layout']['xaxis']['title']['text']=''
    fig['layout']['xaxis']['title']['text']=''
    fig['layout']['xaxis3']['title']['text']=''
    fig['layout']['xaxis4']['title']['text']=''
    ##fig.update_layout(coloraxis_showscale=False)
    fig.layout.coloraxis.colorbar.title = 'PD (V)'
    fig.update_layout(height=400)
    return fig

## Callback for selected data text hanle
@app.callback(
  Output('click-data-2', 'children'),
  Input('facet', 'clickData'),
  Input('graph-with-slider', 'clickData'), 
  Input('segselect', 'value'))
def display_click_data(clickData2, clickData, data_version):
    if data_version == 'ST1':
        df2 = ALL_data_fit_values
        Github_urls = Github_urls_v1
    else:
        df2 = ALL_data_fit_values_v2 
        Github_urls = Github_urls_v2  
    if clickData == None:
        x = 140
        line = df2.iloc[x,]
        lp = line[15]
        ld = line[16]
        temp = line[17]
        filtered_df = Github_urls[(Github_urls['Temp']== temp)]
        filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
        filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
        data_url = filtered_df3.iloc[0,0]
        df = pd.read_table(data_url)
        df.columns = df.iloc[0]
        df =df.iloc[1:]
        newdf = df.apply(pd.to_numeric)  
        z_list = sorted(list(set(newdf['Z  Field (nT)'])))
    else:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
        filtered_df = Github_urls[(Github_urls['Temp']== temp)]
        filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
        filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
        data_url = filtered_df3.iloc[0,0]
        df = pd.read_table(data_url)
        df.columns = df.iloc[0]
        df =df.iloc[1:]
        newdf = df.apply(pd.to_numeric)  
        z_list = sorted(list(set(newdf['Z  Field (nT)'])))
    if clickData2 == None:
        x = -1500
        y = -1000
        z = -1000
    else:
        y = clickData2['points'][0]['y']
        x = clickData2['points'][0]['x']
        z_index = clickData2['points'][0]['curveNumber']
        z = z_list[z_index]
    A = 'Selected point: Bx = {}, By = {}, Bz = {}'.format(x,y,z)
    return A

## Callback for graph: transverse hanle
@app.callback(
  Output('click-data-3', 'figure'),
  Input('facet', 'clickData'),
  Input('graph-with-slider', 'clickData'), 
  Input('segselect', 'value'))
def display_click_data(clickData2, clickData, data_version):
    if data_version == 'ST1':
        df2 = ALL_data_fit_values
        Github_urls = Github_urls_v1
    else:
        df2 = ALL_data_fit_values_v2 
        Github_urls = Github_urls_v2      
    if clickData == None:
        x = 140
        line = df2.iloc[x,]
        lp = line[15]
        ld = line[16]
        temp = line[17]
        filtered_df = Github_urls[(Github_urls['Temp']== temp)]
        filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
        filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
        data_url = filtered_df3.iloc[0,0]
        df = pd.read_table(data_url)
        df.columns = df.iloc[0]
        df =df.iloc[1:]
        newdf = df.apply(pd.to_numeric)  
        z_list = sorted(list(set(newdf['Z  Field (nT)'])))
    else:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
        filtered_df = Github_urls[(Github_urls['Temp']== temp)]
        filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
        filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
        data_url = filtered_df3.iloc[0,0]
        df = pd.read_table(data_url)
        df.columns = df.iloc[0]
        df =df.iloc[1:]
        newdf = df.apply(pd.to_numeric)  
        z_list = sorted(list(set(newdf['Z  Field (nT)'])))
    if clickData2 == None:
        x = -1500
        y = -1000
        z = -1000
    else:
        y = clickData2['points'][0]['y']
        x = clickData2['points'][0]['x']
        z_index = clickData2['points'][0]['curveNumber']
        z = z_list[z_index]
    filtered_df = newdf[(newdf['X  Field (nT)']== x)]
    filtered_df2 = filtered_df[(filtered_df['Y  Field (nT)']== y)]
    fig = px.line(filtered_df2, x='Z  Field (nT)', y='Photodiode Voltage (V)')
    fig.update_traces(mode='markers+lines')  
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 10, 'r': 10}, hovermode='closest') #Change margins
    fig.update_layout(height=150)
    fig.update_layout(font=dict(size=8)) # Change font size
    return fig

## Callback for graph: longitudinal hanle
@app.callback(
  Output('click-data-4', 'figure'),
  Input('facet', 'clickData'),
  Input('graph-with-slider', 'clickData'), 
  Input('segselect', 'value'))
def display_click_data(clickData2, clickData, data_version):
    if data_version == 'ST1':
        df2 = ALL_data_fit_values
        Github_urls = Github_urls_v1
    else:
        df2 = ALL_data_fit_values_v2 
        Github_urls = Github_urls_v2        
    if clickData == None:
        x = 140
        line = df2.iloc[x,]
        lp = line[15]
        ld = line[16]
        temp = line[17]
        filtered_df = Github_urls[(Github_urls['Temp']== temp)]
        filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
        filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
        data_url = filtered_df3.iloc[0,0]
        df = pd.read_table(data_url)
        df.columns = df.iloc[0]
        df =df.iloc[1:]
        newdf = df.apply(pd.to_numeric)  
        z_list = sorted(list(set(newdf['Z  Field (nT)'])))
    else:
        temp = clickData['points'][0]['y']
        lp = clickData['points'][0]['x']
        ld = clickData['points'][0]['z']
        filtered_df = Github_urls[(Github_urls['Temp']== temp)]
        filtered_df2 = filtered_df[(filtered_df['Laser_power']== lp)]
        filtered_df3 = filtered_df2[(filtered_df2['Laser_Detuning']== ld)]
        data_url = filtered_df3.iloc[0,0]
        df = pd.read_table(data_url)
        df.columns = df.iloc[0]
        df =df.iloc[1:]
        newdf = df.apply(pd.to_numeric)  
        z_list = sorted(list(set(newdf['Z  Field (nT)'])))
    if clickData2 == None:
        x = -1500
        y = -1000
        z = -1000
    else:
        y = clickData2['points'][0]['y']
        x = clickData2['points'][0]['x']
        z_index = clickData2['points'][0]['curveNumber']
        z = z_list[z_index]
    filtered_df = newdf[(newdf['Z  Field (nT)']== z)]
    filtered_df2 = filtered_df[(filtered_df['Y  Field (nT)']== y)]
    fig = px.line(filtered_df2, x='X  Field (nT)', y='Photodiode Voltage (V)')
    fig.update_traces(mode='markers+lines')  
    fig.update_layout(margin={'l': 0, 'b': 0, 't': 10, 'r': 10}, hovermode='closest') #Change margins
    fig.update_layout(height=150)
    fig.update_layout(font=dict(size=8)) # Change font size
    return fig

if __name__ == '__main__':
    app.run_server()
