from flask import Flask, render_template

import db
import device_plots

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
    return render_template("device_display.html", plotting_html=device_plots.plot(df), device_id=device_id)


if __name__ == '__main__':
    app.run(debug=True)
