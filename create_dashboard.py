import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import os

def calculate_mean(values):
    
    return sum(values) / len(values)

def calculate_volatility(values):
 
    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5

def calculate_min_max_mean_vol_day(df):
    today = pd.Timestamp.now().date()
    today_values = df.loc[df['Dates'].dt.date == today, 'Values']
    daily_mean = calculate_mean(today_values)
    daily_vol = calculate_volatility(today_values)
    return (today_values.min(), today_values.max(), daily_mean, daily_vol)

def calculate_min_max_mean_vol_week(df):
    today = pd.Timestamp.now(tz=df['Dates'].dt.tz)
    week_start = today - timedelta(days=7)
    week_values = df.loc[df['Dates'] >= week_start]
    week_mean = week_values['Values'].mean()
    week_vol = week_values['Values'].std()
    return (week_values['Values'].min(), week_values['Values'].max(), week_mean, week_vol)

def calculate_min_max_mean_vol_month(df):
    today = pd.Timestamp.now(tz=df['Dates'].dt.tz)
    month_start = today - timedelta(days=30)
    month_values = df.loc[df['Dates'] >= month_start]
    month_mean = month_values['Values'].mean()
    month_vol = month_values['Values'].std()
    return (month_values['Values'].min(), month_values['Values'].max(), month_mean, month_vol)

df = pd.read_csv('values.csv', header = None)
df.columns = ['Dates', 'Values'] 
for i in range(len(df)) :
	value = float(df["Values"][i].replace(" ","").replace("\u202f",""))
	df["Values"][i] = value
print ("df",df)
print ("values",df['Values'])
df['Dates'] = pd.to_datetime(df['Dates'])
value_min = min(df.iloc[:, 1])
value_max = max(df.iloc[:, 1])
current_value = df["Values"].iloc[-1]
daily_min,daily_max,daily_mean,daily_vol =  calculate_min_max_mean_vol_day(df)
week_min,week_max,week_mean,week_vol =  calculate_min_max_mean_vol_week(df)
month_min,month_max,month_mean,month_vol =  calculate_min_max_mean_vol_month(df)

graph_Values = go.Scatter(x=df['Dates'], y=df['Values'], mode='lines')


# Define app layout
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='S&P 500 Value Dashboard'),

    # Current value
    html.Div(children=[
        html.H3(children='Current Value'),
        dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
        html.Div(id='current_value')
    ]),

    # Daily, Weekly, Monthly Summary
    html.Div(children=[
        html.H3(children='Summary Statistics'),
        html.Table(children=[
            html.Tr(children=[
                html.Th('Period'),
                html.Th('Minimum Value'),
                html.Th('Maximum Value'),
                html.Th('Mean'),
                html.Th('Volatility')
            ]),
            html.Tr(children=[
                html.Td('Daily'),
                html.Td(id='daily_min'),
                html.Td(id='daily_max'),
                html.Td(id='daily_mean'),
                html.Td(id='daily_vol')
            ]),
            html.Tr(children=[
                html.Td('Weekly'),
                html.Td(id='week_min'),
                html.Td(id='week_max'),
                html.Td(id='week_mean'),
                html.Td(id='week_vol')
            ]),
            html.Tr(children=[
                html.Td('Monthly'),
                html.Td(id='month_min'),
                html.Td(id='month_max'),
                html.Td(id='month_mean'),
                html.Td(id='month_vol')
            ])
        ])
    ]),

    # Graph of price in time
    html.Div(children=[
        html.H3(children='Price over Time'),
        dcc.Graph(
            id='graph_Values',
            figure={
                'data': [go.Scatter(x=df["Dates"], y=df["Values"])],
                'layout': go.Layout(xaxis=dict(title='Date'), yaxis=dict(title='Value'))
            }
        )
    ])
])
@app.callback(
    [Output('daily_min', 'children'),
     Output('daily_max', 'children'),
     Output('daily_mean', 'children'),
     Output('daily_vol', 'children'),
     Output('week_min', 'children'),
     Output('week_max', 'children'),
     Output('week_mean', 'children'),
     Output('week_vol', 'children'),
     Output('month_min', 'children'),
     Output('month_max', 'children'),
     Output('month_mean', 'children'),
     Output('month_vol', 'children')],
    [Input('interval-component', 'n_intervals')])
def update_stats(n):
    daily_min, daily_max, daily_mean, daily_vol = calculate_min_max_mean_vol_day(df)
    week_min, week_max, week_mean, week_vol = calculate_min_max_mean_vol_week(df)
    month_min, month_max, month_mean, month_vol = calculate_min_max_mean_vol_month(df)
    return (round(daily_min, 2), round(daily_max, 2), round(daily_mean, 2), round(daily_vol, 2),
            round(week_min, 2), round(week_max, 2), round(week_mean, 2), round(week_vol, 2),
            round(month_min, 2), round(month_max, 2), round(month_mean, 2), round(month_vol, 2))

@app.callback(Output('current_value', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_current_value(n):
    df = pd.read_csv('values.csv', header=None)
    df.columns = ['Dates', 'Values']
    for i in range(len(df)) :
        value = float(df["Values"][i].replace(" ","").replace("\u202f",""))
        df["Values"][i] = value   
    current_value = df["Values"].iloc[-1]
    return f'${current_value:.2f}'
    
    # get the last value in the DataFrame
    current_value = df['Values'].iloc[-1]
    
    # update the plot
    graph_values = go.Scatter(x=df['Dates'], y=df['Values'], mode='lines')
    current_value_marker = go.Scatter(x=[df['Dates'].iloc[-1]], y=[current_value], mode='markers', name='Current Value')
    fig = go.Figure([graph_values, current_value_marker])
    fig.update_layout(title='Values Over Time', xaxis_title='Date', yaxis_title='Value')
    
    return fig

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8050, debug=True)
