import os
import socket
import json
from chat_utils import *
import pickle

def file_send_init(filename, s):
    # size = os.path.getsize(filename)
    # msg = json.dumps({'filename': filename, "from": s, "size": size})
    # msg = msg.encode()
    # sent = mysend(s, msg)
    # text = myrecv(s)
    # if text == 'y':
    file_send(filename, s)
    # else:
    #     print('request denied')

def file_send(filename, s):
    f = open(filename,'rb')
    l = f.read(1024)
    print(l)
    while l is not None:
        sent = s.send(l)
        print('sending file...')
        # print('Sent ',repr(l))
        l = f.read(1024)
    f.close()

    
def file_rec_init(path, s):
    # text = myrecv(s)
    # print(text)
    # res = input('Do you wish to download the file? (y)es/(n)o')
    # return res
    # if res == 'y':
    #     msg = 'y'
    #     msg = msg.encode()
    #     s.send(msg)
    #     file_rec(s, text, path)
    # else:
    #     msg = 'n'
    #     msg = msg.encode()
    #     s.send(msg)
    #     print('transfer denied')
    file_rec(path, s)

def file_rec(path, s):
    # size = text['size']
    cur_size = 0
    with open(os.path.join(path, 'text.txt'), 'wb') as f:
        print('file opened')
        print('receiving data...')
        while True:
            # print('{:.1%}'.format(cur_size/size))
            data = s.recv(1024)
            cur_size += 1024
            # print('data=%s', (data))
            f.write(data)
            
            if data is None:
                break
            # write data to a file
            
    f.close()
    # msg = 'transfer complete'
    # msg = msg.encode()
    # s.send(msg)
    print('file received')


    pass

def main():
    print(os.path.getsize('/Users/Robert1/Downloads/v_2009_holz_global_iew.pdf'))
    print(type(os.path.getsize('/Users/Robert1/Downloads/v_2009_holz_global_iew.pdf')))
    cur_size = 10
    size = 50
    print('{:.1%}'.format(cur_size/size))
    with open('/Users/Robert1/Downloads/v_2009_holz_global_iew.pdf', 'rb') as f:
        l = f.read()
        print(l)
    msg = {'abc':l}
    msg = pickle.dumps(msg)
    msg = pickle.loads(msg)
    print(type(msg))



if __name__ == '__main__':
    main()