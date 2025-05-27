import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import random
import time

# Load dataset globally once to avoid reloading on every callback
try:
    df = pd.read_csv('creditcard.csv')
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()  # Return an empty DataFrame if error

# Reduce dataset size for faster rendering
df_sample = df.sample(n=100000) if not df.empty else pd.DataFrame()

# Simulate model accuracy (replace with real model code)
def get_accuracy():
    time.sleep(0.1)  # Simulated delay (reduce this)
    training_data_accuracy = round(random.uniform(0.90, 0.99), 4)
    test_data_accuracy = round(random.uniform(0.85, 0.95), 4)
    return training_data_accuracy, test_data_accuracy

# Initialize the app
app = dash.Dash(__name__)

# Get column options for dropdowns
dropdown_options = [{'label': col, 'value': col} for col in df.columns] if not df.empty else []

# Layout of the app
app.layout = html.Div([
    html.H1("Credit Card Fraud Detection Dashboard", 
            style={'textAlign': 'center', 'color': 'white', 'fontSize': '48px', 'font-family': 'Arial, sans-serif'}),

    html.Div([
        html.Label("Select X-axis:", style={'color': 'white', 'fontSize': '20px'}),
        dcc.Dropdown(id='x-axis-dropdown', options=dropdown_options, value='V1', clearable=False, style={'width': '50%'}),
        html.Label("Select Y-axis:", style={'color': 'white', 'fontSize': '20px', 'marginTop': '10px'}),
        dcc.Dropdown(id='y-axis-dropdown', options=dropdown_options, value='Amount', clearable=False, style={'width': '50%'}),
    ], style={'marginBottom': '30px'}),

    dcc.Graph(id='live-update-graph'),

    html.Div([
        dcc.Graph(id='pie-chart')  # Add the pie chart graph
    ], style={'marginTop': '30px'}),

    html.Div([
        html.H3("Model Accuracy:", style={'color': 'white', 'fontSize': '24px'}),
        html.P("Accuracy on Training Data: ", style={'color': 'white', 'fontSize': '18px'}),
        html.H4(id='training-accuracy', style={'color': 'white', 'fontSize': '20px'}),
        html.P("Accuracy on Test Data: ", style={'color': 'white', 'fontSize': '18px'}),
        html.H4(id='test-accuracy', style={'color': 'white', 'fontSize': '20px'})
    ], style={'marginTop': 30}),

    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)  # Increase interval time
], style={'backgroundColor': '#1e3c72', 'padding': '20px'})

# Callback to update both the graph and the accuracy scores
@app.callback(
    [Output('live-update-graph', 'figure'),
     Output('pie-chart', 'figure'),  # Add pie chart to the callback outputs
     Output('training-accuracy', 'children'),
     Output('test-accuracy', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_dashboard(n, x_axis, y_axis):
    if df.empty:
        return {}, {}, "N/A", "N/A"

    # Bar chart for live update graph
    fig = go.Figure(data=[go.Bar(x=df_sample[x_axis], y=df_sample[y_axis], marker=dict(color=df_sample['Class']))])
    fig.update_layout(title=f"Bar Graph of {x_axis} vs {y_axis}", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')

    # Pie chart for class distribution (fraud vs non-fraud)
    pie_fig = go.Figure(data=[go.Pie(labels=['Non-Fraud', 'Fraud'],
                                     values=df_sample['Class'].value_counts(),
                                     hole=0.4)])  # Add a donut-style pie chart
    pie_fig.update_layout(title="Fraud vs Non-Fraud Distribution", paper_bgcolor='rgba(0,0,0,0)', font_color='white')

    # Simulated model accuracy values
    training_data_accuracy, test_data_accuracy = get_accuracy()

    return fig, pie_fig, f"{training_data_accuracy*100:.2f}%", f"{test_data_accuracy*100:.2f}%"

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)