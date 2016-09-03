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
import pandas as pd
import features
import argparse


def parse_stdin(stdin):
    """generator of a data dictionary from each string of raw data"""
    for line in stdin:
        device_id, epoch_time, data_type, json_data = line.strip('\n').split('\t')
        epoch_time = int(epoch_time)
        json_data = json.loads(json_data)
        torque = json_data['torque']
        temperature = json_data['temperature']
        yield ({'device_id': device_id, 'epoch_time': epoch_time, 'data_type': data_type, 'torque': torque,
                'temperature': temperature})  # how to do this more efficiently?


def main(stdin, out_file=sys.stdout, interval='hour'):
    """prints reduced features from raw data by sending dictionaries from parse_stdin to the 'features' module"""
    # using these to check for new hours or devices
    previous_interval = previous_device_id = 'none'

    # start reading the data
    for index, line_of_data in enumerate(parse_stdin(stdin)):

        time_obj = time.localtime(line_of_data['epoch_time'])
        if interval == 'hour':
            current_interval = time_obj.tm_hour
        elif interval == 'day':
            current_interval = time_obj.tm_yday

        device_id = line_of_data['device_id']
        # check if hour/day or device have changed and if so return features and clear the dataframe
        if previous_interval != current_interval or previous_device_id != line_of_data['device_id']:
            if previous_interval != 'none':
                line_of_output = {interval: current_interval, 'device_id': device_id}
                line_of_output.update({key: features.feature_input[key](df) for key in features.feature_input})
                print >> out_file, line_of_output
            df = pd.DataFrame()
        else:
            df = df.append(pd.DataFrame(line_of_data, index=[index]))

        # note the time and device for comparison with the next iteration
        previous_device_id = device_id
        previous_interval = current_interval

def parse_cl_args():
    parser = argparse.ArgumentParser(description='print dictionary of features from stream of torque and temperature data')
    parser.add_argument('--interval', '-i', choices=['hour', 'day'], default='hour')
    return parser.parse_args(sys.argv[1:]).interval

if __name__ == '__main__':
    main(sys.stdin, interval=parse_cl_args())