
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
def load_local_company_data() :
    csv_path = os.path.join("app", "Dashboard_Pages", "data", "data.csv")
    df = pd.read_csv(csv_path)


    job_satisfaction_involvement = df.groupby("JobInvolvement")["JobSatisfaction"].mean()
    department_satisfaction = df.groupby("Department")[["JobSatisfaction", "WorkLifeBalance"]].mean()
    overtime_satisfaction = df.groupby(["OverTime", "PerformanceRating"])["JobSatisfaction"].mean().unstack()
    overtime_performance_count = df.groupby(["OverTime", "PerformanceRating"])["EmpID"].count().unstack()
    
    return job_satisfaction_involvement, department_satisfaction, overtime_satisfaction, overtime_performance_count


# def get_layout():
#     layout= html.Div([
#         html.H1("HR Data Analysis", style={'textAlign': 'center'}),
        
#         html.Div([
#             html.H3("Select Metric"),
#             dcc.Dropdown(
#                 id="metric-dropdown",
#                 options=[
#                     {"label": "Job Satisfaction", "value": "JobSatisfaction"},
#                     {"label": "Work Life Balance", "value": "WorkLifeBalance"}
#                 ],
#                 value="JobSatisfaction", 
#                 style={"width": "50%"}
#             ),
#         ]),
        
#         html.Div([
#             html.H3("Satisfaction Breakdown"),
#             dcc.Graph(id="satisfaction-pie")
#         ]),
        
#         html.Div([
#             html.H3("Average Job Satisfaction by Job Involvement"),
#             dcc.Graph(id="job-satisfaction-line-chart")
#         ]),
        
#         html.Div([
#             html.H3("Impact of Overtime on Job Satisfaction"),
#             dcc.Graph(id="overtime-satisfaction-bar-chart")
#         ]),
        
#         html.Div([
#             html.H3("Impact of Overtime on Performance Ratings (Count)"),
#             dcc.Graph(id="overtime-performance-count-bar-chart")
#         ])
#     ])
#     return layout

def register_callbacks(app):

    @app.callback(
        Output("job-satisfaction-line-chart", "figure"),
        Input("job-satisfaction-line-chart", "id")
    )
    def update_job_satisfaction_line_chart(_):
        job_satisfaction_involvement, _, _, _ = load_local_company_data()
        fig = px.line(
            job_satisfaction_involvement, 
            x=job_satisfaction_involvement.index, 
            y=job_satisfaction_involvement.values,
            labels={"x": "Job Involvement Level", "y": "Average Job Satisfaction"},
            title="Average Job Satisfaction by Job Involvement Level"
        )
        return fig

    @app.callback(
        Output("satisfaction-pie", "figure"),
        [Input("metric-dropdown", "value")]
    )
    def update_satisfaction_pie_chart(selected_metric):
        _, department_satisfaction, _, _ = load_local_company_data()
        fig = px.pie(
            department_satisfaction, 
            names=department_satisfaction.index, 
            values=department_satisfaction[selected_metric],
            title=f"Average {selected_metric} by Department"
        )
        
        return fig

    @app.callback(
        [Output("overtime-satisfaction-bar-chart", "figure"),
        Output("overtime-performance-count-bar-chart", "figure")],
        Input("overtime-satisfaction-bar-chart", "id")
    )
    def update_overtime_impact_charts(_):
        _, _, overtime_satisfaction, overtime_performance_count = load_local_company_data()

        overtime_satisfaction_fig = px.bar(
            overtime_satisfaction,
            barmode="group",
            labels={"OverTime": "Overtime (Yes/No)", "value": "Average Job Satisfaction"},
            title="Impact of Overtime on Job Satisfaction (Grouped by Performance Ratings)"
        )
        
        overtime_performance_count_fig = px.bar(
            overtime_performance_count,
            barmode="group",
            labels={"OverTime": "Overtime (Yes/No)", "value": "Count of Employees"},
            title="Impact of Overtime on Performance Ratings (Count)"
        )
        
        return overtime_satisfaction_fig, overtime_performance_count_fig

    pass


