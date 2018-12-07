import socket                              # Import socket module
class FileServer:
    def __init__(self):
      self.port = 50000                    # Reserve a port for your service every new transfer wants a new port or you must wait.
      self.s = socket.socket()             # Create a socket object
      self.host = ""                       # Get local machine name
      self.s.bind((host, port))            # Bind to the port
      self.s.listen(5)                     # Now wait for client connection.
      self.target = ''
      self.frm = ''

    def set_target(self, target):
        self.target = target

    def start(self):
        self.frm, addr = self.s.accept()
        self.target, addr = self.s.accept()


    def transfer(self, self.frm, self.target):
        data = self.frm.recv(1024)
        while data is not None:
          self.target.send(data)
          data = self.frm.recv(1024)




