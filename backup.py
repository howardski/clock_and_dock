import dash
import dash_html_components as html
import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import time
from waitress import serve

schedule = {'morning_meeting':{
    'time':'18:00',
    'msg':'morning meeting',
    'isCountDown':False
    }
}

app = dash.Dash(name=__name__)

app.layout = dbc.Container([dbc.Row([dbc.Col(dbc.Label("Client time is:"), width=2),
                                     dbc.Col(html.H2('', id='client-time'), width=10)]),
                            dbc.Row([dbc.Col(dbc.Label("Server time is:"), width=2),
                                     dbc.Col(html.H2('', id='server-time'), width=10)]),
                                     dcc.Interval(id='interval', interval=100, n_intervals=0),
                                     dbc.Col(html.Div('',id='Date'),width=0),
                                     dbc.Col(html.Div(SCHEDULE,id='schedule'))])

# using serverside callback
@app.callback(dash.dependencies.Output('server-time', 'children'),
              [dash.dependencies.Input('interval', 'n_intervals')])
def update_timer(_):
    return datetime.datetime.now().strftime("%c")

# using clientside callback (remember to create the clientside.js file in the assets folder!)
app.clientside_callback(
    dash.dependencies.ClientsideFunction(
        namespace='clientside',
        function_name='update_timer'
    ),
    dash.dependencies.Output('client-time', 'children'),
    [dash.dependencies.Input('interval', 'n_intervals')])

if __name__ == '__main__':
    app.run_server(port=8889)
    # serve(app.server, listen='0.0.0.0:8080')


#TO DO
# 1. schedule times to call audio alerts
# 2. js to receive calls and check if today has been initialized
# 3. list of next 3 events
# 4. format clock
# 5. flash color on the 