import unittest
import parse_torque_temp
import features
import generate_stream
import os


class TestFeatureExtractor(unittest.TestCase):

    def setUp(self):
        raw_data_file = open('temp_data.dat', 'w+')
        data_generator = generate_stream.SimpleStreamGenerator({
            'device_count': 1, 'seconds_per_reading': 600, 'day_count': 1}, output_destination=raw_data_file)
        data_generator.print_stream(1, 1)
        raw_data_file.seek(0)
        self.example_raw_data = raw_data_file.readlines()

        output_file = open('temp_output.dat', 'w+')
        parse_torque_temp.main(self.example_raw_data, out_file=output_file)
        output_file.seek(0)
        self.output = output_file.readlines()

    def test_parse_stdin_returns_dictionaries(self):
        for line_of_data in parse_torque_temp.parse_stdin(self.example_raw_data):
            self.assertIsInstance(line_of_data, dict, msg='{} not equal to {}'.format(line_of_data, dict))

    def test_parse_stdin_returns_expected_keys(self):
        for line_of_data in parse_torque_temp.parse_stdin(self.example_raw_data):
            self.assertEqual({'device_id', 'epoch_time', 'data_type', 'torque', 'temperature'}, set(line_of_data.keys()))

    def test_parse_stdin_returns_expected_length_of_data(self):
        print(len(self.example_raw_data))
        self.assertEqual(len(self.example_raw_data), 24*60*60/600, msg='{} not equal to {}'.format(len(self.example_raw_data), 24*60*60/600))

    def test_generate_features_returns_dictionaries(self):
        for line_of_data in self.output:
            self.assertIsInstance(eval(line_of_data), dict)

    def test_generate_features_returns_a_sensible_length_of_data(self):
        self.assertGreaterEqual(len(self.example_raw_data), len(self.output))

    def tearDown(self):
        os.remove('temp_data.dat')
        os.remove('temp_output.dat')


if __name__ == '__main__':
    unittest.main()
