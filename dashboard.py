import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd

financial_data = pd.read_feather("financial_data.feather")
history_deals_df = pd.read_feather("history_deals_df.feather")
status_color = "green" if financial_data["Status"][0].lower() == "green" else "red"
total_trades = financial_data["Active Trading Days"][0]
trading_days_text = f'Total days traded: {total_trades} out of 3 ({int((total_trades / 3) * 100)}%)'
# Assuming financial_data is a dictionary or a similar data structure containing the financial data
financial_data['Start Date'] = pd.to_datetime(financial_data['Start Date'])

# Remove dollar sign and commas, then convert to float
financial_data['Absolute Profits'] = financial_data['Absolute Profits'].replace('[\$,]', '', regex=True).astype(float)
financial_data['Absolute Losses'] = financial_data['Absolute Losses'].replace('[\$,]', '', regex=True).astype(float)

# Calculate P&L
profit_and_loss = financial_data['Absolute Profits'] - financial_data['Absolute Losses'] 

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),
                     id='corona-image',
                     style={
                         "height": "60px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H3("Journal", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Track Daily Trading Journal", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6( html.H5("challange status:   " + financial_data["Status"][0], className="card-title", style={"color": status_color}),
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children="Profit Target",
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(financial_data["Profit Target"][0],
                   style={
                       'textAlign': 'center',
                       'color': 'green' if float(financial_data['percentage of daily profit'][0][:-1]) >= float(financial_data["Profit Target"][0][:-1]) else 'orange',
                       'fontSize': 40}
                   ),

            html.P('Todays Profits:  ' + financial_data['Absolute Daily Profit'][0]
                   + ' (' + str(financial_data['percentage of daily profit'][0]) + ' )',
                   style={
                       'textAlign': 'center',
                       'color': 'green' if float(financial_data['percentage of daily profit'][0][:-1]) >= float(financial_data["Profit Target"][0][:-1]) else 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Daily Loss',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(financial_data["Daily Loss"][0],
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35' if float(financial_data['percentage of daily loss'][0][:-1]) >= float(financial_data["Daily Loss"][0][:-1]) else 'orange',
                       'fontSize': 40}
                   ),

            html.P('Todays Loss:  ' + financial_data['Absolute daily loss'][0]
                   + ' (' + str(financial_data['percentage of daily loss'][0]) + ' )',
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35' if float(financial_data['percentage of daily loss'][0][:-1]) >= float(financial_data["Daily Loss"][0][:-1]) else 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Total Loss',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(financial_data["Maximum Loss"][0],
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35' if float(financial_data['Percentage of Losses'][0][:-1]) >= float(financial_data["Maximum Loss"][0][:-1]) else 'orange',
                       'fontSize': 40}
                   ),

            html.P('Total Loss:  ' + f"{financial_data['Absolute Losses'][0]}"
                   + ' (' + str(financial_data["Percentage of Losses"][0]) + ' )',
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35' if float(financial_data['Percentage of Losses'][0][:-1]) >= float(financial_data["Maximum Loss"][0][:-1]) else 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Trading Days',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(financial_data["Active Trading Days"][0],
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),

            html.P(trading_days_text,
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns")

    ], className="row flex-display"),

    html.Div([
       html.Div([
                    html.P('Select Account:', className='fix_label', style={'color': 'white'}),
                    dcc.Dropdown(
                        id='financial_data',
                        multi=False,
                        clearable=True,
                        value=10000,
                        placeholder='Select Account',
                        options=[{'label': acc, 'value': acc}
                                for acc in financial_data['Account Size']],
                        className='dcc_compon'
                    ),
                     html.P('The calculated P&L is: ' + '  ' + ' ' + f"${profit_and_loss.values[0]:,.2f}", className='fix_label',  style={'color': 'white', 'text-align': 'center'}),

                     dcc.Graph(id='GrossProfit', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'},
                     ),

                      dcc.Graph(id='GrossLoss', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='commission', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),


        ], className="create_container three columns", id="cross-filter-options"),
            html.Div([
                      dcc.Graph(id='pie_chart',
                              config={'displayModeBar': 'hover'}),
                              ], className="create_container four columns"),

            html.Div([
                        html.H6(children='Total Loss',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                                ),

                        html.P(financial_data["Maximum Loss"][0],
                            style={
                                'textAlign': 'center',
                                'color': '#dd1e35' if float(financial_data['Percentage of Losses'][0][:-1]) >= float(financial_data["Maximum Loss"][0][:-1]) else 'orange',
                                'fontSize': 40}
                            ),

                        html.P('Total Loss:  ' + f"{financial_data['Absolute Losses'][0]}"
                            + ' (' + str(financial_data["Percentage of Losses"][0]) + ' )',
                            style={
                                'textAlign': 'center',
                                'color': '#dd1e35' if float(financial_data['Percentage of Losses'][0][:-1]) >= float(financial_data["Maximum Loss"][0][:-1]) else 'orange',
                                'fontSize': 15,
                                'margin-top': '-18px'}
                            )], className="card_container three columns",
                    ),

        ], className="row flex-display"),

html.Div([
        html.Div([
            dcc.Graph(id="line_chart")], className="create_container1 twelve columns"),

            ], className="row flex-display"),

    ], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})


@app.callback(
    Output('GrossProfit', 'figure'),
    [Input('financial_data', 'value')])
def update_confirmed(selected_account):
    # Get the row corresponding to the selected start date
    selected_row = financial_data.loc[financial_data['Account Size'] == selected_account]

    value_profit_str = selected_row["Absolute Profits"].replace('[\$,]', '', regex=True)
    delta_profit_str = selected_row["Percentage of Profits"].replace('[\%,]', '', regex=True)
    
    # Remove the percentage symbol
    value_profit_str = value_profit_str.replace('%', '')
    delta_profit_str = delta_profit_str.replace('%', '')

    # Convert the strings to float
    value_profit = float(value_profit_str)
    delta_profit = float(delta_profit_str)

    return {
        'data': [go.Indicator(
            mode='number+delta',
            value=value_profit,
            delta={
                'reference': delta_profit,
                'position': 'right',
                'valueformat': ',g',
                'relative': False,
                'font': {'size': 15}
            },
            number={
                'valueformat': ',',
                'font': {'size': 20}
            },
            domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'Gross Profit',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height=50
        ),
    }



@app.callback(
    Output('GrossLoss', 'figure'),
    [Input('financial_data', 'value')])
def update_confirmed(selected_account):
    # Get the row corresponding to the selected start date
    selected_row = financial_data.loc[financial_data['Account Size'] == selected_account]

    value_profit_str = selected_row["Absolute Losses"].replace('[\$,]', '', regex=True)
    delta_profit_str = selected_row["Percentage of Losses"].replace('[\%,]', '', regex=True)
    
    # Remove the percentage symbol
    value_profit_str = value_profit_str.replace('%', '')
    delta_profit_str = delta_profit_str.replace('%', '')

    # Convert the strings to float
    value_loss = float(value_profit_str)
    delta_loss = float(delta_profit_str)

    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_loss,
                    delta={'reference': delta_loss,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'Gross Loss',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#dd1e35'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

@app.callback(
    Output('commission', 'figure'),
    [Input('financial_data', 'value')])
def update_confirmed(selected_account):
    # Get the row corresponding to the selected start date
    selected_row = financial_data.loc[financial_data['Account Size'] == selected_account]

    value_commission = float(selected_row["commission"])
    delta_recovered = float(selected_row["commission"])
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_commission,
                    delta={'reference': delta_recovered,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'Commissions',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='orange'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }


@app.callback(Output('pie_chart', 'figure'),
              [Input('financial_data', 'value')])
def update_confirmed(selected_account):
    # Get the row corresponding to the selected account
    selected_row = financial_data.loc[financial_data['Account Size'] == selected_account]
    
    # Extract average win and average loss values
    average_win = float(selected_row["Average Win"])
    average_loss = float(selected_row["Average Loss"])
    
    # Round the values to two decimal places (adjust as needed)
    average_win = round(average_win)
    average_loss = round(average_loss)
    
    colors = ['orange', '#dd1e35', 'green', '#e55467']  # Assign colors to win and loss

    # Debugging information
    print(f"Selected Account: {selected_account}")
    print(f"Average Win: {average_win}")
    print(f"Average Loss: {average_loss}")

    return {
        'data': [go.Pie(
            labels=['Average Win', 'Average Loss'],
            values=[average_win, average_loss],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            textfont=dict(size=13),
            hole=.8,
            rotation=45
        )],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': f'Average Win vs. Average Loss for Account Size: {selected_account}',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            titlefont={'color': 'white', 'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center',
                'x': 0.5,
                'y': -0.07
            },
            font=dict(family="sans-serif", size=12, color='white')
        )
    }


@app.callback(Output('line_chart', 'figure'),
              [Input('financial_data', 'value')])
def update_pnl_chart(selected_account):
    # Filter the history_deals_df based on the selected account
    selected_deals = history_deals_df.copy()
    selected_deals['cumulative_profit'] = selected_deals['profit'].cumsum()

    # Drop rows with NaN values in the 'cumulative_profit' column
    selected_deals = selected_deals.dropna(subset=['cumulative_profit'])

    return {
        'data': [
            go.Bar(
                x=selected_deals['time'],
                y=selected_deals['cumulative_profit'],
                name='Daily confirmed',
                marker=dict(color='orange'),
                hoverinfo='text',
                hovertext=(
                    '<b>Date</b>: ' + selected_deals['time'].astype(str) + '<br>' +
                    '<b>Cumulative Profit</b>: ' + [f'{x:,.2f}' for x in selected_deals['cumulative_profit']] + '<br>'
                )
            ),
            go.Scatter(
                x=selected_deals['time'],
                y=selected_deals['cumulative_profit'],
                mode='lines+markers',
                name='Cumulative Profit',
                line=dict(width=3, color='#FF00FF'),
                marker=dict(color='orange'),
                hoverinfo='text',
                hovertext=(
                    '<b>Date</b>: ' + selected_deals['time'].astype(str) + '<br>' +
                    '<b>Cumulative Profit</b>: ' + [f'{x:,.2f}' for x in selected_deals['cumulative_profit']] + '<br>'
                )
            )
        ],
        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            title={
                'text': 'Cumulative Profit and Loss',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={'color': 'white', 'size': 20},
            hovermode='x',
            margin=dict(r=0),
            xaxis=dict(
                title='<b>Date</b>',
                color='white',
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(family='Arial', size=12, color='white')
            ),
            yaxis=dict(
                title='<b>Cumulative Profit</b>',
                color='white',
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(family='Arial', size=12, color='white')
            ),
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3
            },
            font=dict(family="sans-serif", size=12, color='white'),
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)