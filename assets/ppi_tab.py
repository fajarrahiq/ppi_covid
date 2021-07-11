import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime



url_confirmed = 'https://raw.githubusercontent.com/fajarrahiq/ppi_covid/main/covid_ppi.csv'
df_confirmed = pd.read_csv(url_confirmed)

colors = {
    'paper_color': '#393939',
    'text': '#E1E2E5',
    'plot_color': '#ffffff',
    'confirmed_text':'#3CA4FF',
    'deaths_text':'#f44336',
    'recovered_text':'#5A9E6F',
    'highest_case_bg':'#393939',
        }
        
divBorderStyle = {
    'backgroundColor' : '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}
    
    
#Data total kejadian Covid-19 di PT.PPI
ppi_confirmed_1     = df_confirmed.loc[df_confirmed['Status'] == 'Positif']
ppi_deaths_1        = df_confirmed.loc[df_confirmed['Status'] == 'Meninggal']
ppi_recovered_1     = df_confirmed.loc[df_confirmed['Status'] == 'Sembuh']

ppi_confirmed     = ppi_confirmed_1.drop(['Status'],axis=1).T
ppi_deaths        = ppi_deaths_1.drop(['Status'],axis=1).T
ppi_recovered     = ppi_recovered_1.drop(['Status'],axis=1).T

xxx = ppi_confirmed.index

#merubah data PT.PPI menjadi array agar dapat dilakukan operasi matematis
ppi_confirmed_array     = ppi_confirmed_1.drop(['Status'],axis=1).sum()
ppi_deaths_array        = ppi_deaths_1.drop(['Status'],axis=1).sum()
ppi_recovered_array     = ppi_recovered_1.drop(['Status'],axis=1).sum()

x_array = ppi_deaths_array.index


#data penambahan kasus Covid-19 harian PT.PPI
ppi_confirmed_shift   = (ppi_confirmed_array - ppi_confirmed_array.shift(1)).drop(ppi_confirmed_array.index[0])
ppi_deaths_shift      = (ppi_deaths_array - ppi_deaths_array.shift(1)).drop(ppi_deaths_array.index[0])
ppi_recovered_shift   = (ppi_recovered_array - ppi_recovered_array.shift(1)).drop(ppi_recovered_array.index[0])

x_shift = ppi_confirmed_shift.index


 

tab_3_layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H4(children='Total Positif: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['confirmed_text'],
                       }
                       ),
                html.P(f"{ppi_confirmed_array[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                    'fontSize': 30,
                }
                ),
                html.P('Penambahan (24 Jam): +' + f"{ppi_confirmed_array[-1] - ppi_confirmed_array[-2]:,d}"
                       + ' (' + str(round(((ppi_confirmed_array[-1] - ppi_confirmed_array[-2])/ppi_confirmed_array[-1])*100, 2)) + '%)',
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                }
                ),
            ],
                style=divBorderStyle,
                className='four columns',
            ),
            html.Div([
                html.H4(children='Total Meninggal: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['deaths_text'],
                       }
                       ),
                html.P(f"{ppi_deaths_array[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                    'fontSize': 30,
                }
                ),
                html.P('Tingkat Kematian: ' + str(round(ppi_deaths_array[-1]/ppi_confirmed_array[-1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                }
                ),
            ],
                style=divBorderStyle,
                className='four columns'),
            html.Div([
                html.H4(children='Total Sembuh: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['recovered_text'],
                       }
                       ),
                html.P(f"{ppi_recovered_array[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                    'fontSize': 30,
                }
                ),
                html.P('Tingkat Kesembuhan: ' + str(round(ppi_recovered_array[-1]/ppi_confirmed_array[-1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                }
                ),
            ],
                style=divBorderStyle,
                className='four columns'),
        ], className='row', style={"margin": "2% 3%"}),


        html.Div([
            dcc.Graph(
            id='tab_baru',
            figure={
                'data' : 
                [
                    {'x' : x_array, 'y' : ppi_confirmed_array, 'type' : 'line', 'name' : 'Positif', 'marker' : {'color' : colors['confirmed_text']}},
                    {'x' : x_array, 'y' : ppi_deaths_array, 'type' : 'line', 'name' : 'Meninggal', 'marker' : {'color' : colors['deaths_text']}},
                    {'x' : x_array, 'y' : ppi_recovered_array, 'type' : 'line', 'name' : 'Sembuh', 'marker' : {'color' : colors['recovered_text']}}
                ],
                'layout' : {
                    'plot_bgcolor' : colors['paper_color'],
                    'paper_bgcolor' : colors['paper_color'],
                    'font' : {'color' : colors['text']},
                    'title' : 'Grafik Total Perkembangan Covid-19 di PT. Pengembang Pelabuhan Indonesia',
                    'legend' : dict(x=0.15, y=0.9)
                }
            })
        ], className="row", style={"margin": "1% 3%"}),


        html.Div([
            html.Div([
                html.H6('Tingkat Kematian', style={'textAlign': 'center', 'color': 'white'}),
                dcc.Graph(
                    id='tab_baru_1',
                    figure={
                        'data': [
                        {'x' : x_array, 'y' : ppi_deaths_array, 'type' : 'bar', 'marker' : {'color' : colors['deaths_text']}},
                        ],
                        'layout': {
                                    'plot_bgcolor' : colors['paper_color'],
                                    'paper_bgcolor' : colors['paper_color'],
                        'font' : {'color' : colors['text']}

                        #'title' : 'Tingkat Kematian Pasien Covid-19'
                        }
                    }
                )
            ], className="six columns"),

            html.Div([
                html.H6('Tingkat Kesembuhan', style={'textAlign': 'center', 'color': 'white'}),
                dcc.Graph(
                    id='tab_baru_2',
                    figure={
                        'data': [
                        {'x' : x_array, 'y' : ppi_recovered_array, 'type' : 'bar', 'marker' : {'color' : colors['recovered_text']}},
                        ],
                        'layout': {
                                    'plot_bgcolor' : colors['paper_color'],
                                    'paper_bgcolor' : colors['paper_color'],
                        'font' : {'color' : colors['text']}

                        #'title' : 'Tingkat Kesembuhan Pasien Covid-19'
                        }
                    }
                )
            ], className="six columns"),
        ], className="row",style={"margin": "1% 3%"}),

        html.Div([
            html.H6('Grafik Harian Perkembangan Covid-19 di PT. PPI', style={'textAlign': 'center', 'color': 'white'}),
            dcc.Graph(
            id='tab_baru',
            figure={
                'data' : 
                [
                    {'x' : x_array, 'y' : ppi_confirmed_shift, 'type' : 'line', 'name' : 'Positif', 'marker' : {'color' : colors['confirmed_text']}},
                    {'x' : x_array, 'y' : ppi_deaths_shift, 'type' : 'line', 'name' : 'Meninggal', 'marker' : {'color' : colors['deaths_text']}},
                    {'x' : x_array, 'y' : ppi_recovered_shift, 'type' : 'line', 'name' : 'Sembuh', 'marker' : {'color' : colors['recovered_text']}}
                ],
                'layout' : {
                    'plot_bgcolor' : colors['paper_color'],
                    'paper_bgcolor' : colors['paper_color'],
                    'font' : {'color' : colors['text']},
                    'legend' : dict(x=0.15, y=0.9)
                }
            })
        ], className="row", style={"margin": "1% 3%"}),

    ],className='row', style={'backgroundColor': '#2D2D2D'})
               
])



