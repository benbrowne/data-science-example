"""Simple time-series simulator.

Invocation:
    python generate_stream.py --help

This source has been tested on Python 2.7 and requires only native libraries.
"""
import argparse
import json
import random
import sys


class SimpleStreamGenerator(object):
    """Generate a stream of data of the following form:

        1001    1420070400  drive_unit  '{"torque": 0, "temperature": 15.1}'
        ...
        1001    1420088888  drive_unit  '{"torque": 10.3, "temperature": 60.4}'
        1002    1420070400  drive_unit  '{"torque": 429.8, "temperature": 86.2}'
        ...

    The columns are 'device_ID', 'epoch_time', 'data_type', 'data'. By default each are
    tab-delimited. The 'data' is JSON formatted.

    The stream is sorted primarily by 'device_id' and secondarily by 'epoch_time'.

    This stream is very simple in that:
        -- data is emitted regularly (every 10 seconds by default)
        -- each data point is drawn from N(0, 1)
    """

    template_configuration = {
        'field_delimiter': {'type': str, 'default': '\t'},
        'start_epoch': {'type':int, 'default': 1420070400},  # 2015-01-01 00:00:00"
        'seconds_per_reading': {'type': int, 'default': 10},
        'data_type': {'type': str, 'default': 'drive_unit'},
        'output_destination': {'type': file, 'default': sys.stdout}
    }

    # pylint: disable=no-member
    def __init__(self, instance_configuration):
        """
        Args:
            instance_configuration (dictionary): optionally override variables defined by
                                                 template_configuration

        Raises:
            ValueError: if improperly configured
        """
        # Set member attributes based on template_configuration and instance_configuration
        for var_name, var in self.template_configuration.items():
            value = instance_configuration.get(var_name, var['default'])
            assert isinstance(value, var['type'])
            setattr(self, var_name, value)

        # Validate configuration
        if self.seconds_per_reading > 86400:
            raise ValueError('seconds_per_reading is %d but should be <= 86400 (24 hours)' %
                             self.seconds_per_reading)

        # Additional (static) configuration
        self.data_keys = ['temperature', 'torque']


    def print_stream(self, device_count, day_count):
        """Print stream for all devices and days

        Args:
            device_count (int)
            day_count (int)

        Returns:
            None

        Side effect:
            Prints to self.output_destination
        """
        for device_id in range(device_count):
            self.print_device_stream(device_id, day_count)

    def print_device_stream(self, device_id, day_count):
        """Print stream for a single device over all days

        Args:
            device_id (int)
            day_count (int)

        Returns:
            None

        Side effect:
            Prints to self.output_destination
        """
        for seconds in range(0, day_count * 86400, self.seconds_per_reading):
            row = [device_id,
                   self.start_epoch + seconds,
                   self.data_type,
                   self.generate_data()]
            print >> self.output_destination, self.field_delimiter.join([str(e) for e in row])

    def generate_data(self):
        """Generate JSON data

        Returns:
            JSON formatted data (string)
        """
        data = {name: random.normalvariate(0, 1) for name in self.data_keys}
        return json.dumps(data)


####################################################################################################
# SUPPORT COMMAND-LINE INVOCATION
####################################################################################################
def parse_command_line_args(cl_args):
    """Parse arguments of the form ['---device_count', 1, ...]

    Args:
        cl_args (list): e.g. sys.argv[1:]

    Returns:
        known arguments (dict)
    """
    parser = argparse.ArgumentParser(usage='Generate a stream of device time-series')

    # Add SimpleStreamGenerator arguments
    for var_name, var in SimpleStreamGenerator.template_configuration.items():
        parser.add_argument(
            '--' + var_name,
            default=var['default'],
            type=var['type'],
            help="default: %(default)s")

    # Add per-run arguments
    parser.add_argument('--device_count', default=1, type=int)
    parser.add_argument('--day_count', default=1, type=int)

    # Parse command-line arguments
    args_known = parser.parse_args(cl_args)
    return dict(args_known._get_kwargs())  # pylint: disable=protected-access


def main(cl_args):
    """Support command-line invocation

    Args:
        cl_args (list): e.g. sys.argv[1:]

    Returns:
        None

    Side effect:
        Prints stream of data, by default to sys.stdout
    """
    args = parse_command_line_args(cl_args)
    stream_generator = SimpleStreamGenerator(args)
    stream_generator.print_stream(args['device_count'], args['day_count'])


if __name__ == '__main__':
    main(sys.argv[1:])
