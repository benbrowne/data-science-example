
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

import features
import pandas as pd
import pymysql


class BaseFeatureExtractor(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, interval_type):
        self.interval_type = interval_type
        self.features = None

    def get_features(self, stream):
        self.features = [feature for feature in self.process_parsed_stream(self.parse_raw_stream(stream))]

    def publish(self, username=None, password=None, target='stdout'):
        if target == 'stdout':
            sys.stdout.write(self.features)
        elif target == 'mysql':
            if args.username is None or args.password is None:
                sys.stdout.write(self.features)
                sys.stdout.write('Did not write to mysql. Enter mysql username and password arguments to parse_torque_temp')
            else:
                con = pymysql.connect(user=username, password=password, database='features')
                cur = con.cursor()
                for line in self.features:
                    line_to_write = (line['device_id'], line['time_stamp'], self.feature_class, str(line['feature_data']))
                    print(line_to_write)
                    cur.execute("INSERT INTO hourly VALUES (null, %s, %s, %s, %s)", line_to_write)
                con.commit()

    @abc.abstractproperty
    def feature_class(self):
        pass

    @abc.abstractmethod
    def get_device_id(self, line):
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
        for device_id, device_stream in itertools.groupby(parsed_stream, self.get_device_id):
            for interval, interval_stream in itertools.groupby(device_stream, self.get_interval):
                data_block = pd.DataFrame()
                for line in interval_stream:
                    data_block = data_block.append(pd.DataFrame.from_records([line]))
                    asctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data_block['epoch_time'].max()))
                line_of_output = {'device_id': device_id,  'time_stamp': asctime}
                line_of_output.update({'feature_data': {key: features.feature_input[key](data_block) for key in features.feature_input}})
                yield line_of_output


class CarFeatureExtractor(BaseFeatureExtractor):

    def __init__(self, interval_type='hour'):
        BaseFeatureExtractor.__init__(self, interval_type)
        self.feature_class()

    def feature_class(self):
        self.feature_class = 'car'

    def parse_raw_stream(self, raw_data):
        """generator of a data dictionary from each string of raw data"""
        for line in raw_data:
            device_id, epoch_time, data_type, json_data = line.strip('\n').split('\t')
            device_id = int(device_id)
            epoch_time = int(epoch_time)
            json_data = json.loads(json_data)
            torque = json_data['torque']
            temperature = json_data['temperature']
            yield ({'device_id': device_id, 'epoch_time': epoch_time, 'data_type': data_type, 'torque': torque,
                    'temperature': temperature})

    def get_device_id(self, line):
        return line['device_id']

    def get_interval(self, line):
        time_obj = time.localtime(line['epoch_time'])
        if self.interval_type == 'hour':
            return time_obj.tm_hour
        elif self.interval_type == 'day':
            return time_obj.tm_yday


def parse_cl_args():
    parser = argparse.ArgumentParser(description='print dictionary of features from stream of torque and temperature data')
    parser.add_argument('--username', '-u', help='mysql username', default=None)
    parser.add_argument('--password', '-p', help='mysql password', default=None)
    parser.add_argument('--interval', '-i', choices=['hour', 'day'], default='hour')
    parser.add_argument('--to', '-t', choices=['mysql', 'stdout'], default='stdout')
    return parser.parse_args(sys.argv[1:])

if __name__ == '__main__':
    args = parse_cl_args()
    feature_extractor = CarFeatureExtractor(interval_type=args.interval)
    feature_extractor.get_features(sys.stdin)
    feature_extractor.publish(username=args.username, password=args.password, target=args.to)
