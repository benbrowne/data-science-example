import pymysql
import pandas as pd

con = pymysql.connect(user='root', password='root', database='features')


def get_device_list():
    cur = con.cursor()
    cur.execute("select distinct device_id from hourly")
    return [i[0] for i in cur.fetchall()]


def device_data(device_id):
    cur = con.cursor()
    cur.execute("select data from hourly where device_id=%s", device_id)
    device_data = [eval(line[0]) for line in cur.fetchall()]
    df = pd.DataFrame({key: [line[key] for line in device_data] for key in device_data[0].keys()})
    return df
