"""
- reads from stdin
- 'breaks the stream' when device or user defined time interval changes
- interval to generate features over is defined by the shell argument
- returns a dataframe to features.py
- features are defined by the user in features.py

data format:
 0	1420156760	drive_unit	{"torque": -0.025472679681420144, "temperature": 0.40841407648251765},
 0	1420156770	drive_unit	{"torque": 0.23807620959515494, "temperature": -1.1707010518041583},
 0	1420156780	drive_unit	{"torque": -0.08595670646206277, "temperature": 1.553783619625692},
 0	1420156790	drive_unit	{"torque": -0.9478755887865989, "temperature": 0.5052556076573897}]
"""

import sys
import json
import time
import numpy as np
import pandas as pd
#import features

def parse_stdin(stdin):
    """generator of lines of data from stdin strings"""
    for index, line in enumerate(stdin):
        device_id, epoch_time, data_type, json_data = line.strip('\n').split('\t')
        epoch_time = float(epoch_time)
        json_data = json.loads(json_data)
        torque = json_data['torque']
        temperature = json_data['temperature']
        yield (pd.DataFrame({'device_id':device_id, 'epoch_time':epoch_time, 'data_type':data_type, 'torque':torque, 'temperature':temperature},index=[index]))    #how to do this more efficiently?

# we'll use these to check for new hours or devices
previous_hour = previous_device_id = 'none'

# start reading the data
for line_of_data in parse_stdin(sys.stdin):
    hour = time.localtime(line_of_data.epoch_time).tm_hour
    # check if time or device have changed and if so return features and clear the dataframe
    if previous_hour != hour or previous_device_id != line_of_data.device_id:
        if previous_hour != 'none':
            # {key:features.feature_input[key](df) for key in features.feature_input}
            print(df.torque.mean())
        df = pd.DataFrame()
    else:
        df = pd.append(df, line_of_data)

    # note the time and device for comparison with the next iteration
    previous_device_id = line_of_data.device_id
    previous_hour = hour
