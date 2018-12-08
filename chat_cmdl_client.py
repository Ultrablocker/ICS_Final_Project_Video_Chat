
from chat_client_class import *
from audio_server import *
from chat_utils import *
def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    parser.add_argument('--TEST', type=str, default='localhost', help='test IP addr')
    args = parser.parse_args()
    print(args)
    # aserver = Audio_Server(PORT+1)
    # aserver.start()

    client = Client(args)

    client.run_chat()

main()
