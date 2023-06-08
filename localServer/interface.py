import socket
import threading
import argparse
from queue import Queue

# Create an argument parser
parser = argparse.ArgumentParser(description="TCP Bridge Client")
parser.add_argument("-c", "--change", action="store_true", help="Change port from 5760 to 5761")
args = parser.parse_args()

# Define the port to use
PORT = 5761 if args.change else 5760

# Define the function to receive data from the tcp bridge program
def recv_data(sock):
    while True:
        # Receive data from the socket
        data = sock.recv(1024)
        if data:
            print("Received: ", data)

# Create a socket and connect to the tcp bridge program
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('<IP ADDRESS>', PORT))

# Start a thread to receive data from the tcp bridge program
recv_thread = threading.Thread(target=recv_data, args=(sock,))
recv_thread.start()

# Loop to send data to the tcp bridge program
while True:
    # Get user input
    message = input("Enter message to send: ")
    
    # Send the message on the socket
    sock.sendall(message.encode())