"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
from file_transfer import *
import os
import pickle
import sys
import time
from file_server import FileServer
import socket
import argparse
from audio_server import *

class ClientSM:
    def __init__(self, s, ip):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.ip = ip
        self.target_ip = ''

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = pickle.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = pickle.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)

    def file_connect_to(self, peer):

        msg = pickle.dumps({'action': 'f_connect', "target":peer})
        mysend(self.s, msg)
        response = pickle.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with  '+ self.peer + "you may now transfer files!'\n" 
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)




    def video_connect_to(self, peer):
        msg = pickle.dumps({"action":"video_connect", "target":peer})
        mysend(self.s, msg)
        response = pickle.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True,response["target_ip"])
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False,0)

    def v_disconnect(self):
        msg = pickle.dumps({"action":"v_disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def f_disconnect(self):
        msg = pickle.dumps({"action":"f_disconnect"})
        mysend(self.s, msg)
        self.out_msg += '\n'
        self.peer = ''


    def disconnect(self):
        msg = pickle.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):

        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================








        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, pickle.dumps({"action":"time"}))
                    time_in = pickle.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, pickle.dumps({"action":"list"}))
                    logged_in = pickle.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                #-----------------------------------implemented for final project-------------------------------------- 




                elif my_msg[0] == 'v':
                    pass
                    peer = my_msg[1:]
                    peer = peer.strip()
                    result,ip = self.video_connect_to(peer)
                    if result:
                        self.target_ip = ip
                        self.state = S_VIDEO_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'


                elif my_msg[0] == 'f':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.file_connect_to(peer) == True:
                        self.state = S_FILETRANSFERING_UP
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'









                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, pickle.dumps({"action":"search", "target":term}))
                    search_rslt = pickle.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, pickle.dumps({"action":"poem", "target":poem_idx}))
                    poem = pickle.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        self.out_msg = self.out_msg + poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = pickle.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " pickle.loads failed " + str(err)
                    return self.out_msg
            
                if peer_msg["action"] == "connect":

                    # ----------your code here------#
                    self.out_msg += peer_msg['from'] + ' joined'
                    self.state = S_CHATTING

                if peer_msg['action'] == 'f_connect':
                    self.out_msg += peer_msg['from'] + ' starts a file transfer!'
                    self.peer = peer_msg['from']
                    self.state = S_FILETRANSFERING_DOWN

                    
                if peer_msg["action"] == "video_connect":
                    self.out_msg += peer_msg['from'] + ' starts a voice call'
                    self.target_ip = peer_msg["target_ip"]
                    self.peer = peer_msg['from']
                    self.state = S_VIDEO_CHATTING


                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_VIDEO_CHATTING:
            self.aclient = Audio_Client(self.target_ip, PORT+1)
            self.aserver = Audio_Server(PORT+1)
            self.aserver.start()  
            time.sleep(1)
            self.aclient.start()
            self.state = S_WATING_CALL_ENDING
        elif self.state == S_WATING_CALL_ENDING:
            if len(my_msg) > 0:     # my stuff going out                
                if my_msg == 'end':                    
                    self.v_disconnect()                    
                    self.aserver.stop()
                    time.sleep(1)
                    self.aclient.stop()
                    # print("audio client disconnect")
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:
                peer_msg = pickle.loads(peer_msg)
                if peer_msg["action"] == "v_disconnect":
                    self.aserver.stop()
                    self.aclient.stop()                    
                    self.out_msg += 'You are disconnected from' + self.peer + '\n'
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if self.state == S_LOGGEDIN:
                self.out_msg += menu




        elif self.state == S_FILETRANSFERING_UP:
            print('initializing file transfer...')
            print('waiting for response...')
            msg = pickle.loads(myrecv(self.s))
            s_file = socket.socket()
            host = msg['ip']
            port = msg['port']
            s_file.connect((host, port))
            # This checks whether the folder has a to_transfer and a downloads folder, if no, create them
            cur_path = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(cur_path, 'downloads')
            if not os.path.exists(filepath):
                os.makedirs('downloads')
            cur_path = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(cur_path, 'to_transfer')
            if not os.path.exists(filepath):
                os.makedirs('to_transfer')
            print('to transfer, put the file you wish to transfer in the folder \'to_transfer\' under the path which this program is\nthe files you downloaded will be in the folder \'downloads\'\n')
            lst = os.listdir(filepath)
            for x in range(len(lst)):
                print('({})'.format(x) + str(lst[x]))
            mark = int(input('which one do you want to transfer?'))
            filename = os.path.join(filepath,lst[mark])
            mysend(self.s, pickle.dumps({"action":'f_confirm_2', 
                'filename': filename,
                'filesize': os.path.getsize(filename)}))
            print('waiting for response...')
            msg = pickle.loads(myrecv(self.s))
            if msg['go']:
                # print('transferring...')
                file_send(filename, s_file)
            self.f_disconnect()
            self.out_msg += menu
            self.state = S_LOGGEDIN
            print('file transferred')

        elif self.state == S_FILETRANSFERING_DOWN:
            print('initializing file transfer')
            cur_path = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(cur_path, 'downloads')
            if not os.path.exists(filepath):
                os.makedirs('downloads')
            # print('peer_msg:', peer_msg)
            # while True:
            file_server = FileServer()
            file_server.start()
            print('connected from', self.peer)
            # print(file_server.port)
            mysend(self.s, pickle.dumps({"action":'f_confirm', 
                'ip': self.ip,
                'port': file_server.port}))
            
            msg = pickle.loads(myrecv(self.s))
            filename = msg['filename']
            filesize = msg['filesize']
            filename_rev = filename[::-1]
            pos = filename_rev.find('/')
            filename = filename[-pos:]
            if filesize > 1024 and filesize < 1024**2:
                printoutsize = str(round(filesize / 1024, 2)) + 'KB'
            elif filesize > 1024**2 and filesize < 1024**3:
                printoutsize = str(round(filesize / 1024**2, 2)) + 'MB'
            elif filesize > 1024**3 and filesize < 1024**4:
                printoutsize = str(round(filesize / 1024**3, 2)) + 'GB'
            print('file name:',filename, 'file size:', printoutsize)

            mark = print(input('--------------------Press any key to continue--------------------\n'))

            mysend(self.s, pickle.dumps({"action":'f_confirm_3', 
                'go': True}))
            file_server.recv(filepath, filesize, filename)


            # res = file_rec(filepath, self.s)
            # print('all files received')
            # time.sleep(3)

            self.out_msg += menu
            self.state = S_LOGGEDIN









        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, pickle.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
  

                # ----------your code here------#
                peer_msg = pickle.loads(peer_msg)
                if peer_msg['action'] == 'exchange':
                    self.out_msg += peer_msg['from'] + peer_msg['message']
                if peer_msg['action'] == 'disconnect':
                    # self.out_msg += peer_msg['from'] + ' has left the chat.'
                    # if peer_msg['is_one']:
                    # self.disconnect()
                    self.out_msg += '\n' + peer_msg['msg']
                    self.state = S_LOGGEDIN


                if peer_msg["action"] == "connect":
                    self.out_msg += peer_msg['from'] + ' joined'
                



                # ----------end of your code----#
                
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
