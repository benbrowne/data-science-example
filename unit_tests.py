import unittest
import parse_torque_temp as ptt
import features

Class TestFeatureExtractor(unittest.TestCase):
	def setup(self):
        data= \
        "0	1420156760	drive_unit	{"torque": -0.025472679681420144, "temperature": 0.40841407648251765},\
         0	1420156770	drive_unit	{"torque": 0.23807620959515494, "temperature": -1.1707010518041583},\
         0	1420177780	drive_unit	{"torque": -0.08595670646206277, "temperature": 1.553783619625692},\
         0	1420177790	drive_unit	{"torque": -0.9478755887865989, "temperature": 0.5052556076573897}"

        expected_output = \
        ""{'max_rate_of_change_of_torque': 4.0438910985332983, 'mean_torque': -0.042394730346960757, 'the_99th_percentile_torque': 2.1613366262627722, 'hour': 17, 'device_id': '0'}\
        {'max_rate_of_change_of_torque': 3.9195023130293078, 'mean_torque': -0.093459251401254578, 'the_99th_percentile_torque': 2.3379620654780693, 'hour': 18, 'device_id': '0'}\
        """


	def test_parse_stdin(self):
        self.assertEquals()

	#def test_get_features(self):



if __name__==__main__:
	unittest.main()