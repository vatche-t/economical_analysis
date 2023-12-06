import dash
from dash import Dash, html, dcc, Input, Output, State
import requests
import pandas as pd
import os
from dashboard import create_dashboard_layout, register_dashboard_callbacks

# Initialize the Dash app
app = Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='data-store', storage_type='memory'),  # Store data in memory
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1('Enter your credentials'),
    dcc.Input(id='account-input', type='number', placeholder='Account'),
    dcc.Input(id='password-input', type='password', placeholder='Password'),
    dcc.Input(id='server-input', type='text', placeholder='Server'),
    dcc.Dropdown(
        id='step-dropdown',
        options=[
            {'label': '1step', 'value': '1step'},
            {'label': '2step', 'value': '2step'},
            {'label': 'rocket', 'value': 'rocket'},
        ],
        value='1step',
        placeholder='Choose Step',
        style={'margin-bottom': '10px'}
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
])

@app.callback(
    Output('url', 'pathname'),
    Output('data-store', 'data'),  # Update the store with the data
    [Input('submit-val', 'n_clicks')],
    [State('account-input', 'value'),
     State('password-input', 'value'),
     State('server-input', 'value'),
     State('step-dropdown', 'value')]
)
def update_output(n_clicks, account, password, server, selected_step):
    if n_clicks > 0:
        url = "http://127.0.0.1:5000/run_analysis"
        data = {
            "account": account,
            "password": password,
            "server": server,
            "stage": selected_step  
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            financial_data = pd.DataFrame(result.get("financial_data"))
            history_deals_df = pd.DataFrame(result.get("history_deals_df"))
            
            history_deals_df["time"] = pd.to_datetime(history_deals_df["time"], unit="ms")

            status_color = "green" if financial_data["Status"][0].lower() == "green" else "red"
            total_trades = int(financial_data["Active Trading Days"][0])
            trading_days_text = (
                f"Total days traded: {total_trades} out of 3 ({int((total_trades / 3) * 100)}%)"
            )
            
            financial_data["Start Date"] = pd.to_datetime(financial_data["Start Date"])
            financial_data["Absolute Profits"] = (
                financial_data["Absolute Profits"].replace("[\$,]", "", regex=True).astype(float)
            )
            financial_data["Absolute Losses"] = (
                financial_data["Absolute Losses"].replace("[\$,]", "", regex=True).astype(float)
            )
            
            profit_and_loss = financial_data["Absolute Profits"] - financial_data["Absolute Losses"]

            
            # Update the data store
            return '/dashboard', {
                'financial_data': financial_data.to_dict(),
                'history_deals_df': history_deals_df.to_dict(),
                'status_color': status_color,
                'total_trades': total_trades,
                'trading_days_text': trading_days_text,
                'profit_and_loss': profit_and_loss.to_list()
            },
        else:
            # Handle error or unsuccessful status code
            pass
    return '/', None

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              State('data-store', 'data'))  # Get data from the store
def display_page(pathname, data):
    if pathname == '/dashboard' and data:
        # Retrieve data from the store
        financial_data = pd.DataFrame(data['financial_data'])
        history_deals_df = pd.DataFrame(data['history_deals_df'])
        status_color = data['status_color']
        total_trades = data['total_trades']
        trading_days_text = data['trading_days_text']
        profit_and_loss = pd.DataFrame(data['profit_and_loss'])
         
        return create_dashboard_layout(financial_data, history_deals_df, status_color, total_trades, trading_days_text, profit_and_loss)
    else:
        return index_page

register_dashboard_callbacks(app)
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
