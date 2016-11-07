import pymysql
import pandas as pd

con = pymysql.connect(user='root', password='root', database='features')


def get_device_list():
    cur = con.cursor()
    cur.execute("select device_id, count(device_id) from hourly group by device_id")
    return cur.fetchall()


def device_data(device_id):
    cur = con.cursor()
    cur.execute("select timestamp, data from hourly where device_id={}".format(device_id))
    times, feature_data = zip(*cur.fetchall())
    feature_data = [eval(line) for line in feature_data]
    df = pd.DataFrame({key: [line[key] for line in feature_data] for key in feature_data[0].keys()})
    df['time'] = times
    return df
