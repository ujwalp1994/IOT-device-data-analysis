import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import datetime

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

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=new_data.index.min(),
        max=new_data.index.max(),
        value=new_data.index.min(),
        step=None,
        marks={str(TimeSeries): str(TimeSeries) for TimeSeries in new_data.index.unique()}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = new_data[new_data.TimeSeries == selected_year]
    traces = []
    columns = new_data.columns
    for i in columns.unique():
        df_by_parameters = filtered_df
        traces.append(go.Scatter(
            x=df_by_parameters.index,
            y=df_by_parameters[i],
            text=df_by_parameters.columns,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [2000, 12000]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()