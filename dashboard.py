import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

def serve_layout(financial_data, deals_df):

    layout = create_dashboard_layout(financial_data, deals_df)
    
    return dcc.Loading(layout)

def create_dashboard_layout(financial_data, history_deals_df):
 

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

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("corona-logo-1.jpg"),
                                id="corona-image",
                                style={
                                    "height": "60px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
                        ],
                        className="one-third column",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Journal",
                                        style={"margin-bottom": "0px", "color": "white"},
                                    ),
                                    html.H5(
                                        "Track Daily Trading Journal",
                                        style={"margin-top": "0px", "color": "white"},
                                    ),
                                ]
                            )
                        ],
                        className="one-half column",
                        id="title",
                    ),
                    html.Div(
                        [
                            html.H6(
                                html.H5(
                                    "challange status:   " + financial_data["Status"][0],
                                    className="card-title",
                                    style={"color": status_color},
                                ),
                                style={"color": "orange"},
                            ),
                        ],
                        className="one-third column",
                        id="title1",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="Profit Target",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                financial_data["Profit Target"][0],
                                style={
                                    "textAlign": "center",
                                    "color": "green"
                                    if float(
                                        financial_data["percentage of daily profit"][0][:-1]
                                    )
                                    >= float(financial_data["Profit Target"][0][:-1])
                                    else "orange",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                "Todays Profits:  "
                                + financial_data["Absolute Daily Profit"][0]
                                + " ("
                                + str(financial_data["percentage of daily profit"][0])
                                + " )",
                                style={
                                    "textAlign": "center",
                                    "color": "green"
                                    if float(
                                        financial_data["percentage of daily profit"][0][:-1]
                                    )
                                    >= float(financial_data["Profit Target"][0][:-1])
                                    else "orange",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                    html.Div(
                        [
                            html.H6(
                                children="Daily Loss",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                financial_data["Daily Loss"][0],
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35"
                                    if float(
                                        financial_data["percentage of daily loss"][0][:-1]
                                    )
                                    >= float(financial_data["Daily Loss"][0][:-1])
                                    else "orange",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                "Todays Loss:  "
                                + financial_data["Absolute daily loss"][0]
                                + " ("
                                + str(financial_data["percentage of daily loss"][0])
                                + " )",
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35"
                                    if float(
                                        financial_data["percentage of daily loss"][0][:-1]
                                    )
                                    >= float(financial_data["Daily Loss"][0][:-1])
                                    else "orange",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                    html.Div(
                        [
                            html.H6(
                                children="Total Loss",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                financial_data["Maximum Loss"][0],
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35"
                                    if float(financial_data["Percentage of Losses"][0][:-1])
                                    >= float(financial_data["Maximum Loss"][0][:-1])
                                    else "orange",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                "Total Loss:  "
                                + f"{financial_data['Absolute Losses'][0]}"
                                + " ("
                                + str(financial_data["Percentage of Losses"][0])
                                + " )",
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35"
                                    if float(financial_data["Percentage of Losses"][0][:-1])
                                    >= float(financial_data["Maximum Loss"][0][:-1])
                                    else "orange",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                    html.Div(
                        [
                            html.H6(
                                children="Trading Days",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                financial_data["Active Trading Days"][0],
                                style={
                                    "textAlign": "center",
                                    "color": "orange",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                trading_days_text,
                                style={
                                    "textAlign": "center",
                                    "color": "orange",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                "Select Account:",
                                className="fix_label",
                                style={"color": "white"},
                            ),
                            dcc.Dropdown(
                                id="financial_data",
                                multi=False,
                                clearable=True,
                                value=10000,
                                placeholder="Select Account",
                                options=[
                                    {"label": acc, "value": acc}
                                    for acc in financial_data["Account Size"]
                                ],
                                className="dcc_compon",
                            ),
                            html.P(
                                "The calculated P&L is: "
                                + "  "
                                + " "
                                + "$"
                                ,
                                className="fix_label",
                                style={"color": "white", "text-align": "center"},
                            ),
                            dcc.Graph(
                                id="GrossProfit",
                                config={"displayModeBar": False},
                                className="dcc_compon",
                                style={"margin-top": "20px"},
                            ),
                            dcc.Graph(
                                id="GrossLoss",
                                config={"displayModeBar": False},
                                className="dcc_compon",
                                style={"margin-top": "20px"},
                            ),
                        ],
                        className="create_container three columns",
                        id="cross-filter-options",
                    ),
                    html.Div(
                        [
                            dcc.Graph(id="pie_chart", config={"displayModeBar": "hover"}),
                        ],
                        className="create_container four columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="line_chart")],
                        className="create_container1 four columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="Win Rate",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                f"{round(financial_data['Winrate'][0] * 100)}%",
                                style={
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                "Average Win:  "
                                + str(round(financial_data["Average Win"][0]))
                                + "$",
                                style={
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                    html.Div(
                        [
                            html.H6(
                                children="Total Lots Traded",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                financial_data["Total Lots Traded"][0],
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                "Number of Trades :  "
                                + str(financial_data["Number of Trades"][0]),
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                    html.Div(
                        [
                            html.H6(
                                children="Equity",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                f"${financial_data['Equity'][0]:,.2f}",
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35",
                                    "fontSize": 40,
                                },
                            ),
                            html.P(
                                "Starting Balance:  "
                                + f"{int(financial_data['Account Size'][0])}"
                                + "$",
                                style={
                                    "textAlign": "center",
                                    "color": "#dd1e35",
                                    "fontSize": 15,
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                    html.Div(
                        [
                            html.H6(
                                children="Platform",
                                style={"textAlign": "center", "color": "white"},
                            ),
                            html.P(
                                financial_data["Platform"][0],
                                style={
                                    "textAlign": "center",
                                    "color": "orange",
                                    "margin-top": "10px",
                                    "fontSize": 25,
                                },
                            ),
                            html.P(
                                "Server: " + financial_data["Server"],
                                style={
                                    "textAlign": "center",
                                    "color": "orange",
                                    "fontSize": 15,
                                    "padding": "15px",
                                    "margin-top": "-18px",
                                },
                            ),
                        ],
                        className="card_container three columns",
                    ),
                ],
                className="row flex-display",
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )
    


    return dcc.Loading(app.layout)


