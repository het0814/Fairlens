
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv(r"app\Dashboard_Pages\synthetic_dataset.csv")
# def get_layout():
#     layout= html.Div([
#         html.H1("Salary and Tenure Analysis", style={'text-align': 'center'}),  

#         html.Div([
#             html.Div([
#                 dcc.Graph(id='salary-scatter')
#             ], style={'width': '48%', 'display': 'inline-block'}),
#         ]),

#         html.Div([        
#             html.Div([
#                 dcc.Graph(id='salary-hike-vs-performance')
#             ], style={'width': '48%', 'display': 'inline-block'}),
#         ], style={'display': 'flex', 'justify-content': 'space-between'}),

#         html.Div([
#             html.Div([
#                 dcc.Graph(id='years-at-company')
#             ], style={'width': '48%', 'display': 'inline-block'}),
#         ], style={'margin-top': '50px'}), 

#         html.Div([
#             html.Div([
#                 dcc.Graph(id='attrition-by-department')
#             ], style={'width': '48%', 'display': 'inline-block'}),
#         ], style={'margin-top': '50px'})
#     ])
#     return layout
def register_callbacks(app):

    @app.callback(
        Output('salary-distribution', 'figure'),
        [Input('salary-distribution', 'id')]
    )
    def update_salary_distribution(_):
        avg_salary_by_position = df.groupby("Position")["PayRate"].mean().reset_index()

        fig = px.bar(avg_salary_by_position, x="Position", y="PayRate", 
                    title="Average Salary by Position",
                    labels={"Position": "Job Position", "PayRate": "Average Salary"},
                    text="PayRate") 
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')  
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},  
            height=600  
        )
        return fig
    @app.callback(
        Output('salary-hike-vs-performance', 'figure'),
        [Input('salary-hike-vs-performance', 'id')]
    )
    def update_salary_hike_vs_performance(_):
        avg_salary_hike = df.groupby("PerformanceRating")["PercentSalaryHike"].mean().reset_index()
        fig = px.bar(avg_salary_hike, x="PerformanceRating", y="PercentSalaryHike", 
                    title="Average Salary Hike by Performance Rating",
                    labels={"PerformanceRating": "Performance Rating", 
                            "PercentSalaryHike": "Average Salary Hike (%)"},
                    text="PercentSalaryHike")
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        return fig

    @app.callback(
        Output('years-at-company', 'figure'),
        [Input('years-at-company', 'id')]
    )
    def update_years_at_company_histogram(_):
        fig = px.histogram(df, x="YearsAtCompany", title="Distribution of Years at Company",
                        labels={"YearsAtCompany": "Years at Company"}, nbins=20)
        return fig

    @app.callback(
        Output('attrition-by-department', 'figure'),
        [Input('attrition-by-department', 'id')]
    )
    def update_attrition_by_department(_):
        fig = px.histogram(df, x="Department", color="Attrition", 
                        title="Attrition by Department",
                        labels={"Attrition": "Attrition Status", "Department": "Department"},
                        category_orders={"Attrition": ["No", "Yes"]}, barmode='stack')
        return fig

    pass

