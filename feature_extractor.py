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

def parse_data(features, input_stream=stdin, interval,variable='torque'):

	#we'll use these to check for new hours or devices
	previous_hour=previous_device_id='none'
	
	#the place we're going to accumulate data until device or hour changes:
	data_list=[]

	#start reading the data
	for line in input_stream:
		device_id,hour,data_type,data=line.strip('\n').split('\t')

		#convert epoch time to hour of the day
		hour=time.localtime(float(hour)).tm_hour

		#convert our json string to a dictionary of data and append to our running list
		data_list.append(json.loads(data)[variable])
		
		#check if time or device have changed and if so return our feature
		if previous_hour!=hour or previous_device_id!=device_id:
			print(func(data_list))

			#wipe the data for a new time and/or device
			data_list=[]

		#note the time and device for comparison with the next iteration
		previous_device_id=device_id
		previous_hour=hour


feature_generator(variable='temperature',func=np.std)





