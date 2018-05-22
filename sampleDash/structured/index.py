import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import app1, app2
import dash

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return app1.layout
    elif pathname == '/apps/app2':
         return app2.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)