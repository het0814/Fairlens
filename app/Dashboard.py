import dash
from dash import dcc, html, Input, Output
from app.Dashboard_Pages.Dashboard_Page_1 import register_callbacks as page1_callbacks
from app.Dashboard_Pages.Dashboard_Page_2 import register_callbacks as page2_callbacks
from app.Dashboard_Pages.Dashboard_Page_3 import register_callbacks as page3_callbacks
from app.Dashboard_Pages.Dashboard_Page_4 import register_callbacks as page4_callbacks
from app.Dashboard_Pages.Dashboard_Page_5 import register_callbacks as page5_callbacks  

def init_dashboard(server):
    app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server, url_base_pathname='/dashboard/')
    app.layout = html.Div([
        html.Div([
            html.H1("HR Analytics", style={'display': 'inline-block', 'margin-right': '20px'}),
            html.H2("FairLens: Visualization Board", style={'display': 'inline-block', 'color': 'purple'})
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),

        html.Div([
            html.Div([
                html.Div([
                    html.H4("Total Employees", style={'marginBottom': '10px'}),
                    html.H2("310", style={'color': 'blue', 'marginBottom': '20px', 'fontWeight': 'bold'}),
                ], style={
                    'border': '1px solid gray', 'padding': '15px', 'marginBottom': '20px',
                    'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)', 'borderRadius': '10px', 'textAlign': 'center'
                }),

                html.Div([
                    html.H4("Avg Pay Rate", style={'marginBottom': '10px'}),
                    html.H2("31.28", style={'color': 'blue', 'marginBottom': '20px', 'fontWeight': 'bold'}),
                ], style={
                    'border': '1px solid gray', 'padding': '15px', 'marginBottom': '20px',
                    'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)', 'borderRadius': '10px', 'textAlign': 'center'
                }),

                html.Div([
                    html.H4("Avg Age", style={'marginBottom': '10px'}),
                    html.H2("25.53", style={'color': 'blue', 'marginBottom': '20px', 'fontWeight': 'bold'}),
                ], style={
                    'border': '1px solid gray', 'padding': '15px',
                    'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)', 'borderRadius': '10px', 'textAlign': 'center'
                })
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

            html.Div([
                dcc.Tabs(
                    id="tabs",
                    value='tab-1',
                    children=[
                        dcc.Tab(label='Employee Demographics', value='tab-1',
                                style={'padding': '10px', 'fontWeight': 'bold'},
                                selected_style={'padding': '10px', 'color': 'white', 'backgroundColor': 'black'}),
                        dcc.Tab(label='Employee Performance', value='tab-2',
                                style={'padding': '10px', 'fontWeight': 'bold'},
                                selected_style={'padding': '10px', 'color': 'white', 'backgroundColor': 'black'}),
                        dcc.Tab(label='Compensation & Tenure', value='tab-3',
                                style={'padding': '10px', 'fontWeight': 'bold'},
                                selected_style={'padding': '10px', 'color': 'white', 'backgroundColor': 'black'}),
                        dcc.Tab(label='Recruitment & Development', value='tab-4',
                                style={'padding': '10px', 'fontWeight': 'bold'},
                                selected_style={'padding': '10px', 'color': 'white', 'backgroundColor': 'black'}),
                        dcc.Tab(label='Attrition & Diversity Trends', value='tab-5',
                                style={'padding': '10px', 'fontWeight': 'bold'},
                                selected_style={'padding': '10px', 'color': 'white', 'backgroundColor': 'black'}),
                    ]
                ),
                html.Div(id='content-area')
            ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px'})
        ])
    ])


    @app.callback(
        Output('content-area', 'children'),
        [Input('tabs', 'value')]
    )
    def update_content(tab):
        if tab == 'tab-1':
            return html.Div([
                html.H2("Work From Home Distance Categories"),
                dcc.Graph(id='donut-chart', style={'width': '100%', 'margin': 'auto'}),
                html.H2("Gender and Ethnicity Breakdown (Stacked Column Chart with Percentage)"),
                dcc.Graph(id='bar-chart', style={'width': '100%', 'margin': 'auto'}),
                html.H2("Diversity Metrics Breakdown"),
                dcc.Graph(id='diversity-bar-chart', style={'width': '100%', 'margin': 'auto'}),
                html.H2("Total Employees by Age Bin"),
                dcc.Graph(id='age-bin-pie-chart', style={'width': '100%', 'margin': 'auto'}),
            ])
        elif tab == 'tab-2':
            return html.Div([
                html.H3("Select Metric"),
                dcc.Dropdown(
                    id="metric-dropdown",
                    options=[
                        {"label": "Job Satisfaction", "value": "JobSatisfaction"},
                        {"label": "Work Life Balance", "value": "WorkLifeBalance"}
                    ],
                    value="JobSatisfaction", style={"width": "50%"}
                ),
                html.H3("Satisfaction Breakdown"),
                dcc.Graph(id="satisfaction-pie"),
                html.H3("Average Job Satisfaction by Job Involvement"),
                dcc.Graph(id="job-satisfaction-line-chart"),
                html.H3("Impact of Overtime on Job Satisfaction"),
                dcc.Graph(id="overtime-satisfaction-bar-chart"),
                html.H3("Impact of Overtime on Performance Ratings (Count)"),
                dcc.Graph(id="overtime-performance-count-bar-chart")
            ])
        elif tab == 'tab-3':
            return html.Div([
                html.H1("Salary and Tenure Analysis", style={'text-align': 'center'}),
                dcc.Graph(id='salary-distribution', style={'width': '100%', 'display': 'inline-block'}),
                dcc.Graph(id='salary-hike-vs-performance', style={'width': '100%'}),
                dcc.Graph(id='years-at-company', style={'width': '100%'}),
                dcc.Graph(id='attrition-by-department', style={'width': '100%'}),
            ])
        elif tab == 'tab-4':
            return html.Div([
                html.H2("Hiring Source Distribution"),
                dcc.Graph(id='hiring-source-bar-chart', style={'width': '100%', 'margin': 'auto'}),
                html.H2("Average Training Times by Department"),
                dcc.Graph(id='average-training-bar-chart', style={'width': '100%', 'margin': 'auto'}),
                html.H2("Impact of Training on Performance"),
                dcc.Graph(id='training-performance-scatter', style={'width': '100%', 'margin': 'auto'}),
                html.H2("Distribution of Years with Current Manager"),
                dcc.Graph(id='years-with-manager-histogram', style={'width': '100%', 'margin': 'auto'}),
            ])
        elif tab == 'tab-5':
            return html.Div([
                html.H1("Attrition Predictions & Diversity Trends"),
                html.Div([html.H2("Predicted Attrition by Years"),
                        dcc.Graph(id='attrition-trend-graph'),], style={'padding': '20px'}),
                html.Div([html.H2("Gender Diversity Trends Over Time"),
                    html.Label('Select Gender Category for Diversity Trends'),
                    dcc.Dropdown(
                        id='gender-dropdown',
                        options=[
                            {'label': 'Female', 'value': 'IsFemale'},
                            {'label': 'Male', 'value': 'IsMale'},
                            {'label': 'Transgender', 'value': 'IsTransgender'},
                            {'label': 'Non-binary/non-conforming', 'value': 'IsNon_binary_non_conforming'},
                            {'label': 'Prefer not to say', 'value': 'IsPrefer_not_to_say'},
                            {'label': 'Other', 'value': 'IsOther'},
                        ],
                        value='IsFemale',
                        style={'width': '50%'}
                    ),
                    dcc.Graph(id='gender-trend-graph'),], style={'padding': '20px'}),
                html.Div([
                    html.H2("Diversity Trends Over Time"),
                    html.Label('Select Diversity Category for Trends'),
                    dcc.Dropdown(
                        id='diversity-dropdown',
                        options=[
                            {'label': 'Indigenous', 'value': 'Indigenous'},
                            {'label': 'Disability', 'value': 'Disability'},
                            {'label': 'Minority', 'value': 'Minority'},
                            {'label': 'Veteran', 'value': 'Veteran'}
                        ],
                        value='Indigenous', 
                        style={'width': '50%'}
                    ),
                    dcc.Graph(id='diversity-trend-graph'),], style={'padding': '20px'}),
                html.Div([
                    html.H2("Histogram of Predicted Performance Rating"),
                    dcc.Graph(id='performance-histogram'),], style={'padding': '20px'}),
            ])
        else:
            return html.Div("No content available")

    page1_callbacks(app)
    page2_callbacks(app)
    page3_callbacks(app)
    page4_callbacks(app)
    page5_callbacks(app)  

