import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_cases = pd.read_csv('./data/cases.csv')
df_cases['week_ending'] = pd.to_datetime(
    df_cases['week_ending'])

latest_cases = df_cases.iloc[-1]

try:
    previous_cases = df_cases.iloc[-2]
except IndexError:
    previous_cases = latest_cases.copy()
    previous_cases['total_confirmed'] = 0
    previous_cases['student_confirmed'] = 0
    previous_cases['staff_confirmed'] = 0

fig_cases = go.Figure()
fig_cases.add_trace(go.Scatter(x=df_cases['week_ending'], y=df_cases['total_confirmed'],
                               mode='lines+markers',
                               name='Total',
                               ))
fig_cases.add_trace(go.Scatter(x=df_cases['week_ending'], y=df_cases['student_confirmed'],
                               mode='lines+markers',
                               name='Student',
                               ))
fig_cases.add_trace(go.Scatter(x=df_cases['week_ending'], y=df_cases['staff_confirmed'],
                               mode='lines+markers', name='Staff',
                               ))

fig_cases.update_layout(
    title=f"Total Confirmed Cases (as of {latest_cases['week_ending'].strftime('%Y-%m-%d')})",
    xaxis_title='Week Ending Date',
    yaxis_title='Number',
    legend_title='Category',
)

df_testing = pd.read_csv('./data/testing.csv')
df_testing['week_ending'] = pd.to_datetime(
    df_testing['week_ending'])

fig_screening = go.Figure()
fig_screening.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['asym_screened'],
                                   mode='lines+markers',
                                   name='Asymptomatic',
                                   ))
fig_screening.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['sym_screened'],
                                   mode='lines+markers',
                                   name='Symptomatic',
                                   ))

fig_screening.update_layout(
    title=f'Weekly number of asymptomatic and symptomatic tests',
    xaxis_title='Week Ending Date',
    yaxis_title='Number',
    legend_title='Test Type',
)

fig_positives = go.Figure()
fig_positives.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['asym_positive'],
                                   mode='lines+markers',
                                   name='Asymptomatic',
                                   ))
fig_positives.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['sym_positive'],
                                   mode='lines+markers',
                                   name='Symptomatic',
                                   ))

fig_positives.update_layout(
    title=f'Weekly number of asymptomatic/symptomatic test positives',
    xaxis_title='Week Ending Date',
    yaxis_title='Number',
    legend_title='Test Type',
)

fig_positivity_rate = go.Figure()
fig_positivity_rate.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['asym_positive_rate'],
                                         mode='lines+markers',
                                         name='Asymptomatic',
                                         ))
fig_positivity_rate.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['sym_positive_rate'],
                                         mode='lines+markers',
                                         name='Symptomatic',
                                         ))

fig_positivity_rate.update_layout(
    title=f'Weekly asymptomatic/symptomatic test positivity rate',
    xaxis_title='Week Ending Date',
    yaxis_title='Percentage',
    legend_title='Test Type',
)

df_participation = pd.read_csv('./data/participation.csv')
df_participation['week_ending'] = pd.to_datetime(
    df_participation['week_ending'])

fig_participation = go.Figure()
fig_participation.add_trace(go.Scatter(x=df_participation['week_ending'], y=df_participation['consented'],
                                       mode='lines+markers',
                                       name='Consented',
                                       hovertext=df_participation['consented_percent'].astype('str') + '%'))
fig_participation.add_trace(go.Scatter(x=df_participation['week_ending'], y=df_participation['declined'],
                                       mode='lines+markers',
                                       name='Declined',
                                       hovertext=df_participation['declined_percent'].astype('str') + '%'))
fig_participation.add_trace(go.Scatter(x=df_participation['week_ending'], y=df_participation['undecided'],
                                       mode='lines+markers', name='Undecided',
                                       hovertext=df_participation['undecided_percent'].astype('str') + '%'))

fig_participation.update_layout(
    title=f"Testing Participation (Total Eligible = {df_participation.iloc[-1]['consented'] + df_participation.iloc[-1]['declined'] + df_participation.iloc[-1]['undecided']})",
    xaxis_title='Week Ending Date',
    yaxis_title='Number',
    legend_title='Status',
)

app.layout = dbc.Container(className='mt-3', children=[
    html.H1(children='University of Cambridge COVID-19 Dashboard'),

    html.Div(children='''
        Updated every Monday. Last update: 11 October 2020
    '''),

    html.Div(children=[
        'Unofficial student-run dashboard. Data from ',
        html.A(
            href='https://www.cam.ac.uk/coronavirus/stay-safe-cambridge-uni/data-from-covid-19-testing-service',
            target='_blank',
            children='University of Cambridge'
        ),
        '.'
    ]
    ),

    html.Div(className='my-5',
             children=[
                 dbc.Row(
                     [
                         dbc.Col(html.Div('Total Confirmed Cases')),
                         dbc.Col(html.Div('Total Student Cases')),
                         dbc.Col(html.Div('Total Staff Cases')),
                     ]
                 ),
                 dbc.Row(
                     [
                         dbc.Col(html.Div(html.H5(
                             f"{latest_cases['total_confirmed']} (+{latest_cases['total_confirmed'] - previous_cases['total_confirmed']})"))),
                         dbc.Col(html.Div(html.H5(
                             f"{latest_cases['student_confirmed']} (+{latest_cases['student_confirmed'] - previous_cases['student_confirmed']})"))),
                         dbc.Col(html.Div(html.H5(
                             f"{latest_cases['staff_confirmed']} (+{latest_cases['staff_confirmed'] - previous_cases['staff_confirmed']})"))),
                     ]
                 ),
             ]
             ),

    dcc.Graph(
        id='cases-graph',
        figure=fig_cases
    ),

    dcc.Graph(
        id='test-screening-graph',
        figure=fig_screening
    ),

    dcc.Graph(
        id='test-positive-graph',
        figure=fig_positives
    ),

    dcc.Graph(
        id='test-positivity-graph',
        figure=fig_positivity_rate
    ),

    dcc.Graph(
        id='participation-graph',
        figure=fig_participation
    ),

    html.Div(className='mt-4 mb-2',
             children=[
                 dbc.Row(
                     children=dbc.Col(
                         className='d-flex justify-content-center',
                         children=html.A(href='https://github.com',
                                         target='_blank', children='GitHub'))
                 ),
                 dbc.Row(
                     children=dbc.Col(
                         className='d-flex justify-content-center',
                         children=html.A(href='https://faizaanpervaiz.me',
                                         target='_blank', children='Faizaan Pervaiz'))
                 )
             ])
])

if __name__ == '__main__':
    app.title = 'Cambridge Uni COVID-19 Dashboard'
    app.run_server(debug=os.getenv('FLASK_ENV') == 'development')
