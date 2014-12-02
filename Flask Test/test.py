from flask import Flask, jsonify, render_template, request
import json
import Queue
import random
import serial
import threading
import time
app = Flask( __name__ )

@app.route( '/_random_number' )
def get_data():
	if len( sensor_buffer.values()[0] ) == 0: return
	else: return jsonify( result=[ i.pop(0) for i in sensor_buffer.values() ] )

@app.route( '/' )
def index():
	return render_template( 'index.html' )

def parse_data():
	wait_for_start()
	while True:
		data = q.get()
		data += (q.get()<<8)
		q.get()
		wait_for_start()

def serial_poll():
	while True:
		data = ser_read()
		q.put(data)

def serial_init():
	ser = serial.Serial()
	ser.baudrate = 9600
	ser.port = '/dev/ttyACM0'
	ser.open()

	return ser

def ser_read():
	while True:
		try:
			data = ord(ser.read())
			print data
			break
		except:
			continue
	return data

def wait_for_end():
	pad_len = 5
	while True:
		pad = q.get()
		if pad == pad_len-1:
			break

def wait_for_start():
	pad_start = 0
	pad_len = 5
	lst = []
	while len(lst) != pad_len:
		while q.empty(): continue
		data = q.get()
		if len(lst) == 0:
			if data == 0: lst.append(data)
		else:
			if data == len(lst): lst.append(data)

def foo( s ):
	while True:
		data = ser_read()
		s['sensor1'].append(data)
		s['sensor3'].append(data)
		s['sensor2'].append(data/100.0)

if __name__ == "__main__":
	global q
	global sensor_buffer
	global ser
	q = Queue.Queue()
	sensor_buffer = { 'sensor1': [], 'sensor2': [], 'sensor3': [] }
	ser = serial_init()
	app.debug = True

	parse_thread = threading.Thread( target=foo, args=(sensor_buffer, ) )
	#parse_thread = threading.Thread( target=parse_data, args=(sensor_buffer, ) )
	#serial_thread = threading.Thread( target=serial_poll, args=( ) )
	parse_thread.daemon = True
	#serial_thread.daemon = True
	parse_thread.start()
	#serial_thread.start()
	
	app.run(port=5015)

	while True:
		time.sleep( .1 )
