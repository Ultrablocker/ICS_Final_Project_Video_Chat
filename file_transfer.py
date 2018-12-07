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
    
    l = f.read()
    m = {'action': 'f_exchange', 'data': l, 'size': size, 'filename': filename}
    print(m['size'])
    m = pickle.dumps(m)
    mysend(s, m)
    f.close()

    
def file_rec_init(path, s):
    text = myrecv(s)
    print(type(text))

    file_rec(path, s)

def file_rec(path, s):
    # size = text['size']
    # cur_size = 0
    # print(myrecv(s))
    msg = pickle.loads(myrecv(s))
    filename = msg['filename']
    print(filename)
    data = msg['data']
    print(type(data))
    filename = os.path.join(path, filename)
    with open(filename, 'wb') as f:
        print('file opened')
        print('receiving data...')
        # print(data)
        f.write(data)
            
            # write data to a file
            
    # msg = 'transfer complete'
    # msg = msg.encode()
    # s.send(msg)
    print('file received')


    pass

def main():
    
    
    with open('/Users/Robert1/Downloads/v_2009_holz_global_iew.pdf', 'rb') as f:
        l = f.read(1024)
        print(l)
    msg = pickle.dumps({'action': 'f_exchange', 'data': l, 'size': size, 'filename': 'filename'})
    print(len(msg))
    msg = {'abc':l}
    msg = pickle.dumps(msg)
    msg = pickle.loads(msg)
    print(type(msg))



if __name__ == '__main__':
    main()