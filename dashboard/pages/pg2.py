import dash
from dash import Dash, dcc, html, Input, Output
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
import pymssql
conn = pymssql.connect("gen10-data-fundamentals-22-05-sql-server.database.windows.net","haydenmuscha","P3ngu!ns87","group5database")

query = f'SELECT * FROM CensusStat'
df1 = pd.read_sql(query, conn)

query2 = f'SELECT * FROM Demographic'
df2 = pd.read_sql(query2, conn)

query3 = f'SELECT * FROM Metric'
df3 = pd.read_sql(query3, conn)

merg1 = pd.merge(df1, df2, how="inner", on="demoID")
merg2 = pd.merge(merg1, df3, how="inner", on="metricID")

merg2.rename(columns = {'value':'percent'}, inplace = True)


incomestates = merg2.loc[merg2['category'] == 'income bracket']
incomestates = incomestates[["stateID", "percent","demo_group"]]
incomestates.rename(columns = {'demo_group':'income bracket'}, inplace = True)

foodstates = merg2.loc[merg2['metric'] == 'food security']
foodstates = foodstates[["year","stateID", "percent","demo_group"]]
foodstates = foodstates[["year","stateID", "percent"]]
foodstates = foodstates[foodstates.stateID != 'DC']
foodstates = foodstates[foodstates.stateID != 'US']


edustates = merg2.loc[merg2['category'] == 'education level']
edustates = edustates[["stateID", "percent","demo_group"]]
edustates.rename(columns = {'demo_group':'education'}, inplace = True)


dash.register_page(__name__, name='Diabetes Demographics')


layout = html.Div(
    [
        dbc.Row(
            [
                dcc.Markdown('''
                    Demographics of Diabetes Type 2
                    
                    with multiple lines of text
                    
                    what is to be put here is to be decided
                ''')
            ],
        ),  
        dbc.Row(
            [
                dbc.Col(html.H1("Income Brackets By Percentage of Population by State",
                    className='text-center text-primary mb-4'),
                ),
                dbc.Col(html.H1("Educational Attainment By Percentage of Populaiton by State",
                    className='text-center text-primary mb-4'),
                ),
                dbc.Col(html.H1("Food Insecurity By Percentage of Populaiton by State by Year",
                    className='text-center text-primary mb-4'),
                )
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                dcc.Dropdown(id="slct_state1", options =[{'label':x, 'value':x} for x in incomestates.sort_values('income bracket')['income bracket'].unique()],
                        value='Less than 10,000'),width=4
                ),
                dbc.Col(
                dcc.Dropdown(id="slct_state2", options =[{'label':x, 'value':x} for x in edustates.sort_values('education')['education'].unique()],
                        value='Less than high school graduate'), width= 4
                ),
                dbc.Col(
                dcc.Dropdown(id="slct_state3", options =[{'label':x, 'value':x} for x in foodstates.sort_values('year')['year'].unique()],
                        value=2003), width= 4
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                    dcc.Graph(id='income_map', figure={}),
                    ], width=4
                ),
                dbc.Col(
                    [
                    dcc.Graph(id='education_map', figure={}),
                    ], width=4
                ),
                dbc.Col(
                    [
                    dcc.Graph(id='food_map', figure={}),
                    ], width=4
                ),
            ]
        ),
        dbc.Row(
            [
                dcc.Markdown('''
                    Call to Action
                    
                    with multiple lines of text
                    
                    what is to be put here is to be decided
                ''')
            ],
        ),
    ]
)
@callback(
     Output(component_id='income_map', component_property='figure'),
    [Input(component_id='slct_state1', component_property='value')]
)
def update_graph(option_slctd):



    dff = incomestates.copy()
    dff = dff[dff["income bracket"] == option_slctd]


    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='stateID',
        scope="usa",
        color='percent',
        hover_data=['stateID', 'percent'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=(0,16),
        labels={'stateID': 'percent'},
        template='plotly_dark'
    )
    return fig

@callback(
     Output(component_id='education_map', component_property='figure'),
    [Input(component_id='slct_state2', component_property='value')]
)    
def update_graph(option_slctd2):



    df = edustates.copy()
    df = df[df["education"] == option_slctd2]


    # Plotly Express
    fig2 = px.choropleth(
        data_frame=df,
        locationmode='USA-states',
        locations='stateID',
        scope="usa",
        color='percent',
        hover_data=['stateID', 'percent'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=(0,16),
        labels={'stateID': 'percent'},
        template='plotly_dark'
    )
    return fig2
@callback(
     Output(component_id='food_map', component_property='figure'),
    [Input(component_id='slct_state3', component_property='value')]
)    
def update_graph(option_slctd3):



    d = foodstates.copy()
    d = d[d["year"] == option_slctd3]


    # Plotly Express
    fig3 = px.choropleth(
        data_frame=d,
        locationmode='USA-states',
        locations='stateID',
        scope="usa",
        color='percent',
        hover_data=['stateID', 'percent'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=(0,16),
        labels={'stateID': 'percent'},
        template='plotly_dark'
    )
    return fig3