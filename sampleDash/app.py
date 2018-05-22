import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import datetime

app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


df = pd.read_csv(
    '/Users/ujwal/Downloads/record-147753.csv', header=0)

df = df.drop('sleep_position [NA](/api/datatype/270/)',1)

df= df.dropna()

df.rename(columns={'time [s/256]': 'TimeSeries','breathing_rate [rpm](/api/datatype/33/)':'breathing_rate', 'minute_ventilation [mL/min](/api/datatype/36/)':'ventilation','activity [g](/api/datatype/49/)':'activity', 'heart_rate [bpm](/api/datatype/19/)': 'heart_rate','cadence [spm](/api/datatype/53/)':'steps'}, inplace=True)

for i in df.index:
        df.at[i, 'TimeSeries'] = df.at[i, 'TimeSeries'] /256
for i in df.index:
        df.at[i, 'TimeSeries'] = datetime.datetime.fromtimestamp(df.at[i, 'TimeSeries'])
for i in df.index:
        df.at[i, 'TimeSeries'] = df.at[i, 'TimeSeries'].strftime('%Y-%m-%d %H:%M:%S')


df['TimeSeries'] =  pd.to_datetime(df['TimeSeries'], format='%Y-%m-%d %H:%M:%S')

new_data = df.reset_index().set_index('TimeSeries').resample('H').mean()
new_data = new_data.drop('index',1)

trace1 = go.Bar(x=new_data.index, y=new_data['breathing_rate'], name='breathing_rate')
trace2 = go.Bar(x=new_data.index, y=new_data['ventilation'], name='ventilation')
trace3 = go.Bar(x=new_data.index, y=new_data['activity'], name='activity')
trace4 = go.Bar(x=new_data.index, y=new_data['heart_rate'], name='heart_rate')
trace5 = go.Bar(x=new_data.index, y=new_data['steps'], name='steps')


app.layout = html.Div(children=[
    html.H1(children='Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Hexoskin body suit data',
        style={
        'textAlign': 'center',
        'color': colors['text']
        }),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3, trace4, trace5],
            'layout':
            go.Layout(barmode='stack')
        })
])

if __name__ == '__main__':
    app.run_server()