import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app.Dashboard_Pages.ML_ModelComputation_page_5 import get_gender_diversity_predictions, get_predicted_attrition_by_years, get_diversity_predictions, get_preformance_predictions

app = dash.Dash(__name__)

gender_trends, gender_predictions = get_gender_diversity_predictions()
predicted_attrition_by_years = get_predicted_attrition_by_years()
diversity_trends = get_diversity_predictions()
performance_predictions = get_preformance_predictions()

# gender_options = [
#     {'label': 'Female', 'value': 'IsFemale'},
#     {'label': 'Male', 'value': 'IsMale'},
#     {'label': 'Transgender', 'value': 'IsTransgender'},
#     {'label': 'Non-binary/non-conforming', 'value': 'IsNon_binary_non_conforming'},
#     {'label': 'Prefer not to say', 'value': 'IsPrefer_not_to_say'},
#     {'label': 'Other', 'value': 'IsOther'},
# ]

# diversity_options = [
#     {'label': 'Indigenous', 'value': 'Indigenous'},
#     {'label': 'Disability', 'value': 'Disability'},
#     {'label': 'Minority', 'value': 'Minority'},
#     {'label': 'Veteran', 'value': 'Veteran'}
# ]

# app.layout = html.Div([
#     html.H1("Attrition Predictions & Diversity Trends"),

#     html.Div([
#         html.H2("Predicted Attrition by Years"),
#         dcc.Graph(id='attrition-trend-graph'),
#     ], style={'padding': '20px'}),

#     html.Div([
#         html.H2("Gender Diversity Trends Over Time"),

#         html.Label('Select Gender Category for Diversity Trends'),
#         dcc.Dropdown(
#             id='gender-dropdown',
#             options=gender_options,
#             value='IsFemale',  
#             style={'width': '50%'}
#         ),

#         dcc.Graph(id='gender-trend-graph'),
#     ], style={'padding': '20px'}),

#     html.Div([
#         html.H2("Diversity Trends Over Time"),

#         html.Label('Select Diversity Category for Trends'),
#         dcc.Dropdown(
#             id='diversity-dropdown',
#             options=diversity_options,
#             value='Indigenous',  
#             style={'width': '50%'}
#         ),

#         dcc.Graph(id='diversity-trend-graph'),
#     ], style={'padding': '20px'}),

#     html.Div([
#         html.H2("Histogram of Predicted Performance Rating"),

#         dcc.Graph(id='performance-histogram'),
#     ], style={'padding': '20px'}),
# ])

def register_callbacks(app):
    @app.callback(
        Output('attrition-trend-graph', 'figure'),
        [Input('gender-dropdown', 'value')]
    )
    def update_attrition_graph(selected_gender):
        attrition_trace = go.Scatter(
            x=predicted_attrition_by_years.index,
            y=predicted_attrition_by_years.values,
            mode='markers+lines',
            name=f'Predicted Attrition',
            line=dict(color='green', dash='dash'),
            marker=dict(symbol='circle', size=8)
        )

        figure = {
            'data': [attrition_trace],
            'layout': go.Layout(
                title=f'Predicted Attrition Rates by Years at Company',
                xaxis={'title': 'Years at Company'},
                yaxis={'title': 'Predicted Attrition Rate'},
                showlegend=True
            )
        }
        return figure

    @app.callback(
        Output('gender-trend-graph', 'figure'),
        [Input('gender-dropdown', 'value')]
    )
    def update_gender_graph(selected_gender):
        historical_data = gender_trends[['Year', selected_gender]]
        future_predictions = gender_predictions[selected_gender]

        historical_trace = go.Scatter(
            x=historical_data['Year'],
            y=historical_data[selected_gender],
            mode='markers+lines',
            name=f'Historical {selected_gender}',
            line=dict(color='blue'),
            marker=dict(symbol='circle', size=8)
        )
        
        future_years = list(range(gender_trends['Year'].max() + 1, gender_trends['Year'].max() + 16))
        predicted_trace = go.Scatter(
            x=future_years,
            y=future_predictions,
            mode='markers+lines',
            name=f'Predicted {selected_gender}',
            line=dict(color='orange', dash='dash'),
            marker=dict(symbol='circle', size=8)
        )
        
        figure = {
            'data': [historical_trace, predicted_trace],
            'layout': go.Layout(
                title=f'{selected_gender} Gender Trends Over Time (15-Year Prediction)',
                xaxis={'title': 'Year'},
                yaxis={'title': f'Percentage of {selected_gender} Employees'},
                showlegend=True
            )
        }
        return figure

    @app.callback(
        Output('diversity-trend-graph', 'figure'),
        [Input('diversity-dropdown', 'value')]
    )
    def update_diversity_graph(selected_diversity):
        historical_data = diversity_trends[['Year', selected_diversity]]

        historical_trace = go.Scatter(
            x=historical_data['Year'],
            y=historical_data[selected_diversity],
            mode='markers+lines',
            name=f'Historical {selected_diversity}',
            line=dict(color='purple'),
            marker=dict(symbol='circle', size=8)
        )

        future_years = list(range(diversity_trends['Year'].max() + 1, diversity_trends['Year'].max() + 11))
        future_predictions = diversity_trends.loc[diversity_trends['Year'].isin(future_years), selected_diversity]

        predicted_trace = go.Scatter(
            x=future_years,
            y=future_predictions,
            mode='markers+lines',
            name=f'Predicted {selected_diversity}',
            line=dict(color='red', dash='dash'),
            marker=dict(symbol='circle', size=8)
        )

        figure = {
            'data': [historical_trace, predicted_trace],
            'layout': go.Layout(
                title=f'{selected_diversity} Diversity Trends Over Time (10-Year Prediction)',
                xaxis={'title': 'Year'},
                yaxis={'title': f'Percentage of {selected_diversity} Employees'},
                showlegend=True
            )
        }
        return figure

    @app.callback(
        Output('performance-histogram', 'figure'),
        [Input('performance-histogram', 'id')] 
    )
    def update_performance_graph(selected_gender):
        trace = go.Histogram(
            x=performance_predictions,
            nbinsx=20, 
            marker=dict(color='blue', line=dict(color='black', width=1)),
            opacity=0.7
        )

        figure = {
            'data': [trace],
            'layout': go.Layout(
                title='Histogram of Predicted Performance Ratings (SVR)',
                xaxis={'title': 'Predicted Performance Rating'},
                yaxis={'title': 'Number of Employees'},
                bargap=0.2,  
                showlegend=False
            )
        }
        return figure
    pass
