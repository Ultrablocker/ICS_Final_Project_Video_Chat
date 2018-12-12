"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle
from chat_utils import *
import chat_group as grp
# from Feed import Feed


class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.user_ip = {}
        self.client_call_avail={}
        self.all_sockets = []
        self.group = grp.Group()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        # self.feed = Feed()

    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)



    def login(self, sock):
        # print(sock)
        # read the msg that should have login code plus username
        try:
            msg = pickle.loads(myrecv(sock))
            print(msg)
            if len(msg) > 0:

                if msg["action"] == "login":
                    ip = msg["ip"]
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        # move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        # add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        #add ip
                        self.user_ip[name] = ip
                        #set call available state
                        self.client_call_avail[name] = 'available'
                        # load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name] = pickle.load(
                                    open(name + '.idx', 'rb'))
                            except IOError:  # chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)

                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, pickle.dumps(
                            {"action": "login", "status": "ok"}))
                    else:  # a client under this name has already logged in
                        mysend(sock, pickle.dumps(
                            {"action": "login", "status": "duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print('wrong code received')
            else:  # client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pickle.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        del self.user_ip[name]
        del self.client_call_avail[name]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

# ==============================================================================
# main command switchboard
# ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        try:
            msg = myrecv(from_sock)
        except UnicodeDecodeError:
            msg = from_sock.recv(1024)

        if len(msg) > 0:
            # ==============================================================================
            # handle connect request this is implemented for you
            # ==============================================================================


            msg = pickle.loads(msg)
            # print(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = pickle.dumps({"action": "connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = pickle.dumps(
                        {"action": "connect", "status": "success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, pickle.dumps(
                            {"action": "connect", "status": "request", "from": from_name}))
                else:
                    msg = pickle.dumps(
                        {"action": "connect", "status": "no-user"})
                mysend(from_sock, msg)
# ==============================================================================
# video connect
# ==============================================================================

            elif msg['action'] == 'video_connect':
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = pickle.dumps({"action": "video_connect", "status": "self"})
                elif to_name not in self.client_call_avail:
                    msg = pickle.dumps(
                        {"action": "video_connect", "status": "no-user"})
                elif self.client_call_avail[to_name] == "busy":
                    msg = pickle.dumps({"action": "video_connect", "status": "busy"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    self.client_call_avail[from_name] = "busy"
                    self.client_call_avail[to_name] = "busy"
                    from_ip = self.user_ip[from_name]
                    to_ip = self.user_ip[to_name]
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    #the_guys = self.group.list_me(from_name)
                    msg = pickle.dumps(
                        {"action": "video_connect", "status": "success","target_ip":to_ip})
                    # for g in the_guys[1:]:
                    #     to_sock = self.logged_name2sock[g]
                    mysend(to_sock, pickle.dumps(
                        {"action": "video_connect", "status": "request", "from": from_name,"target_ip":from_ip}))

                else:
                    msg = pickle.dumps(
                        {"action": "video_connect", "status": "no-user"})
                mysend(from_sock, msg)

                
                

                pass
# ==============================================================================
# handle messeage exchange: IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                """
                Finding the list of people to send to and index message
                """
                # IMPLEMENTATION
                # ---- start your code ---- #

                message = msg['message']
                self.indices[from_name].add_msg_and_index(message)
                # self.indices[from_name].msgs.append(time.strftime('%d.%m.%y,%H:%M', time.localtime()))
                # self.indices[from_name].msgs.append(from_name)
                


                # ---- end of your code --- #

                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]

                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    mysend(to_sock, pickle.dumps(msg))

                    # ---- end of your code --- #










            elif msg['action'] == 'f_connect':
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = pickle.dumps({"action": "f_connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = pickle.dumps(
                        {"action": "f_connect", "status": "success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, pickle.dumps(
                            {"action": "f_connect", "status": "request", "from": from_name}))

                else:
                    msg = pickle.dumps(
                        {"action": "f_connect", "status": "no-user"})
                mysend(from_sock, msg)



            elif msg['action'] == 'f_confirm':
                from_name = self.logged_sock2name[from_sock]
                print('f_confirm received')

                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, pickle.dumps(msg))

            elif msg['action'] == 'f_confirm_2':
                from_name = self.logged_sock2name[from_sock]
                print('f_confirm_2 received')

                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, pickle.dumps(msg))
            elif msg['action'] == 'f_confirm_3':
                from_name = self.logged_sock2name[from_sock]
                print('f_confirm_3 received')

                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, pickle.dumps(msg))


                
                

                pass





# ==============================================================================
# the "from" guy has had enough (talking to "to")!
# ==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                # g = the_guys.pop()
                # to_sock = self.logged_name2sock[g]
                # mysend(to_sock, pickle.dumps(
                #         {"action": "disconnect", 'from': from_name, 'is_one': False}))
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, pickle.dumps(
                        {"action": "disconnect", "msg": "everyone left, you are alone", 'from': from_name, 'is_one': True}))

# ==============================================================================
# video disconnect
# ==============================================================================
            elif msg["action"] == "f_disconnect":
                print("received")
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                self.client_call_avail[from_name] = "available"

                the_guys.remove(from_name)
                g = the_guys.pop()
                

            elif msg["action"] == "v_disconnect":
                print("received")
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                self.client_call_avail[from_name] = "available"

                the_guys.remove(from_name)
                g = the_guys.pop()
                self.client_call_avail[g] = "available"
                to_sock = self.logged_name2sock[g]
                mysend(to_sock,pickle.dumps({"action":"v_disconnect"}))
                print("sent")
# ==============================================================================
#                 listing available peers: IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "list":

                # IMPLEMENTATION
                # ---- start your code ---- #
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all(from_name)

                # ---- end of your code --- #
                mysend(from_sock, pickle.dumps(
                    {"action": "list", "results": msg}))
# ==============================================================================
#             retrieve a sonnet : IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "poem":

                # IMPLEMENTATION
                # ---- start your code ---- #
                
                poem = '\n'.join(self.sonnet.get_poem(int(msg['target'])))

                # ---- end of your code --- #

                mysend(from_sock, pickle.dumps(
                    {"action": "poem", "results": poem}))
# ==============================================================================
#                 time
# ==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, pickle.dumps(
                    {"action": "time", "results": ctime}))
# ==============================================================================
#                 search: : IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "search":

                # IMPLEMENTATION
                # ---- start your code ---- #
                search_rslt = []
                for user in self.indices.keys():
                    m = self.indices[user].search_time(msg['target'])
                    print(m)
                    for x in m:
                        for n in x:
                            search_rslt.append(n)
                        search_rslt.append('['+ user + ']' + '\n')
                search_rslt = ' '.join(search_rslt).lstrip()


                
                print('server side search: ' + search_rslt)

                # ---- end of your code --- #
                mysend(from_sock, pickle.dumps(
                    {"action": "search", "results": search_rslt}))


# ==============================================================================
#                 the "from" guy really, really has had enough
# ==============================================================================

        else:
            # client died unexpectedly
            self.logout(from_sock)

# ==============================================================================
# main loop, loops *forever*
# ==============================================================================


    def run(self):
        print('starting server...')
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])

            print('checking logged clients..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
                    # time.sleep(2)
            # print('selected')
            print('checking new clients..')
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            print('checking for new connections..')
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
