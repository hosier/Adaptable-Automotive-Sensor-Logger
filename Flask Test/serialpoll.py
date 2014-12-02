import serial

class SensorData:
	def __init__(self, ser_obj, s_dict, p_start, p_len):
		self.ser = ser_obj
		self.sensor_buffer = s_dict
		self.num_sensors = len(s_dict)
		self.pad_start = p_start
		self.pad_len = p_len

	def ser_read(self):
		while True:
			try:
				data = ord(self.ser.read())
				break
			except:
				continue
		return data
