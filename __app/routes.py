import pandas as pd

from flask import render_template
from app import app
from utils import *


@app.route('/')
@app.route('/index')
def index():
    # conn = connection('aquarium_arduino', 'test')
    # df = pd.read_sql("select * from readings where id_sensor=1 order by date_ins desc limit 100", conn)

    # # df = pd.read_csv(r'C:\Users\akubosze\OneDrive - Nokia\Pricing\PriceErosion\Dev\RawData\QoQ\WindowFrames_QoQ_20191022.csv')
    # columns = list(df.columns)
    # rows = []

    # for index, row in df.iterrows():
    #     rows.append(row)

    # return render_template('index.html', columns=columns, items=rows)

    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('index.html', values=temperatures, labels=times, legend=legend)