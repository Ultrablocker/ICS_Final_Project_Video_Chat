"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
from file_transfer import *
import os
import pickle
import time

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.f_peer = ''

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
            self.f_peer = peer
            self.out_msg += 'You are connected with '+ self.peer + "you may now transfer files!'\n" 
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)




    def video_connect_to(self, peer):
        pass
        msg = pickle.dumps({"action":"video_connect", "target":peer})
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

    def vsend(self, framestring, from_sock, to_sock):
        pass
        totalsent = 0
        metasent = 0
        length =len(framestring)
        lengthstr=str(length).zfill(8)

        while metasent < 8 :
            sent = self.to_sock.send(lengthstr[metasent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            metasent += sent
        
        
        while totalsent < length :
            sent = self.to_sock.send(framestring[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent += sent

    def vreceive(self, from_sock, to_sock):
        pass
        totrec=0
        metarec=0
        msgArray = []
        metaArray = []
        while metarec < 8:
            chunk = self.to_sock.recv(8 - metarec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            metaArray.append(chunk)
            metarec += len(chunk)
        lengthstr= ''.join(metaArray)
        length=int(lengthstr)

        while totrec<length :
            chunk = self.sock.recv(length - totrec)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            msgArray.append(chunk)
            totrec += len(chunk)
        return ''.join(msgArray)






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
                    if self.video_connect_to(peer):
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
                    self.out_msg += peer_msg['from'] + ' joined'
                    self.state = S_FILETRANSFERING_DOWN

                    



                    # ----------end of your code----#
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_VIDEO_CHATTING:
            pass
            while True:
                frame = self.vreceive(from_sock, to_sock)
                self.feed.set_frame(frame)
                frame = self.feed.get_frame()
                self.vsend(frame, from_sock, to_sock)

        elif self.state == S_FILETRANSFERING_UP:
            print('initializing file transfer...')
            # This checks whether the folder has a to_transfer and a downloads folder, if no, create them
            cur_path = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(cur_path, 'downloads')
            if not os.path.exists(filepath):
                os.makedirs('downloads')
            cur_path = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(cur_path, 'to_transfer')
            if not os.path.exists(filepath):
                os.makedirs('to_transfer')
            print('to transfer, put the file you wish to transfer in the folder \'to_transfer\' under the path which this program is')
            print('the files you downloaded will be in the folder \'downloads\'')
            # swi = input('Do you wish to start? (y)es/(n)o')
            lst = os.listdir(filepath)
            for x in range(len(lst)):
                print('({})'.format(x) + str(lst[x]))
            mark = int(input('which one do you want to transfer?'))
            file_send(os.path.join(filepath,lst[mark]), self.s)

            time.sleep(5)

            print('all files tranferred')
            self.state = S_LOGGEDIN

        elif self.state == S_FILETRANSFERING_DOWN:
            cur_path = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(cur_path, 'downloads')
            if not os.path.exists(filepath):
                os.makedirs('downloads')
            while True:
                res = file_rec(filepath, self.s)
                if res:
                    break
                # time.sleep(5)
            print('all files received')
            # self.state = S_LOGGEDIN




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
