import socket
import time

# use local loop back address by default
#CHAT_IP = '127.0.0.1'
# CHAT_IP = socket.gethostbyname(socket.gethostname())

PORT = 10087
SHOWME = False
LEVEL = 1

CHAT_IP = ''#socket.gethostbyname(socket.gethostname())

CHAT_PORT = 11120
SERVER = (CHAT_IP, CHAT_PORT)

VIDEO_PORT = 10087

menu = "\n++++ Choose one of the following commands\n \
        time: calendar time in the system\n \
        who: to find out who else are there\n \
        c _peer_: to connect to the _peer_ and chat\n \
        v _peer_: to connect to the _peer_ and initiate a voice call \n \
        f _peer_: to initiate file transfering\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        p _#_: to get number <#> sonnet\n \
        q: to leave the chat system\n\n"

S_OFFLINE   = 0
S_CONNECTED = 1
S_LOGGEDIN  = 2
S_CHATTING  = 3
S_VIDEO_CHATTING = 4
S_FILETRANSFERING_UP = 5
S_FILETRANSFERING_DOWN = 6
S_WATING_CALL_ENDING = 7

SIZE_SPEC = 5

CHAT_WAIT = 0.2

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    elif state == S_VIDEO_CHATTING:
        print('Video chatting')
    elif state == S_FILETRANSFERING:
        print('Transfering files')
    elif state == S_WATING_CALL_ENDING:
        print('video chatting')
    else:
        print('Error: wrong state')

def mysend(s, msg):
    #append size to message and send it
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:].encode() + msg
    # msg = msg.encode()
    total_sent = 0
    while total_sent < len(msg):
        sent = s.send(msg[total_sent:])
        if sent==0:
            print('server disconnected')
            break
        total_sent += sent
    # print(len(msg))

def myrecv(s):
    #receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    #now receive message
    # print(size)
    msg = b''
    while len(msg) < size:
        text = s.recv(size-len(msg))
        msg += text
        if text == b'':
            print('disconnected')
            break
        msg += text
    #print ('received '+message)
    # print(len(msg))
    return (msg)

def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text) # message goes directly to screen
