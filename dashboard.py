import dash
from dash import html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc


from dash_daq import GraduatedBar
import pandas as pd

# Read financial data
financial_data = pd.read_feather("financial_data.feather")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])

# Define a helper function to create a styled card

def create_card(title, value, color="dark", percent_circle=None):
    # Apply conditional styling based on the title
    if title == "Profit Target" and financial_data["Absolute Profits"][0] > 0.06:
        icon = html.I(className="bi bi-check-circle-fill me-2", style={"color": "green", "marginRight": "5px"})
    elif title == "Maximum Loss" and financial_data["Absolute Losses"][0] > 0.06:
        icon = html.I(className="bi bi-x-octagon-fill me-2", style={"color": "red", "marginRight": "5px"})
    elif title == "Daily Loss" and float(value.rstrip('%')) > 0.06:
        icon = html.I(className="bi bi-x-octagon-fill me-2", style={"color": "red", "marginRight": "5px"})
    else:
        icon = None

    # Dynamically change text color based on "Status" value
    status_color = "green" if title == "Status" and value.lower() == "green" else "red"

    # Convert percentage string to float (remove '%' and convert to float)
    percent_value = float(percent_circle.rstrip('%')) if percent_circle else 0

    card_content = [
        dbc.CardHeader(html.Div([icon, title])),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(f"{value}", className="card-title", style={"color": status_color} if title == "Status" else None),
                            width=5 if title not in ["Profit Target", "Maximum Loss", "Active Trading Days"] else 5,
                        ),
                        dbc.Col(
                            dmc.RingProgress(
                                id=f"{title.lower().replace(' ', '_')}_progress",
                                sections=[{"value": f"{percent_value}", "color": "indigo"}],
                                label=dmc.Center(dmc.Text(f"{percent_value}", color="indigo")),
                                size=100,  # Adjust the size as needed
                            ) if title in ["Profit Target", "Daily Loss", "Maximum Loss", "Active Trading Days"] else None,
                            width=5 if title not in ["Profit Target", "Maximum Loss", "Active Trading Days"] else 7,
                        ),
                    ],
                    align="right",  # Center align the content in the row
                    style={"padding": "5px", "margin-top": "10px"}
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, color=color, inverse=True)

app.layout = html.Div(
    children=[
        html.H1("Financial Dashboard", className="text-center mt-3 mb-4"),
        html.Div(
            children=[
                 # First Row
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                create_card("Status", financial_data["Status"][0])
                            ],
                            className="mb-4",
                            style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "250px"}
                        ),
                    ],
                    style={"background-color": "#343a40",}
                ),
                html.Div(
                    children=[
                        create_card(
                            "Profit Target",
                            financial_data["Profit Target"][0],
                            percent_circle=financial_data["percentage of daily profit"][0],
                        ),
                    ],
                    className="mb-4",
                    style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "250px"}
                ),
                html.Div(
                    children=[
                        create_card(
                            "Daily Loss",
                            financial_data["Daily Loss"][0],
                            percent_circle=financial_data["percentage of daily loss"][0]
                        ),
                    ],
                    className="mb-4",
                    style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "250px"}
                ),
                html.Div(
                    children=[
                        create_card(
                            "Maximum Loss",
                            financial_data["Maximum Loss"][0],
                            percent_circle=financial_data['Percentage of Losses'][0]
                        ),
                    ],
                    className="mb-4",
                    style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "250px"}
                ),
                html.Div(
                    children=[
                        create_card(
                            "Active Trading Days",
                            f"{financial_data['Active Trading Days'][0]}/3",
                            "dark",
                            percent_circle=f"{(financial_data['Active Trading Days'][0] / 3) * 100:.0f}%"
                        ),
                    ],
                    className="mb-4",
                    style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "250px",}
                ),
            ],
            className="d-flex justify-content-end", 
            style={"background-color": "#343a40", "padding": "20px"}
        ),

        # Fourth Row
        html.Div(
            children=[
                html.Div(
                    children=[
                        create_card(
                            "Number of Trades",
                            financial_data["Number of Trades"][0],
                            "dark"
                        ),
                        create_card(
                            "Winrate",
                            f"{financial_data['Winrate'][0] * 100:.2f}%",
                            "dark",
                            percent_circle=f"{financial_data['Winrate'][0] * 100:.0f}%"
                        ),
                        create_card(
                            "Average Win",
                            f"{financial_data['Average Win'][0]:,.2f}",
                            "dark",
                            percent_circle=f"{financial_data['Percentage of Average Win'][0]}"
                        ),
                    ],
                    className="mb-4",
                    style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "250px",}
                ),
            ],
            style={"background-color": "#343a40"}
        ),

        # Fifth Row
        html.Div(
            children=[
                html.Div(
                    children=[
                        create_card(
                            "Average Loss",
                            f"{financial_data['Average Loss'][0]:,.2f}",
                            "dark",
                            percent_circle=f"{financial_data['Percentage of Average Loss'][0]}"
                        ),
                        create_card(
                            "Losses",
                            f"{financial_data['Absolute Losses'][0]:,.2f}",
                            "dark",
                            percent_circle=f"{financial_data['Percentage of Losses'][0]}"
                        ),
                        create_card(
                            "Profits",
                            f"{financial_data['Absolute Profits'][0]:,.2f}",
                            "dark",
                            percent_circle=f"{financial_data['Percentage of Profits'][0]}"
                        ),
                    ],
                    className="mb-4",
                    style={"background-color": "#343a40", "color": "white", "padding": "15px", "width": "260px",}
                ),
            ],
            style={"background-color": "#343a40"}
        ),

    ],
    style={"background-color": "#343a40"}
)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
