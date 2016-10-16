
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
import abc
import argparse
import itertools
import json
import sys
import time

import pandas as pd

import features


class BaseFeatureExtractor(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, interval_type='hour', out_file='sys.stdout'):
        self.interval_type = interval_type
        self.out_file = out_file

    @abc.abstractmethod
    def get_deviceid(self, line):
        pass

    @abc.abstractmethod
    def get_interval(self, line):
        pass

    @abc.abstractmethod
    def parse_raw_stream(self, raw_data):
        """generator of dictionary from each string of raw data"""
        pass

    def process_parsed_stream(self, parsed_stream):
        """Takes iterator of data dictionaries. Returns features, one line per time interval"""
        data_block = pd.DataFrame()
        for device_id, device_stream in itertools.groupby(parsed_stream, self.get_deviceid):
            for interval, interval_stream in itertools.groupby(device_stream, self.get_interval):
                for line in interval_stream:
                    data_block = data_block.append(pd.DataFrame.from_records([line]))
                line_of_output = {'device_id': device_id, 'interval': interval}
                line_of_output.update({key: features.feature_input[key](data_block) for key in features.feature_input})
                print >> self.out_file, line_of_output


class CarFeatureExtractor(BaseFeatureExtractor):

    def parse_raw_stream(self, raw_data):
        """generator of a data dictionary from each string of raw data"""
        for line in raw_data:
            device_id, epoch_time, data_type, json_data = line.strip('\n').split('\t')
            epoch_time = int(epoch_time)
            json_data = json.loads(json_data)
            torque = json_data['torque']
            temperature = json_data['temperature']
            yield ({'device_id': device_id, 'epoch_time': epoch_time, 'data_type': data_type, 'torque': torque,
                    'temperature': temperature})

    def get_deviceid(self, line):
        return line['device_id']

    def get_interval(self, line):
        time_obj = time.localtime(line['epoch_time'])
        if self.interval_type == 'hour':
            return time_obj.tm_hour
        elif self.interval_type == 'day':
            return time_obj.tm_yday


def parse_cl_args():
    parser = argparse.ArgumentParser(description='print dictionary of features from stream of torque and temperature data')
    parser.add_argument('--interval', '-i', choices=['hour', 'day'], default='hour')
    return parser.parse_args(sys.argv[1:]).interval

if __name__ == '__main__':
    feature_extractor = CarFeatureExtractor(interval_type=parse_cl_args(), out_file=sys.stdout)
    feature_extractor.process_parsed_stream(feature_extractor.parse_raw_stream(sys.stdin))
