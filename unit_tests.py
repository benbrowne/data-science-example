import StringIO
import unittest

import generate_stream
import parse_torque_temp


class TestFeatureExtractor(unittest.TestCase):

    def test_parse_raw_stream_yields_dictionaries(self):
        """parse_raw_stream should yield a dictionary from each string of raw data"""
        incoming_data_buffer = StringIO.StringIO()
        data_generator = generate_stream.SimpleStreamGenerator({
             'device_count': 1, 'seconds_per_reading': 20000, 'day_count': 1}, output_destination=incoming_data_buffer)
        data_generator.print_stream(1, 1)
        incoming_data_buffer.seek(0)
        car_feature_extractor = parse_torque_temp.CarFeatureExtractor(interval_type='day')
        for line_of_data in car_feature_extractor.parse_raw_stream(incoming_data_buffer.readlines()):
            self.assertIsInstance(line_of_data, dict)

    def test_process_parsed_stream(self):
        test_data = ({'epoch_time': 1420070400, 'torque': -1.1652325642334105, 'temperature': 0.2086529951928006, 'data_type': 'drive_unit', 'device_id': '0'},
                     {'epoch_time': 1420090400, 'torque': -0.12455250551323277, 'temperature': -0.10835061835785172, 'data_type': 'drive_unit', 'device_id': '0'},
                     {'epoch_time': 1420110400, 'torque': 1.0804368379804778, 'temperature': 0.24757520808954456, 'data_type': 'drive_unit', 'device_id': '0'},
                     {'epoch_time': 1420130400, 'torque': -0.6802021990509769, 'temperature': 0.6486716331588083, 'data_type': 'drive_unit', 'device_id': '0'},
                     {'epoch_time': 1420150400, 'torque': -0.5475751664617249, 'temperature': -1.7881683713154541, 'data_type': 'drive_unit', 'device_id': '0'})
        expected_output = "{'max_rate_of_change_of_torque': 1.0406800587201777, 'mean_torque': -0.64489253487332165, 'interval': 365, 'the_99th_percentile_torque': -0.13495930610043455, 'device_id': '0'}\n{'max_rate_of_change_of_torque': 1.2049893434937107, 'mean_torque': -0.28742511945577343, 'interval': 1, 'the_99th_percentile_torque': 1.0322372642407294, 'device_id': '0'}\n"
        feature_buffer = StringIO.StringIO()
        car_feature_extractor = parse_torque_temp.CarFeatureExtractor(interval_type='day', out_file=feature_buffer)
        car_feature_extractor.process_parsed_stream(test_data)
        self.assertEqual(feature_buffer.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()


#old unit tests for reference:

# import unittest
# import parse_torque_temp
# import features
# import generate_stream
# import os
#
#
# class TestFeatureExtractor(unittest.TestCase):
#
#     def setUp(self):
#         raw_data_file = open('temp_data.dat', 'w+')
#         data_generator = generate_stream.SimpleStreamGenerator({
#             'device_count': 1, 'seconds_per_reading': 600, 'day_count': 1}, output_destination=raw_data_file)
#         data_generator.print_stream(1, 1)
#         raw_data_file.seek(0)
#         self.example_raw_data = raw_data_file.readlines()
#
#         output_file = open('temp_output.dat', 'w+')
#         parse_torque_temp.main(self.example_raw_data, out_file=output_file)
#         output_file.seek(0)
#         self.output = output_file.readlines()
#
#     def test_parse_stdin_returns_dictionaries(self):
#         for line_of_data in parse_torque_temp.parse_stdin(self.example_raw_data):
#             self.assertIsInstance(line_of_data, dict, msg='{} not equal to {}'.format(line_of_data, dict))
#
#     def test_parse_stdin_returns_expected_keys(self):
#         for line_of_data in parse_torque_temp.parse_stdin(self.example_raw_data):
#             self.assertEqual({'device_id', 'epoch_time', 'data_type', 'torque', 'temperature'}, set(line_of_data.keys()))
#
#     def test_parse_stdin_returns_expected_length_of_data(self):
#         print(len(self.example_raw_data))
#         self.assertEqual(len(self.example_raw_data), 24*60*60/600, msg='{} not equal to {}'.format(len(self.example_raw_data), 24*60*60/600))
#
#     def test_generate_features_returns_dictionaries(self):
#         for line_of_data in self.output:
#             self.assertIsInstance(eval(line_of_data), dict)
#
#     def test_generate_features_returns_a_sensible_length_of_data(self):
#         self.assertGreaterEqual(len(self.example_raw_data), len(self.output))
#
#     def tearDown(self):
#         os.remove('temp_data.dat')
#         os.remove('temp_output.dat')
#
#
# if __name__ == '__main__':
#     unittest.main()
