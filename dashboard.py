import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

# Read financial data
financial_data = pd.read_feather("financial_data.feather")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define a helper function to create a styled card
def create_card(title, value, color="dark", percent_circle=None):
    card_content = [
        dbc.CardHeader(title),
        dbc.CardBody(
            [
                html.H5(f"{value}", className="card-title"),
                html.P(percent_circle, className="card-text") if percent_circle else None,
            ]
        ),
    ]
    return dbc.Card(card_content, color=color, inverse=True)

# Set the layout of the app
app.layout = html.Div(
    children=[
        html.H1("Financial Dashboard", className="text-center mt-3 mb-4"),
        dbc.Row(
            [
                dbc.Col(create_card("Status", financial_data["Status"][0]), width=4),
                dbc.Col(
                    create_card(
                        "Profit Target", financial_data["Profit Target"][0], "success"
                    ),
                    width=4,
                ),
                dbc.Col(
                    create_card(
                        "Daily Loss", financial_data["Daily Loss"][0], "danger"
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    create_card(
                        "Maximum Loss",
                        financial_data["Maximum Loss"][0],
                        "dark",
                        percent_circle="6%",
                    ),
                    width=6,
                ),
                dbc.Col(
                    create_card(
                        "Active Trading Days",
                        f"{financial_data['Active Trading Days'][0]}/{financial_data['Daily Loss Time Difference (days)'][0]}",
                        "dark",
                        percent_circle=f"{(financial_data['Active Trading Days'][0] / financial_data['Daily Loss Time Difference (days)'][0]) * 100:.0f}%",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    create_card(
                        "Number of Trades", financial_data["Number of Trades"][0], "dark"
                    ),
                    width=4,
                ),
                dbc.Col(
                    create_card(
                        "Winrate",
                        f"{financial_data['Winrate'][0] * 100:.2f}%",
                        "dark",
                        percent_circle=f"{financial_data['Winrate'][0] * 100:.0f}%",
                    ),
                    width=4,
                ),
                dbc.Col(
                    create_card(
                        "Average Win",
                        f"{financial_data['Average Win'][0]:,.2f}",
                        "dark",
                        percent_circle=f"{financial_data['Percentage of Average Win'][0]}",
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    create_card(
                        "Average Loss",
                        f"{financial_data['Average Loss'][0]:,.2f}",
                        "dark",
                        percent_circle=f"{financial_data['Percentage of Average Loss'][0]}",
                    ),
                    width=4,
                ),
                dbc.Col(
                    create_card(
                        "Absolute Losses",
                        f"{financial_data['Absolute Losses'][0]:,.2f}",
                        "dark",
                        percent_circle=f"{financial_data['Percentage of Losses'][0]}",
                    ),
                    width=4,
                ),
                dbc.Col(
                    create_card(
                        "Absolute Profits",
                        f"{financial_data['Absolute Profits'][0]:,.2f}",
                        "dark",
                        percent_circle=f"{financial_data['Percentage of Profits'][0]}",
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
