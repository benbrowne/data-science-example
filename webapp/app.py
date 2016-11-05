import time

from flask import Flask, render_template
import plotly
import pandas as pd

import db


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route("/devices")
def devices():
    device_list = db.get_device_list()
    return render_template("devices.html", device_list=device_list)

@app.route("/devices/<device_id>")
def python_device_display(device_id):
    df = db.device_data(device_id)
    data = [{'x': df.mean_torque, 'type': 'histogram'}]
    layout = {'title': 'Distribution of Mean Torque', 'xaxis': {'title': 'Mean Torque'}, 'yaxis': {'title': 'Frequency'}}
    histogram_url = plotly.plotly.plot({'data': data, 'layout': layout}, auto_open=False)
    histogram_html = plotly.tools.get_embed(histogram_url)
    return render_template("device_display.html", histogram_html=histogram_html, device_id=device_id)


if __name__ == '__main__':
    app.run(debug=True)

