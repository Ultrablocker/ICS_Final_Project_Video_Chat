from socket import *
import threading
import pyaudio
import wave
import sys
import zlib
import struct
import pickle
import time
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.5


class Audio_Server(threading.Thread):
	def __init__(self, port):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.socket = socket(AF_INET,SOCK_STREAM)
		self.addr = ('',port)
		self.stream = None
		self.p = pyaudio.Pyaudio()

	def run():
		print('Audio_Server starts...')
		self.socket.bind(self.addr)
		self.socket.listen(1)
		conn,address = self.socket.accept()
		print('remote audio client connected successfully')
		data = b''
		payload_size = struct.calcsize('L')
		self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer = CHUNK
                                  )
		#run the infinite loop
		while True:
			#read size first
			while len(data) < payload_size:
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]

            #read data
            while len(data) < msg_size:
                data += conn.recv(81920)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frames = pickle.loads(frame_data)
            #play the received data
            for frame in frames:
                self.stream.write(frame, CHUNK)


        def stop():
        	self.sock.close()
	        if self.stream is not None:
	            self.stream.stop_stream()
	            self.stream.close()
	        self.p.terminate()