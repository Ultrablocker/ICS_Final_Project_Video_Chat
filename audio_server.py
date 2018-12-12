import socket
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
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = ('',port)
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        # print('Audio_Server starts...')
        self.socket.bind(self.addr)
        self.socket.listen(2)

        conn,address = self.socket.accept()
        print('remote audio client connected successfully')
        data = b''
        payload_size = struct.calcsize('L')
        self.stream = self.p.open(format = FORMAT,channels = CHANNELS,rate = RATE,output = True,frames_per_buffer = CHUNK)
        #run the infinite loop
        while True:
            while len(data) < payload_size:
                
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            try:
                msg_size = struct.unpack('L', packed_size)[0]
            except:
                break
            while len(data) < msg_size:
                
                data += conn.recv(81920)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frames = pickle.loads(frame_data)
            for frame in frames:
                
                self.stream.write(frame, CHUNK)
            if not self.__running.isSet():
                break
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        self.socket.close()
                
                

    def stop(self):
        self.__running.clear()
        
        # if self.stream is not None:
        #     self.stream.stop_stream()
        #     self.stream.close()
        # self.p.terminate()
        # self.socket.close()

    def set_start(self):
        self.ifstream = not(self.ifstream)
        self.stream.stop_stream()
        self.stream.close()






class Audio_Client(threading.Thread):
    def __init__(self ,ip, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.addr = (ip, port)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.__running = threading.Event()
        self.__running.set()
        # print("AUDIO client starts...")


    def stop(self) :
        self.__running.clear()
        
        # if self.stream is not None:
        #     self.stream.stop_stream()
        #     self.stream.close()
        # self.p.terminate()
        # self.sock.close()


    def run(self):
        while True:
            try:
                self.sock.connect(self.addr)
                break
            except:
                time.sleep(3)
                continue
        # print("AUDIO client connected...")
        self.stream = self.p.open(format=FORMAT, 
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        while self.__running.isSet() and self.stream.is_active():
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = self.stream.read(CHUNK, exception_on_overflow = False)
                frames.append(data)
            senddata = pickle.dumps(frames)
            try:
                self.sock.sendall(struct.pack("L", len(senddata)) + senddata)
            except:
                break

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        self.sock.close()
