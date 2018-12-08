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
    while (l):
       s.send(l)
       # print('Sent ',repr(l))
       l = f.read(1024)
    f.close()


def file_rec(path, s, size, name):

    filename_rev = name[::-1]
    pos = filename_rev.find('/')
    name = name[-pos:]
    print(path)
    filename = os.path.join(path, name)
    print(filename)
    with open(filename, 'wb') as f:
        while True:
            print('receiving data...')
            data = s.recv(1024)
            print(data)
            # print('data=%s', (data))
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