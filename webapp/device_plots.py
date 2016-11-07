import plotly


def plot(df):
    # make histogram of max temperature
    data = [{'x': df.max_temperature, 'type': 'histogram'}]
    layout = {'title': 'Distribution of Max Temperature', 'xaxis': {'title': 'Max Temperature'},
              'yaxis': {'title': 'Frequency'}}
    histogram_url = plotly.plotly.plot({'data': data, 'layout': layout}, auto_open=False)
    histogram_html = plotly.tools.get_embed(histogram_url)

    # make scatter of torque vs time
    data = [{'x': df.time, 'y': df.mean_torque, 'type': 'scatter', 'mode': 'markers'}]
    layout = {'title': 'Mean Torque vs time', 'xaxis': {'title': 'Time'}, 'yaxis': {'title': 'Torque'}}
    scatter_url = plotly.plotly.plot({'data': data, 'layout': layout}, auto_open=False)
    scatter_html = plotly.tools.get_embed(scatter_url)

    # make scatter of torque vs temperature
    data = [{'x': df.mean_torque, 'y': df.mean_temperature, 'type': 'scatter', 'mode': 'markers'}]
    layout = {'title': 'Mean temperature vs torque', 'xaxis': {'title': 'Torque'}, 'yaxis': {'title': 'Temperature'}}
    torque_temp_url = plotly.plotly.plot({'data': data, 'layout': layout}, auto_open=False)
    torque_temp_html = plotly.tools.get_embed(torque_temp_url)

    return histogram_html + scatter_html + torque_temp_html
