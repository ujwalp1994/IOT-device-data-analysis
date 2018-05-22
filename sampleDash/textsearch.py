# import pandas_datareader.data as web
import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

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

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    # start = datetime.datetime(2015, 1, 1)
    # end = datetime.datetime.now()
    # df = web.DataReader(input_data, 'morningstar', start, end)
    # df.reset_index(inplace=True)
    # df.set_index("Date", inplace=True)
    # df = df.drop("Symbol", axis=1)

    # df = new_data['']

    df = pd.DataFrame(index=new_data.index)
    df[input_data] = new_data[input_data]

    print(df)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.input_data, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)