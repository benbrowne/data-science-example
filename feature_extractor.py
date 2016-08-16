'''
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
'''

import sys
import json
import time
import numpy as np
import pandas as pd

def parse_data(time_interval, input_stream=stdin):

	#we'll use these to check for new hours or devices
	previous_hour=previous_device_id='none'
	
	#the place we're going to accumulate data until device or hour changes:
	data_list=pd.dataframe()

	#start reading the data
	for line in input_stream:
		device_id,epoch_time,data_type,data=line.strip('\n').split('\t')

		#read epoch time
		epoch_time=float(epoch_time)

		#convert our json string to a dictionary of data and append to our running list
		data_list.append(json.loads(data))
		
		#check if time or device have changed and if so return our feature and clear the data
		if previous_hour!=hour or previous_device_id!=device_id:
			print(func(data_list))
			data_list=pd.dataframe()

		#note the time and device for comparison with the next iteration
		previous_device_id=device_id
		previous_hour=epoch_time.tm_hour


feature_generator(variable='temperature',func=np.std)





