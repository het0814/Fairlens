import dash
from dash import dcc, html, Input, Output
from app.Dashboard_Pages.Dashboard_Page_1 import register_callbacks as page1_callbacks
from app.Dashboard_Pages.Dashboard_Page_2 import register_callbacks as page2_callbacks
from app.Dashboard_Pages.Dashboard_Page_3 import register_callbacks as page3_callbacks
from app.Dashboard_Pages.Dashboard_Page_4 import register_callbacks as page4_callbacks
from app.Dashboard_Pages.Dashboard_Page_5 import register_callbacks as page5_callbacks

def init_dashboard(server):
    app = dash.Dash(__name__,
                    suppress_callback_exceptions=True,
                    server=server,
                    url_base_pathname='/dashboard/',
                    external_stylesheets=["/static/css/custom.css"]
                    )

    app.layout = html.Div([
        html.Div([
            html.H1("HR Analytics", style={'textAlign': 'center'}),
            html.H2("FairLens: Visualization Board", style={'textAlign': 'center', 'color': '#63b3ed'})
        ], className="header-box"),

        html.Div([
            html.Div([
                html.Div([html.H4("Total Employees"), html.H2("310")], className="stat-box"),
                html.Div([html.H4("Avg Pay Rate"), html.H2("31.28")], className="stat-box"),
                html.Div([html.H4("Avg Age"), html.H2("25.53")], className="stat-box")
            ], className="sidebar"),

            html.Div([
                html.Div([
                    html.Button("Employee Demographics", id="tab-1-btn", n_clicks=0, className="tab-button"),
                    html.Button("Employee Performance", id="tab-2-btn", n_clicks=0, className="tab-button"),
                    html.Button("Compensation & Tenure", id="tab-3-btn", n_clicks=0, className="tab-button"),
                    html.Button("Recruitment & Development", id="tab-4-btn", n_clicks=0, className="tab-button"),
                    html.Button("Attrition & Diversity Trends", id="tab-5-btn", n_clicks=0, className="tab-button")
                ], className="tab-bar"),
                html.Div(id='content-area', className="content-box")
            ], className="main-panel")
        ], className="dashboard-body")
    ])

    @app.callback(
        Output('content-area', 'children'),
        Output('tab-1-btn', 'className'),
        Output('tab-2-btn', 'className'),
        Output('tab-3-btn', 'className'),
        Output('tab-4-btn', 'className'),
        Output('tab-5-btn', 'className'),
        Input('tab-1-btn', 'n_clicks'),
        Input('tab-2-btn', 'n_clicks'),
        Input('tab-3-btn', 'n_clicks'),
        Input('tab-4-btn', 'n_clicks'),
        Input('tab-5-btn', 'n_clicks'),
    )
    def update_tab_content(n1, n2, n3, n4, n5):
        clicks = [n1, n2, n3, n4, n5]
        idx = clicks.index(max(clicks))

        classes = ["tab-button"] * 5
        classes[idx] = "tab-button active"

        return [
            tab1_content(),
            tab2_content(),
            tab3_content(),
            tab4_content(),
            tab5_content()
        ][idx], *classes

    def grid_content(title, graphs):
        return html.Div([
            html.H2(title, style={'textAlign': 'center', 'color': '#63b3ed'}),
            html.Div([
                html.Div([dcc.Graph(id=graphs[0])], className="graph-cell"),
                html.Div([dcc.Graph(id=graphs[1])], className="graph-cell")
            ], className="graph-row"),
            html.Div([
                html.Div([dcc.Graph(id=graphs[2])], className="graph-cell"),
                html.Div([dcc.Graph(id=graphs[3])], className="graph-cell")
            ], className="graph-row")
        ])

    def tab1_content():
        return grid_content("Employee Demographics", [
            'donut-chart',
            'bar-chart',
            'diversity-bar-chart',
            'age-bin-pie-chart'
        ])

    def tab2_content():
        return html.Div([
            html.Div([
                html.Label("Select Metric", style={'color': '#fff'}),
                dcc.Dropdown(
                    id="metric-dropdown",
                    options=[
                        {"label": "Job Satisfaction", "value": "JobSatisfaction"},
                        {"label": "Work Life Balance", "value": "WorkLifeBalance"}
                    ],
                    value="JobSatisfaction",
                    style={'width': '50%'}
                )
            ], style={'padding': '20px'}),
            grid_content("Employee Performance", [
                'satisfaction-pie',
                'job-satisfaction-line-chart',
                'overtime-satisfaction-bar-chart',
                'overtime-performance-count-bar-chart'
            ])
        ])

    def tab3_content():
        return grid_content("Compensation & Tenure", [
            'salary-distribution',
            'salary-hike-vs-performance',
            'years-at-company',
            'attrition-by-department'
        ])

    def tab4_content():
        return grid_content("Recruitment & Development", [
            'hiring-source-bar-chart',
            'average-training-bar-chart',
            'training-performance-scatter',
            'years-with-manager-histogram'
        ])

    def tab5_content():
        return html.Div([
            html.Div([
                html.Label("Gender Diversity Category", style={'color': '#fff'}),
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
                    style={'width': '50%'}
                ),
                html.Label("Diversity Category", style={'color': '#fff', 'marginTop': '10px'}),
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
                )
            ], style={'padding': '20px'}),
            grid_content("Attrition & Diversity Trends", [
                'attrition-trend-graph',
                'gender-trend-graph',
                'diversity-trend-graph',
                'performance-histogram'
            ])
        ])

    page1_callbacks(app)
    page2_callbacks(app)
    page3_callbacks(app)
    page4_callbacks(app)
    page5_callbacks(app)

    return app.server
