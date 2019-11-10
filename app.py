import pandas as pd

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from utils import *
# from math import floor, ceil

app = Flask(__name__)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/aquarium', methods=['POST', 'GET'])
def aquarium():
    if request.method == 'POST':
        aquarium_post(request.args)
    elif request.methos == 'GET':
        aquarium_get()

    return ('', 204)


def aquarium_post(args):
    # Parse post data
    id_sensors = args.get('id_sensor').split(';')
    values = args.get('value').split(';')
    timestamps = args.get('timestamp').split(';')

    # conn = connection(args.get('user'), args.get('pwd'))
    
    query = "insert into public.readings values "
    _query = "({id_sensor}, {value}, {timestamp})"
    values_query = []

    for i in range(0, len(id_sensors)):
        # get entry data
        _id_sensor = id_sensors[i]
        _value = values[i]
        _timestamp = timestamps[i]    

        # add new entry into the list
        values.append(_query.format(id_sensor=_id_sensor, 
                                    value=_value, 
                                    timestamp=_timestamp))     

    query += ','.join(values) + ';'  # prepare query string
    # conn.execute(query)  # execute
    print(query)

    return


def aquarium_get():
    raise NotImplementedError


@app.route('/')
@app.route('/scheduler')
def scheduler():
    df = pd.read_csv('scheduler.csv', sep=';', index_col='id')
    df.sort_index(inplace=True)

    rows = df.to_dict(orient='row')

    df_light_program = pd.read_csv('light.csv', sep=';', index_col='id')
    light_programs = df_light_program.to_dict(orient='row')

    return render_template('scheduler.html', 
                            rows=rows, 
                            programs=light_programs)

@app.route('/')
@app.route('/stats')
def stats():
    # conn = connection('aquarium_arduino', 'test')
    # df = pd.read_sql("select * from v_readings where id_sensor=1 order by 1, 2, 3, 4", conn)

    df = pd.read_csv(r'data.csv', sep=';')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)
 
    # get available sensors
    sensors = df[['id_sensor', 'sensor_name']].\
        drop_duplicates().to_dict(orient='records')

    groups = df.groupby(by='id_sensor')[['value', 'timestamp']]  # group sensor data
    sensors_data = {}  # containter for chart data

    # loop throught sensors
    for key, group in groups:
        labels = group['timestamp'].tolist()
        values = group['value'].apply(lambda x: round(x, 2)).tolist()  
        sensors_data[key] = {'labels': labels, 'values': values}

    labels = df['timestamp']
    values = df['value'].apply(lambda x: round(x, 2))

    return render_template('stats.html', 
                           values=values,
                           labels=labels,
                           sensors=sensors,
                           sensors_data=sensors_data)
