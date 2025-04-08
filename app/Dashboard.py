import dash
from dash import dcc, html, Input, Output

from app.Dashboard_Pages.Dashboard_Page_1 import register_callbacks as page1_callbacks
from app.Dashboard_Pages.Dashboard_Page_2 import register_callbacks as page2_callbacks
from app.Dashboard_Pages.Dashboard_Page_3 import register_callbacks as page3_callbacks
from app.Dashboard_Pages.Dashboard_Page_4 import register_callbacks as page4_callbacks
from app.Dashboard_Pages.Dashboard_Page_5 import register_callbacks as page5_callbacks


def init_dashboard(server):
    app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server, url_base_pathname='/dashboard/')
    app.title = "FairLens HR Analytics"

    def kpi_card(title, value):
        return html.Div([
            html.Div([
                html.H6(title, style={'color': '#e2e8f0', 'marginBottom': '4px'}),
                html.H4(value, style={'color': '#63b3ed', 'fontWeight': 'bold', 'fontSize': '20px'}),
            ], style={
                'backgroundColor': '#1a202c',
                'padding': '10px 15px',
                'borderRadius': '8px',
                'boxShadow': '0 2px 8px rgba(0,255,255,0.1)',
                'width': '140px',
                'textAlign': 'center'
            })
        ])

    app.layout = html.Div([
        # Top Bar: KPI Cards + Title + Buttons on Right
        html.Div([
            # KPI Cards
            html.Div([
                kpi_card("Total Employees", "310"),
                kpi_card("Avg Pay Rate", "31.28"),
                kpi_card("Avg Age", "25.53")
            ], style={
                'display': 'flex',
                'gap': '15px',
                'alignItems': 'center'
            }),

            # Centered Title
            html.Div([
                html.H1("FairLens HR Analytics", style={
                    'color': '#63b3ed', 'margin': '0', 'fontWeight': 'bold'
                }),
                html.H4("Intelligent Workforce Insights", style={
                    'color': '#a0aec0', 'marginTop': '4px'
                }),
            ], style={'marginLeft': '40px'}),

            # Home + Sign Out Buttons
            html.Div([
                html.A("🏠 Home", href="/home", style={
                    'backgroundColor': '#1f2937',
                    'color': '#63b3ed',
                    'padding': '10px 14px',
                    'borderRadius': '6px',
                    'marginRight': '10px',
                    'textDecoration': 'none',
                    'fontWeight': 'bold',
                    'border': '1px solid #2d3748'
                }),
                html.A("🔓 Sign Out", href="/login", style={
                    'backgroundColor': '#1f2937',
                    'color': '#63b3ed',
                    'padding': '10px 14px',
                    'borderRadius': '6px',
                    'textDecoration': 'none',
                    'fontWeight': 'bold',
                    'border': '1px solid #2d3748'
                }),
            ], style={'marginLeft': 'auto'})  # Push to right
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'flexWrap': 'wrap',
            'marginBottom': '30px',
            'padding': '10px 20px',
            'backgroundColor': '#0d1117'
        }),

        # Tabs Section
        html.Div([
            dcc.Tabs(
                id="tabs",
                value='tab-1',
                children=[
                    dcc.Tab(label='Employee Demographics', value='tab-1'),
                    dcc.Tab(label='Employee Performance', value='tab-2'),
                    dcc.Tab(label='Compensation & Tenure', value='tab-3'),
                    dcc.Tab(label='Recruitment & Development', value='tab-4'),
                    dcc.Tab(label='Attrition & Diversity Trends', value='tab-5'),
                ],
                style={
                    'backgroundColor': '#0d1117',
                    'color': '#cbd5e1',
                    'borderBottom': '1px solid #2d3748',
                    'fontWeight': 'bold'
                },
                colors={
                    'border': '#2d3748',
                    'primary': '#63b3ed',
                    'background': '#1f2937'
                },
                className='custom-tabs'
            ),
            html.Div(id='content-area', style={'padding': '25px'})
        ], style={
            'width': '100%',
            'margin': '0 auto',
            'backgroundColor': '#1a202c',
            'borderRadius': '12px',
            'boxShadow': '0 0 12px rgba(99,179,237,0.15)',
        })
    ], style={'backgroundColor': '#0d1117', 'minHeight': '100vh', 'padding': '30px'})

    # Callback to switch tab content
    @app.callback(
        Output('content-area', 'children'),
        [Input('tabs', 'value')]
    )
    def update_content(tab):
        def graph_grid(*graph_ids):
            return html.Div([
                html.Div([dcc.Graph(id=graph_id)], style={'width': '48%', 'marginBottom': '25px'})
                for graph_id in graph_ids
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'gap': '20px'})

        if tab == 'tab-1':
            return html.Div([
                graph_grid('donut-chart', 'bar-chart'),
                graph_grid('diversity-bar-chart', 'age-bin-pie-chart')
            ])
        elif tab == 'tab-2':
            return html.Div([
                html.Label("Select Metric", style={'color': '#63b3ed', 'marginBottom': '10px'}),
                dcc.Dropdown(
                    id="metric-dropdown",
                    options=[
                        {"label": "Job Satisfaction", "value": "JobSatisfaction"},
                        {"label": "Work Life Balance", "value": "WorkLifeBalance"}
                    ],
                    value="JobSatisfaction",
                    style={"width": "50%", "marginBottom": "30px"}
                ),
                graph_grid("satisfaction-pie", "job-satisfaction-line-chart"),
                graph_grid("overtime-satisfaction-bar-chart", "overtime-performance-count-bar-chart")
            ])
        elif tab == 'tab-3':
            return html.Div([
                graph_grid("salary-distribution", "salary-hike-vs-performance"),
                graph_grid("years-at-company", "attrition-by-department")
            ])
        elif tab == 'tab-4':
            return html.Div([
                graph_grid("hiring-source-bar-chart", "average-training-bar-chart"),
                graph_grid("years-with-manager-histogram")
            ])
        elif tab == 'tab-5':
            return html.Div([
                html.Div([
                    html.Div([
                        html.H4("Predicted Attrition by Years", style={'color': '#63b3ed'}),
                        dcc.Graph(id='attrition-trend-graph', style={'height': '300px'})
                    ], style={'width': '48%', 'marginBottom': '25px'}),

                    html.Div([
                        html.H4("Gender Diversity Trends", style={'color': '#63b3ed'}),
                        html.Label('Select Gender Category', style={'color': '#a0aec0'}),
                        dcc.Dropdown(
                            id='gender-dropdown',
                            options=[
                                {'label': 'Female', 'value': 'IsFemale'},
                                {'label': 'Male', 'value': 'IsMale'},
                                {'label': 'Transgender', 'value': 'IsTransgender'},
                                {'label': 'Non-binary', 'value': 'IsNon_binary_non_conforming'},
                                {'label': 'Prefer not to say', 'value': 'IsPrefer_not_to_say'},
                                {'label': 'Other', 'value': 'IsOther'},
                            ],
                            value='IsFemale',
                            style={'marginBottom': '10px'}
                        ),
                        dcc.Graph(id='gender-trend-graph', style={'height': '300px'})
                    ], style={'width': '48%'}),
                ], style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '2%'}),

                html.Div([
                    html.Div([
                        html.H4("Diversity Trends", style={'color': '#63b3ed'}),
                        html.Label('Select Diversity Category', style={'color': '#a0aec0'}),
                        dcc.Dropdown(
                            id='diversity-dropdown',
                            options=[
                                {'label': 'Indigenous', 'value': 'Indigenous'},
                                {'label': 'Disability', 'value': 'Disability'},
                                {'label': 'Minority', 'value': 'Minority'},
                                {'label': 'Veteran', 'value': 'Veteran'}
                            ],
                            value='Indigenous',
                            style={'marginBottom': '10px'}
                        ),
                        dcc.Graph(id='diversity-trend-graph', style={'height': '300px'})
                    ], style={'width': '48%', 'marginBottom': '25px'}),

                    html.Div([
                        html.H4("Predicted Performance Rating Distribution", style={'color': '#63b3ed'}),
                        dcc.Graph(id='performance-histogram', style={'height': '300px'})
                    ], style={'width': '48%'})
                ], style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '4%'}),
            ])

    # Register page-specific callbacks
    page1_callbacks(app)
    page2_callbacks(app)
    page3_callbacks(app)
    page4_callbacks(app)
    page5_callbacks(app)

    return app.server
