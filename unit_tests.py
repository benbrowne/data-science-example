import unittest
import parse_torque_temp
import features
import generate_stream
import os


class TestFeatureExtractor(unittest.TestCase):

    def setUp(self):
        temp_file = open('temp_data.dat', 'r+')
        data_generator = generate_stream.SimpleStreamGenerator({'device_count': 1, 'seconds_per_reading': 600,
                                                                'day_count': 1, 'output_destination': temp_file})
        data_generator.print_stream(1, 1)
        self.example_raw_data = temp_file.readlines()
        print(self.example_raw_data)

    def test_parse_stdin_returns_dictionaries(self):
        for line_of_data in parse_torque_temp.parse_stdin(self.example_raw_data):
            self.assertIsInstance(eval(line_of_data), dict)

    def test_parse_stdin_returns_expected_keys(self):
        for line_of_data in parse_torque_temp.parse_stdin(self.example_raw_data):
            self.assertEqual({'device_id', 'epoch_time', 'data_type', 'torque', 'temperature'}, set(eval(line_of_data).keys()))

    def test_parse_stdin_returns_expected_length_of_data(self):
        self.assertEqual(len(self.example_raw_data), 24*60*60/600)

    # def test_generate_features(self):
    #     self.assertEqual(expected_output, parse_torque_temp.main(data))
    #     # def test_get_features(self):
    #
    # def tearDown(self):
    #     os.remove('temp_data.dat')


if __name__ == '__main__':
    unittest.main()
