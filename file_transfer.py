import os
import socket
import json
from chat_utils import *
import pickle


def file_send(filename, s):
    f = open(filename,'rb')
    size = os.path.getsize(filename)
    filename_rev = filename[::-1]
    pos = filename_rev.find('/')
    filename = filename[-pos:]
    print(filename)
    l = f.read(1024)
    com_size = 0
    while (l):
       s.send(l)
       # print('Sent ',repr(l))
       com_size += 1024
       percent= com_size/size
       if percent < 1 and com_size % 102400 == 0:
           print ("\033[A                             \033[A")
           print("Transferring...{percent:.2%}\r".format(percent = com_size/size))
       l = f.read(1024)
    f.close()


def file_rec(path, s, size, name):


    filename = os.path.join(path, name)
    # print(filename)
    com_size = 0
    with open(filename, 'wb') as f:
        print('receiving data...')
        while True:
            data = s.recv(1024)
            # print(data)
            com_size += 1024
            percent= com_size/size
            if percent < 1 and com_size % 102400 == 0:
                print ("\033[A                             \033[A")
                print("Downloading...{percent:.2%}".format(percent = com_size/size))

            
            if not data:
                break
        # write data to a file
            f.write(data)
            
            # write data to a file
            
    # msg = 'transfer complete'
    # msg = msg.encode()
    # s.send(msg)
    print('file received')


    pass

def main():
    
    
    # with open('/Users/Robert1/Downloads/v_2009_holz_global_iew.pdf', 'rb') as f:
    #     l = f.read(1024)
    #     print(l)
    # msg = pickle.dumps({'action': 'f_exchange', 'data': l, 'size': size, 'filename': 'filename'})
    # print(len(msg))
    # msg = {'abc':l}
    # msg = pickle.dumps(msg)
    # msg = pickle.loads(msg)
    # print(type(msg))
    print(type(socket.gethostbyname(socket.gethostname())))


if __name__ == '__main__':
    main()