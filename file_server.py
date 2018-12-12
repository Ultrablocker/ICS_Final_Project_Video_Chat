import socket
from file_transfer import *
from chat_utils import *
import threading
class FileServer(threading.Thread):
    def __init__(self):
        super(FileServer, self).__init__()
        self.port = 50000                    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             
        self.host = ""                       
        self.s.bind((self.host, self.port))            
        self.s.listen(5)             
        self.target = ''
        self.frm = ''



    def run(self):
        self.frm, addr = self.s.accept()
        # print('connected from', addr)
            
    def recv(self, path, size, name):
        file_rec(path, self.frm, size, name)
    def close():
      self.shutdown(socket.SHUT_RDWR)
      self.close()
      print ("closed")






