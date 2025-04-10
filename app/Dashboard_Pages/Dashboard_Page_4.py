import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

def load_local_company_data():

    csv_path = os.path.join("app", "Dashboard_Pages", "data", "data.csv")
    df = pd.read_csv(csv_path)

    hiring_source_data = df.groupby('RecruitmentSource').size().reset_index(name='Count')

    training_data = df.groupby('Department')['TrainingTimesLastYear'].sum().reset_index(name='Total Training Times')

    df_training_performance = df[['TrainingTimesLastYear', 'PerformanceRating']].dropna()
    df_training_performance['TrainingTimesLastYear'] = pd.to_numeric(df_training_performance['TrainingTimesLastYear'], errors='coerce')
    df_training_performance['PerformanceRating'] = pd.to_numeric(df_training_performance['PerformanceRating'], errors='coerce')

    df['YearsWithCurrManager'] = pd.to_numeric(df['YearsWithCurrManager'], errors='coerce')
    df = df.dropna(subset=['YearsWithCurrManager'])

    avg_training_data = df.groupby('Department')['TrainingTimesLastYear'].mean().reset_index(name='Average Training Times')
    
    return hiring_source_data, avg_training_data, df_training_performance, df
 
# def get_layout():

#     layout=html.Div([
#         html.H1("HR Dashboard"),

#         html.Div([
#             html.H2("Hiring Source Distribution"),
#             dcc.Graph(id='hiring-source-bar-chart'),
#         ], style={'width': '70%', 'margin': 'auto'}),

#         html.Div([
#             html.H2("Training Frequency by Department"),
#             dcc.Graph(id='training-bar-chart'),
#         ], style={'width': '70%', 'margin': 'auto'}),

#         html.Div([
#             html.H2("Impact of Training on Performance"),
#             dcc.Graph(id='training-performance-scatter'),
#         ], style={'width': '70%', 'margin': 'auto'}),

#         html.Div([
#             html.H2("Distribution of Years with Current Manager"),
#             dcc.Graph(id='years-with-manager-histogram'),
#         ], style={'width': '70%', 'margin': 'auto'}),
#     ])
#     return layout

def register_callbacks(app):
    @app.callback(
        Output('hiring-source-bar-chart', 'figure'),
        Input('hiring-source-bar-chart', 'id')  # Triggered when the chart is loaded
    )
    def update_hiring_source_chart(_):
        hiring_source_data, _, _, _ = load_local_company_data()
        fig = px.bar(
            hiring_source_data,
            x='Count',
            y='RecruitmentSource',
            orientation='h',
            title="Employee Distribution by Hiring Source",
            labels={'RecruitmentSource': 'Hiring Source', 'Count': 'Number of Employees'},
            text_auto=True
        ).update_layout(
            showlegend=False,
            xaxis_title="Number of Employees",
            yaxis_title="Recruitment Source",
            plot_bgcolor='white'
        )
        return fig

    # Callback for Average Training Times by Department
    @app.callback(
        Output('average-training-bar-chart', 'figure'),
        Input('average-training-bar-chart', 'id')  # Triggered when the chart is loaded
    )
    def update_average_training_frequency_chart(_):
        _, avg_training_data, _, _ = load_local_company_data()
        fig = px.bar(
            avg_training_data,
            x='Department',
            y='Average Training Times',
            title="Average Training Times by Department",
            labels={'Department': 'Department', 'Average Training Times': 'Average Training Times Last Year'},
            color='Average Training Times',
            color_continuous_scale='Viridis'
        ).update_layout(
            xaxis_title="Department",
            yaxis_title="Average Training Times",
            plot_bgcolor='white'
        )
        return fig

    # Callback for Impact of Training on Performance (Average)
    @app.callback(
        Output('training-performance-bar-chart', 'figure'),
        Input('training-performance-bar-chart', 'id')  # Triggered when the chart is loaded
    )
    def update_training_performance_chart(_):
        _, _, df_training_performance, _ = load_local_company_data()
        # Group by training times and calculate the average performance rating
        df_avg_performance = df_training_performance.groupby('TrainingTimesLastYear')['PerformanceRating'].mean().reset_index()

        # Create the bar chart with the average performance rating per training time
        fig = px.bar(
            df_avg_performance,
            x='TrainingTimesLastYear',
            y='PerformanceRating',
            title="Average Performance Rating by Training Times",
            labels={"TrainingTimesLastYear": "Training Times Last Year", "PerformanceRating": "Average Performance Rating"},
            color='PerformanceRating',
            color_continuous_scale='Viridis'
        ).update_layout(
            xaxis_title="Training Times Last Year",
            yaxis_title="Average Performance Rating",
            template="plotly_white",
        )
        return fig

    # Callback for Distribution of Years with Current Manager
    @app.callback(
        Output('years-with-manager-histogram', 'figure'),
        Input('years-with-manager-histogram', 'id')  # Triggered when the chart is loaded
    )
    def update_years_with_manager_histogram(_):
        _, _, _, df = load_local_company_data()
        fig = px.histogram(
            df,
            x='YearsWithCurrManager',
            title="Distribution of Years with Current Manager",
            labels={"YearsWithCurrManager": "Years with Current Manager"},
            nbins=20,
            color='YearsWithCurrManager'
        ).update_layout(
            xaxis_title="Years with Current Manager",
            yaxis_title="Number of Employees",
            template="plotly_white",
        )
        return fig

    pass
