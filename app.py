from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objs as go
from flask_cors import CORS

import requests
import pandas as pd
import numpy as np

import dashboard

# Initialize the Dash app
app = Dash(__name__,suppress_callback_exceptions=True)
CORS(app.server)

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
            
  
            
            # Update the data store
            return '/dashboard', {
                'financial_data': financial_data.to_dict(),
                'history_deals_df': history_deals_df.to_dict(),
            },
        else:
            # Handle error or unsuccessful status code
            pass
    return '/', None

@app.callback(Output('page-content', 'children'), 
             Input('url', 'pathname'),
             State('data-store', 'data'))  
def display_page(pathname, data):
    if pathname == '/dashboard' and data:
        financial_data = pd.DataFrame(data['financial_data'])
        deals_df = pd.DataFrame(data['history_deals_df'])
        
        return dashboard.serve_layout(financial_data, deals_df)
    else:
        return index_page


@app.callback(Output("GrossProfit", "figure"), [Input("financial_data", "value")],State('data-store', 'data')) 
def update_Pro(selected_account, data):
    # Get the row corresponding to the selected start date
    financial_data = pd.DataFrame(data['financial_data'])
    selected_row = financial_data.loc[
        financial_data["Account Size"] == selected_account
    ]

    value_profit_str = selected_row["Absolute Profits"].replace("[\$,]", "", regex=True)
    delta_profit_str = selected_row["Percentage of Profits"].replace(
        "[\%,]", "", regex=True
    )

    # Remove the percentage symbol
    value_profit_str = value_profit_str.replace("%", "")
    delta_profit_str = delta_profit_str.replace("%", "")

    # Convert the strings to float
    value_profit = float(value_profit_str)
    delta_profit = float(delta_profit_str)

    return {
        "data": [
            go.Indicator(
                mode="number+delta",
                value=value_profit,
                delta={
                    "reference": delta_profit,
                    "position": "right",
                    "valueformat": ",g",
                    "relative": False,
                    "font": {"size": 15},
                },
                number={"valueformat": ",", "font": {"size": 20}},
                domain={"y": [0, 1], "x": [0, 1]},
            )
        ],
        "layout": go.Layout(
            title={
                "text": "Gross Profit",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font=dict(color="orange"),
            paper_bgcolor="#1f2c56",
            plot_bgcolor="#1f2c56",
            height=50,
        ),
    }




@app.callback(Output("GrossLoss", "figure"), [Input("financial_data", "value")], State('data-store', 'data')) 
def update_Loss(selected_account, data):
    financial_data = pd.DataFrame(data['financial_data'])
    # Get the row corresponding to the selected start date
    selected_row = financial_data.loc[
        financial_data["Account Size"] == selected_account
    ]

    value_profit_str = selected_row["Absolute Losses"].replace("[\$,]", "", regex=True)
    delta_profit_str = selected_row["Percentage of Losses"].replace(
        "[\%,]", "", regex=True
    )

    # Remove the percentage symbol
    value_profit_str = value_profit_str.replace("%", "")
    delta_profit_str = delta_profit_str.replace("%", "")

    # Convert the strings to float
    value_loss = float(value_profit_str)
    delta_loss = float(delta_profit_str)

    return {
        "data": [
            go.Indicator(
                mode="number+delta",
                value=value_loss,
                delta={
                    "reference": delta_loss,
                    "position": "right",
                    "valueformat": ",g",
                    "relative": False,
                    "font": {"size": 15},
                },
                number={
                    "valueformat": ",",
                    "font": {"size": 20},
                },
                domain={"y": [0, 1], "x": [0, 1]},
            )
        ],
        "layout": go.Layout(
            title={
                "text": "Gross Loss",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font=dict(color="#dd1e35"),
            paper_bgcolor="#1f2c56",
            plot_bgcolor="#1f2c56",
            height=50,
        ),
    }


@app.callback(Output("pie_chart", "figure"), [Input("financial_data", "value")], State('data-store', 'data')) 
def update_pie_chart(selected_account, data):
    financial_data = pd.DataFrame(data['financial_data'])
    # Get the row corresponding to the selected account
    selected_row = financial_data.loc[
        financial_data["Account Size"] == selected_account
    ]

    # Extract average win and average loss values
    average_win = float(selected_row["Average Win"])
    average_loss = float(selected_row["Average Loss"])

    # Round the values to two decimal places (adjust as needed)
    average_win = round(average_win)
    average_loss = round(average_loss)

    # Calculate absolute values for clarity in the pie chart
    selected_row["Absolute Win"] = abs(average_win)
    selected_row["Absolute Loss"] = abs(average_loss)

    # Round up the values
    selected_row["Absolute Win Rounded"] = np.ceil(selected_row["Absolute Win"])
    selected_row["Absolute Loss Rounded"] = np.ceil(selected_row["Absolute Loss"])

    colors = ["#3D9970", "#dd1e35"]  # Assign colors to win and loss

    return {
        "data": [
            go.Pie(
                labels=["Average Win", "Average Loss"],
                values=[
                    selected_row["Absolute Win Rounded"].iloc[0],
                    selected_row["Absolute Loss Rounded"].iloc[0],
                ],
                marker=dict(colors=colors),
                hoverinfo="label+percent+value",  # Include the 'value' in hoverinfo
                textinfo="label+percent",  # Display 'label' and 'percent' in the text
                texttemplate="%{label}: $%{value}",  # Customize the text template to include '$'
                textfont=dict(size=13),
                hole=0.7,
                rotation=45,
                insidetextorientation="radial",  # Adjusts text orientation for better visibility
                textposition="outside",  # Position text inside the pie chart
            )
        ],
        "layout": go.Layout(
            plot_bgcolor="#1f2c56",
            paper_bgcolor="#1f2c56",
            hovermode="closest",
            title={
                "text": f"Average Win vs. Average Loss",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "white", "size": 20},
            legend={
                "orientation": "h",
                "bgcolor": "#1f2c56",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.07,
            },
            font=dict(family="sans-serif", size=12, color="white"),
        ),
    }


@app.callback(Output("line_chart", "figure"), [Input("financial_data", "value")], State('data-store', 'data')) 
def update_pnl_chart(selected_account, data):
    history_deals_df = pd.DataFrame(data['history_deals_df'])
    history_deals_df["time"] = pd.to_datetime(history_deals_df["time"], unit="ms")
    # Filter the history_deals_df based on the selected account
    selected_deals = history_deals_df.copy()

    # Calculate mean profit and loss for each day
    mean_daily_profit = selected_deals.groupby(selected_deals["time"].dt.date)[
        "profit"
    ].mean()

    # Create a new column for cumulative balance
    selected_deals["cumulative_balance"] = selected_deals["profit"].cumsum()

    # Drop rows with NaN values in the 'cumulative_balance' column
    selected_deals = selected_deals.dropna(subset=["cumulative_balance"])

    return {
        "data": [
            go.Scatter(
                x=mean_daily_profit.index,
                y=selected_deals.groupby(selected_deals["time"].dt.date)[
                    "cumulative_balance"
                ]
                .last()
                .values,
                mode="lines+markers",
                name="Cumulative Balance",
                line=dict(width=3, color="#FF00FF"),
                marker=dict(color="orange"),
                hoverinfo="text",
                hovertext=(
                    "<b>Date</b>: "
                    + mean_daily_profit.index.astype(str)
                    + "<br>"
                    + "<b>Cumulative Balance</b>: "
                    + [
                        f"{x:,.2f}"
                        for x in selected_deals.groupby(selected_deals["time"].dt.date)[
                            "cumulative_balance"
                        ]
                        .last()
                        .values
                    ]
                    + "<br>"
                ),
            )
        ],
        "layout": go.Layout(
            plot_bgcolor="#1f2c56",
            paper_bgcolor="#1f2c56",
            title={
                "text": "Cumulative Profit and Loss",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "white", "size": 20},
            hovermode="x",
            margin=dict(r=0),
            xaxis=dict(
                title="<b>Date</b>",
                color="white",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="white",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="white"),
            ),
            yaxis=dict(
                title="<b>Cumulative Balance</b>",
                color="white",
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="white",
                linewidth=2,
                ticks="outside",
                tickfont=dict(family="Arial", size=12, color="white"),
            ),
            legend={
                "orientation": "h",
                "bgcolor": "#1f2c56",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.3,
            },
            font=dict(family="sans-serif", size=12, color="white"),
        ),
    }
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
