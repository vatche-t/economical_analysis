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
    # Apply conditional styling based on the title
    if title == "Profit Target" and financial_data["Absolute Profits"][0] > 0.06:
        color = "success"
    elif title == "Maximum Loss" and financial_data["Absolute Losses"][0] > 0.06:
        color = "danger"

    # Dynamically change text color based on "Status" value
    status_color = "green" if title == "Status" and value.lower() == "green" else "red"

    card_content = [
        dbc.CardHeader(title),
        dbc.CardBody(
            [
                html.H5(f"{value}", className="card-title", style={"color": status_color} if title == "Status" else None),
                html.P(percent_circle, className="card-text") if percent_circle else None,
            ]
        ),
    ]
    return dbc.Card(card_content, color=color, inverse=True)

app.layout = html.Div(
    children=[
        html.H1("Financial Dashboard", className="text-center mt-3 mb-4"),
        dbc.Container(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(create_card("Status", financial_data["Status"][0]), width=2),
                            ],
                            className="mb-4",
                        ),
                    ],
                    fluid=True,  # Make container full-width
                    className="bg-dark text-white p-3 mb-4",  # Add dark background and padding
                ),
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_card(
                                        "Profit Target",
                                        financial_data["Profit Target"][0],
                                        "success",
                                        percent_circle=financial_data["percentage of daily profit"][0],
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Daily Loss",
                                        financial_data["Daily Loss"][0],
                                        "danger",
                                        percent_circle=financial_data["percentage of daily loss"][0],
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Maximum Loss",
                                        financial_data["Maximum Loss"][0],
                                        "dark",
                                        percent_circle=financial_data['Percentage of Losses'][0],
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Active Trading Days",
                                        f"{financial_data['Active Trading Days'][0]}/3",
                                        "dark",
                                        percent_circle=f"{(financial_data['Active Trading Days'][0] / 3) * 100:.0f}%",
                                    ),
                                    width=2,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                    fluid=True,
                    className="bg-dark text-white p-3 mb-4",
                ),
                
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_card(
                                        "Number of Trades",
                                        financial_data["Number of Trades"][0],
                                        "dark"
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Winrate",
                                        f"{financial_data['Winrate'][0] * 100:.2f}%",
                                        "dark",
                                        percent_circle=f"{financial_data['Winrate'][0] * 100:.0f}%",
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Average Win",
                                        f"{financial_data['Average Win'][0]:,.2f}",
                                        "dark",
                                        percent_circle=f"{financial_data['Percentage of Average Win'][0]}",
                                    ),
                                    width=2,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                    fluid=True,
                    className="bg-dark text-white p-3 mb-4",
                ),
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_card(
                                        "Average Loss",
                                        f"{financial_data['Average Loss'][0]:,.2f}",
                                        "dark",
                                        percent_circle=f"{financial_data['Percentage of Average Loss'][0]}",
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Losses",
                                        f"{financial_data['Absolute Losses'][0]:,.2f}",
                                        "dark",
                                        percent_circle=f"{financial_data['Percentage of Losses'][0]}",
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    create_card(
                                        "Profits",
                                        f"{financial_data['Absolute Profits'][0]:,.2f}",
                                        "dark",
                                        percent_circle=f"{financial_data['Percentage of Profits'][0]}",
                                    ),
                                    width=2,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                    fluid=True,
                    className="bg-dark text-white p-3 mb-4",
                ),
            ],
        ),
    ],
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
