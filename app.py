import dash
import dash_html_components as html
import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import time
import json
import datetime as dt

SCHEDULE = {'morning_meeting':{
    'time':'20:41:45',
    'msg':'morning meeting',
    'isCountDown':False
    },
'open':{
    'time':'21:09:00',
    'msg':'stripe bear is the best',
    'isCountDown':True
    }
}

SCHEDULE['open']['time'] = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(seconds=65),'%H:%M:%S')

def gen_countdown(time,msg):
    '''
    generates 5 minute, 1 minute, 30 seconds, 10 second-->1 countdown messages
    '''
    countdowns = {}
    time = dt.datetime.strptime(time,'%H:%M:%S')
    for i in (300,60,30,10,5,4,3,2,1):
        ctime = time + dt.timedelta(seconds=-1*i)
        if i >= 60:
            msg_new = msg + ' in ' + str(i//60) + ' minute'
        elif i >= 10:
            msg_new = str(i) + ' seconds'
        else:
            msg_new = str(i)
        countdown = {
            'time': dt.datetime.strftime(ctime,'%H:%M:%S'),
            'msg': msg_new,
            'hour': ctime.hour,
            'minute': ctime.minute,
            'second': ctime.second
        }
        countdowns['%s_%s'%(msg,i)] = countdown
    return countdowns


def init_schedule():
    '''
    do fancy pants over here with checking if a trading day, expiry day, etc.. etc..
    '''
    filtered = {}
    for k,v in SCHEDULE.items():
        filtered[k] = {
            'time':v['time'],
            'msg':v['msg'],
            'hour':v['time'].split(':')[0],
            'minute':v['time'].split(':')[1],
            'second':v['time'].split(':')[2]
        }
        if v['isCountDown']:
            for t,m in gen_countdown(v['time'],v['msg']).items():
                filtered[t] = m
    return json.dumps(filtered)

app = dash.Dash(name=__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([dbc.Row([
                                     dbc.Button('',id='server-time', className='mr-1',color='primary',size='lg',style={'font-size':'24px'})]),
                                     dcc.Interval(id='intervalC', interval=100, n_intervals=0),
                                     dcc.Interval(id='intervalS', interval=5000, n_intervals=0),
                                     dbc.Col(html.Div('',id='currentdate',style={'display':'none'}),width=0),
                                     dbc.Col(html.Div(init_schedule(),id='schedule',style={'display':'none'}),width=0)])

# using serverside callback
@app.callback(dash.dependencies.Output('server-time', 'children'),
              [dash.dependencies.Input('intervalC', 'n_intervals')])
def update_timer(_):
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-5]

@app.callback(dash.dependencies.Output('server-time', 'color'),
              [dash.dependencies.Input('intervalC', 'n_intervals')])
def change_color(_):
    now = dt.datetime.now()
    second = now.second
    if second%2!=0:
        return 'danger'
    return 'primary'

# using clientside callback (remember to create the clientside.js file in the assets folder!)
app.clientside_callback(
    dash.dependencies.ClientsideFunction(
        namespace='clientside',
        function_name='schedule_msg'
    ),
    dash.dependencies.Output('currentdate', 'children'),
    [dash.dependencies.Input('intervalS', 'n_intervals'),
    dash.dependencies.Input('schedule', 'children')])

@app.callback(dash.dependencies.Output('schedule', 'children'),
              [dash.dependencies.Input('intervalS', 'n_intervals')])
def update_schedule(_):
    return init_schedule()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')