import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np


financial_data = pd.read_feather("financial_data.feather")
history_deals_df = pd.read_feather("history_deals_df.feather")
status_color = "green" if financial_data["Status"][0].lower() == "green" else "red"
total_trades = financial_data["Active Trading Days"][0]
trading_days_text = (
    f"Total days traded: {total_trades} out of 3 ({int((total_trades / 3) * 100)}%)"
)
# Assuming financial_data is a dictionary or a similar data structure containing the financial data
financial_data["Start Date"] = pd.to_datetime(financial_data["Start Date"])

# Remove dollar sign and commas, then convert to float
financial_data["Absolute Profits"] = (
    financial_data["Absolute Profits"].replace("[\$,]", "", regex=True).astype(float)
)
financial_data["Absolute Losses"] = (
    financial_data["Absolute Losses"].replace("[\$,]", "", regex=True).astype(float)
)

# Calculate P&L
profit_and_loss = financial_data["Absolute Profits"] - financial_data["Absolute Losses"]

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

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
                            + f"${profit_and_loss.values[0]:,.2f}",
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


@app.callback(Output("GrossProfit", "figure"), [Input("financial_data", "value")])
def update_confirmed(selected_account):
    # Get the row corresponding to the selected start date
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


@app.callback(Output("GrossLoss", "figure"), [Input("financial_data", "value")])
def update_confirmed(selected_account):
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


@app.callback(Output("pie_chart", "figure"), [Input("financial_data", "value")])
def update_pie_chart(selected_account):
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


@app.callback(Output("line_chart", "figure"), [Input("financial_data", "value")])
def update_pnl_chart(selected_account):
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


if __name__ == "__main__":
    app.run_server(debug=True)
