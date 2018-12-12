
from chat_client_class import *

def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    parser.add_argument('-l', type=str, default='localhost', help='test IP addr')
    args = parser.parse_args()

    client = Client(args)
    client.run_chat()

main()
