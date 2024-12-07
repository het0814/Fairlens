
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv(r"app\Dashboard_Pages\synthetic_dataset.csv")

df['DistanceCategory'] = df['DistanceFromHome'].apply(
    lambda x: 'Near' if 0 <= x <= 4 else
              'Far' if 5 <= x <= 7 else
              'Very Far' if 7 < x <= 10 else
              'Out of Range'
)

pie_data = df['DistanceCategory'].value_counts().reset_index()
pie_data.columns = ['DistanceCategory', 'Count']

gender_ethnicity_data = df.groupby(['Sex', 'Ethnicity']).size().reset_index(name='Count')
total_by_gender = gender_ethnicity_data.groupby('Sex')['Count'].transform('sum')
gender_ethnicity_data['Percentage'] = (gender_ethnicity_data['Count'] / total_by_gender) * 100

disability_percentage = (df[df['Disability'] == 'Yes'].shape[0] / df.shape[0]) * 100
lgbtq_percentage = (df[df['LGBTQ'] == 'Yes'].shape[0] / df.shape[0]) * 100
minority_percentage = (df[df['Minority'] == 'Yes'].shape[0] / df.shape[0]) * 100
veteran_percentage = (df[df['Veteran'] == 'Yes'].shape[0] / df.shape[0]) * 100
diversity_metrics = pd.DataFrame({
    'Diversity Group': ['Disability', 'LGBTQ', 'Minority', 'Veteran'],
    'Percentage': [disability_percentage, lgbtq_percentage, minority_percentage, veteran_percentage]
})

def create_age_bin(age):
    if age <= 20:
        return "Under 20"
    elif age <= 25:
        return "21-25"
    elif age <= 30:
        return "26-30"
    elif age <= 35:
        return "31-35"
    elif age <= 40:
        return "36-40"
    elif age <= 45:
        return "41-45"
    elif age <= 50:
        return "46-50"
    else:
        return "50+"
df['Age_Bin'] = df['Age'].apply(create_age_bin)

age_bin_counts = df['Age_Bin'].value_counts().reset_index()
age_bin_counts.columns = ['Age_Bin', 'Total_Employees']

total_employees = df['EmpID'].nunique()  

avg_pay_rate = round(df['PayRate'].mean(),2)

avg_age = round(df['Age'].mean(),2)






from dash import html

# def get_layout():
#     layout=html.Div([
#         html.H1("HR Dashboard"),

#         html.Div([
#             html.H3("Total Employees"),
#             html.Div(
#                 f"{total_employees}",
#                 style={
#                     'fontSize': '24px',
#                     'fontWeight': 'bold',
#                     'textAlign': 'center',
#                     'padding': '20px',
#                     'margin': 'auto',
#                     'width': '150px',
#                     'height': '100px',
#                     'border': '2px solid #007BFF',
#                     'borderRadius': '10px',
#                     'backgroundColor': '#F0F8FF',
#                     'color': '#007BFF',
#                     'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
#                 }
#             )
#         ]),

#         html.Div([
#             html.H3("Average Pay Rate"),
#             html.Div(
#                 f"{avg_pay_rate}",
#                 style={
#                     'fontSize': '24px',
#                     'fontWeight': 'bold',
#                     'textAlign': 'center',
#                     'padding': '20px',
#                     'margin': 'auto',
#                     'width': '150px',
#                     'height': '100px',
#                     'border': '2px solid #007BFF',
#                     'borderRadius': '10px',
#                     'backgroundColor': '#F0F8FF',
#                     'color': '#007BFF',
#                     'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
#                 }
#             )
#         ]),

#         html.Div([
#             html.H3("Average Age"),
#             html.Div(
#                 f"{avg_age}",
#                 style={
#                     'fontSize': '24px',
#                     'fontWeight': 'bold',
#                     'textAlign': 'center',
#                     'padding': '20px',
#                     'margin': 'auto',
#                     'width': '150px',
#                     'height': '100px',
#                     'border': '2px solid #007BFF',
#                     'borderRadius': '10px',
#                     'backgroundColor': '#F0F8FF',
#                     'color': '#007BFF',
#                     'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
#                 }
#             )
#         ]),
        
#         html.Div([
#             html.H2("Work From Home Distance Categories"),
#             dcc.Graph(id='donut-chart', style={'width': '50%', 'margin': 'auto'}),
#         ]),

#         html.Div([
#             html.H2("Gender and Ethnicity Breakdown (Stacked Column Chart with Percentage)"),
#             dcc.Graph(id='bar-chart', style={'width': '70%', 'margin': 'auto'}),
#         ]),

#         html.Div([
#             html.H2("Diversity Metrics Breakdown"),
#             dcc.Graph(id='diversity-bar-chart', style={'width': '70%', 'margin': 'auto'}),
#         ]),
        
#         html.Div([
#             html.H2("Total Employees by Age Bin"),
#             dcc.Graph(id='age-bin-pie-chart', style={'width': '50%', 'margin': 'auto'}),
#         ])
#     ])
#     return layout

def register_callbacks(app):
    
    @app.callback(
        Output('donut-chart', 'figure'),
        Input('donut-chart', 'id') 
    )
    def update_pie_chart(_):
        fig = px.pie(
            pie_data,
            names='DistanceCategory',
            values='Count',
            title="Employee Distribution by Distance from Home",
            hole=0.5
        )
        return fig

    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('bar-chart', 'id')] 
    )
    def update_stacked_bar_chart(_):
        fig = px.bar(
            gender_ethnicity_data,
            x='Sex',
            y='Percentage',
            color='Ethnicity',
            barmode='stack',
            title="Gender and Ethnicity Breakdown (Stacked Percentage)",
            labels={'Sex': 'Gender', 'Percentage': 'Percentage (%)'},
            text_auto='.2f'  
        )
        fig.update_yaxes(ticksuffix="%")  
        return fig

    @app.callback(
        Output('diversity-bar-chart', 'figure'),
        Input('diversity-bar-chart', 'id')  
    )
    def update_diversity_bar_chart(_):
        fig = px.bar(
            diversity_metrics,
            x='Diversity Group',
            y='Percentage',
            title="Diversity Metrics",
            labels={'Diversity Group': 'Diversity Group', 'Percentage': 'Percentage (%)'},
            color='Diversity Group',  
            barmode='group'  
        )
        fig.update_yaxes(ticksuffix="%") 
        return fig

    @app.callback(
        Output('age-bin-pie-chart', 'figure'),
        Input('age-bin-pie-chart', 'id')  
    )
    def update_pie_chart(_):
        fig = px.pie(
            age_bin_counts,
            names='Age_Bin',
            values='Total_Employees',
            title="Total Employees by Age Bin",
            labels={'Age_Bin': 'Age Bin', 'Total_Employees': 'Total Employees'}
        )
        return fig
    
    pass


