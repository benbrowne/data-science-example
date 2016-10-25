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
        expected_output = [{'max_rate_of_change_of_torque': 1.0406800587201777, 'mean_torque': -0.64489253487332165, 'interval': 365, 'the_99th_percentile_torque': -0.13495930610043455, 'device_id': '0'}, {'max_rate_of_change_of_torque': 1.2049893434937107, 'mean_torque': -0.28742511945577343, 'interval': 1, 'the_99th_percentile_torque': 1.0322372642407294, 'device_id': '0'}]
        car_feature_extractor = parse_torque_temp.CarFeatureExtractor(interval_type='day')
        features = [feature for feature in car_feature_extractor.process_parsed_stream(test_data)]
        self.assertEqual(features, expected_output)

if __name__ == '__main__':
    unittest.main()