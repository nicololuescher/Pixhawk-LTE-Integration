import argparse
import socket
import threading

class Sender:
    def __init__(self, port, verbose=False):
        self.port = port
        self.verbose = verbose
        self.peer = None
        self.lock = threading.Lock()
        self.connected = False
        self.conn = None

    def set_peer(self, peer):
        self.peer = peer

    def handle_client(self):
        ip = '0.0.0.0'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, self.port))
        sock.listen()

        while True:
            conn, addr = sock.accept()
            with self.lock:
                self.connected = True
                self.conn = conn
            print(f"Client connected on port {self.port}: {addr}")

            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if self.verbose:
                        print(f"Received on port {self.port}: ", data)
                    with self.lock:
                        if self.peer and self.peer.connected:
                            self.peer.forward(data)
                except (ConnectionResetError, ConnectionAbortedError, OSError):
                    break

            with self.lock:
                self.connected = False
            print(f"Client disconnected on port {self.port}")

    def forward(self, data):
        with self.lock:
            if self.connected:
                self.conn.sendall(data)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="enable verbose output")
    args = parser.parse_args()

    sender1 = Sender(5760, verbose=args.verbose)
    sender2 = Sender(5761, verbose=args.verbose)

    sender1.set_peer(sender2)
    sender2.set_peer(sender1)

    thread1 = threading.Thread(target=sender1.handle_client)
    thread2 = threading.Thread(target=sender2.handle_client)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
