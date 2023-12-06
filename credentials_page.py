# credentials_page.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import requests
import pandas as pd

# Define the credentials layout
credentials_layout = html.Div([
    html.H1("Enter Credentials"),
    dcc.Input(id='account-input', type='text', placeholder='Account Number'),
    dcc.Input(id='password-input', type='password', placeholder='Password'),
    dcc.Input(id='server-input', type='text', placeholder='Server'),
    dcc.Input(id='stage-input', type='text', placeholder='Stage'),
    html.Button('Submit', id='submit-button'),
])

# Define the credentials callbacks
credentials_callbacks = [
    Output('url', 'pathname'),
    Output('page-content', 'children'),
    Output('financial_data', 'data'),
    Output('history_deals_df', 'data'),
    Input('submit-button', 'n_clicks'),
    State('account-input', 'value'),
    State('password-input', 'value'),
    State('server-input', 'value'),
    State('stage-input', 'value')
]

def update_credentials(n_clicks, account, password, server, stage):
    if n_clicks is None:
        raise PreventUpdate

    # Call the Flask endpoint to get data
    url = "http://127.0.0.1:5000/run_analysis"
    data = {"account": account, "password": password, "server": server, "stage": stage}

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        financial_data = pd.DataFrame(result.get("financial_data"))
        history_deals_df = pd.DataFrame(result.get("history_deals_df"))

        # Save data to feather files
        financial_data.to_feather('financial_data.feather')
        history_deals_df.to_feather('history_deals_df.feather')

        # Redirect to the dashboard page
        return '/dashboard', dashboard_layout, financial_data.to_dict('records'), history_deals_df.to_dict('records')
    else:
        # Show an error message or redirect to an error page
        return '/error', html.H1('Error: Unable to fetch data'), None, None
