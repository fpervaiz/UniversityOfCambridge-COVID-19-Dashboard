import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtb
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/css/main.css']

app = dash.Dash(__name__, title='Cambridge Uni COVID-19 Dashboard', external_stylesheets=external_stylesheets, meta_tags=[
    {
        'name': 'title',
        'content': 'University of Cambridge COVID-19 Dashboard'
    },
    {
        'name': 'description',
        'content': 'A simple dashboard for tracking weekly case and testing data from the University of Cambridge testing programmes for students and staff.'
    },
    {
        'name': 'keywords',
        'content': 'coronavirus, covid, university, cambridge, data, visualisation, dashboard'
    },
    {
        'name': 'language',
        'content': 'English',
    },
    {
        'name': 'author',
        'content': 'Faizaan Pervaiz'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    # {
    #     'name': 'viewport',
    #     'content': 'width=device-width, initial-scale=1.0'
    # },
    {
        'property': 'og:type',
        'content': 'website'
    },
    {
        'property': 'og:url',
        'content': 'http://camcovid.xyz'
    },
    {
        'property': 'og:title',
        'content': 'University of Cambridge COVID-19 Dashboard'
    },
    {
        'property': 'og:description',
        'content': 'A simple dashboard for tracking weekly case and testing data from the University of Cambridge testing programmes for students and staff.'
    },
    {
        'property': 'og:image',
        'content': 'http://camcovid.xyz/assets/sars-cov-2.jpg'
    },
    {
        'property': 'twitter:card',
        'content': 'summary_large_image'
    },
    {
        'property': 'twitter:url',
        'content': 'http://camcovid.xyz'
    },
    {
        'property': 'twitter:title',
        'content': 'University of Cambridge COVID-19 Dashboard'
    },
    {
        'property': 'twitter:description',
        'content': 'A simple dashboard for tracking weekly case and testing data from the University of Cambridge testing programmes for students and staff.'
    },
    {
        'property': 'twitter:image',
        'content': 'http://camcovid.xyz/assets/sars-cov-2.jpg'
    }
])

server = app.server

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

df_colleges = pd.read_csv('./data/colleges.csv').rename(columns={
    'college': 'College',
    'positives': 'Number of students tested positive',
    'isolating_households': 'Number of households isolating',
    'isolating_students': 'Number of students isolating',
    'last_updated': 'Last updated',
    'source_name': 'Source'
})

# Currently no sensible way of placing a hyperlink in a DataTable cell
# so just use URL string for now
df_colleges['Source'] = df_colleges.source_link.where(
    df_colleges['source_link'].notna(), df_colleges.Source)

table_colleges = dtb.DataTable(
    id='college-table',
    columns=[{"name": i, "id": i}
             for i in df_colleges.columns if i != 'source_link'],
    data=df_colleges.to_dict('records'),
    sort_action='native',
    style_table={'overflowX': 'auto'},
)

df_testing = pd.read_csv('./data/testing.csv')
df_testing['week_ending'] = pd.to_datetime(
    df_testing['week_ending'])
df_testing['total_screened'] = df_testing['asym_screened'] + \
    df_testing['sym_screened']
df_testing['total_positive'] = df_testing['asym_positive'] + \
    df_testing['sym_positive'] + df_testing['other_positive']

fig_screening = go.Figure()
fig_screening.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['asym_screened'],
                                   mode='lines+markers',
                                   name='Asymptomatic',
                                   ))
fig_screening.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['sym_screened'],
                                   mode='lines+markers',
                                   name='Symptomatic',
                                   ))
fig_screening.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['total_screened'],
                                   mode='lines+markers',
                                   name='Total',
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
fig_positives.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['other_positive'],
                                   mode='lines+markers',
                                   name='Other (NHS/Targeted)',
                                   ))
fig_positives.add_trace(go.Scatter(x=df_testing['week_ending'], y=df_testing['total_positive'],
                                   mode='lines+markers',
                                   name='Total',
                                   ))

fig_positives.update_layout(
    title=f"Weekly Confirmed Cases (as of {df_testing.iloc[-1]['week_ending'].strftime('%Y-%m-%d')})",
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

app.layout = dbc.Container(className='container my-5 px-5 pt-5 pb-3', children=[
    html.H1(children='University of Cambridge COVID-19 Dashboard'),

    html.Div(children='''
        Updated weekly. Last update: 20 October 2020
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
                         dbc.Col(html.Div('Weekly Asymptomatic Tests')),
                         dbc.Col(html.Div('Weekly Asymptomatic Positivity Rate')),
                     ]
                 ),
                 dbc.Row(
                     [
                         dbc.Col(html.Div(html.H5(
                             f"{latest_cases['total_confirmed']} (+{latest_cases['week_confirmed']})"))),
                         dbc.Col(html.Div(html.H5(
                             f"{df_testing.iloc[-1]['asym_screened']} (+{df_testing.iloc[-1]['asym_screened'] - df_testing.iloc[-2]['asym_screened']})"))),
                         dbc.Col(html.Div(html.H5(
                             f"{df_testing.iloc[-1]['asym_positive_rate']}% (+{round(df_testing.iloc[-1]['asym_positive_rate'] - df_testing.iloc[-2]['asym_positive_rate'], 1)}%)"))),
                     ]
                 ),
             ]
             ),

    dcc.Graph(
        id='test-positive-graph',
        figure=fig_positives
    ),

    dcc.Graph(
        id='cases-graph',
        figure=fig_cases
    ),

    html.Div(className='my-5',
             children=[
                 html.H4(className='mb-4', children='Breakdown by College'),
                 table_colleges,
             ]
             ),

    dcc.Graph(
        id='test-screening-graph',
        figure=fig_screening
    ),

    dcc.Graph(
        id='test-positivity-graph',
        figure=fig_positivity_rate
    ),

    dcc.Graph(
        id='participation-graph',
        figure=fig_participation
    ),

    html.Div(className='my-3', children=[
        html.H4(className='mb-3', children='Notes'),
        html.Ul([
            html.Li([
                html.Strong('20 October 2020: '),
                'The University has stopped providing a breakdown of students and staff cases, therefore only the total number of cases is available from the week ending 18th October 2020.']
            )
        ])
    ]),

    html.Div(className='mt-5',
             children=[
                 dbc.Row(
                     children=dbc.Col(
                         className='d-flex justify-content-center',
                         children=html.A(href='https://github.com/fpervaiz/UniversityOfCambridge-COVID-19-Dashboard',
                                         target='_blank', children='GitHub'))
                 ),
                 dbc.Row(
                     children=dbc.Col(
                         className='d-flex justify-content-center',
                         children=html.A(href='https://faizaanpervaiz.me',
                                         target='_blank', children='Faizaan Pervaiz'))
                 ),
                 dbc.Row(
                     children=dbc.Col(
                         className='d-flex justify-content-center',
                         children=html.A(href='https://phil.cdc.gov/Details.aspx?pid=23311',
                                         target='_blank', children='Image credits: CDC PHIL'))
                 )
             ])
])

if __name__ == '__main__':
    app.run_server(debug=os.getenv('FLASK_ENV') == 'development')
