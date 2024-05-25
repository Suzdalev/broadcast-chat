import socket
import sys
import threading
import time

localPORT = 1488


def sender_func(message):
    if len(message) == 0:
        return
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_socket.bind(("0.0.0.0", 0))
    send_socket.sendto(message.encode(), ("255.255.255.255", localPORT))
    send_socket.close()
    return


def receiver_func():
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_server_socket.bind(("0.0.0.0", localPORT))

    while True:
        data = udp_server_socket.recvfrom(4096)
        print(f"\n[{time.localtime()[3]}:{time.localtime()[4]} @ {data[1][0]}]:\n  >> {data[0].decode()}\n")


receiverThread = threading.Thread(target=receiver_func, daemon=True)
receiverThread.start()

sender_func('[---- JOINED ----]')

while True:
    try:
        sender_func(input())
    except KeyboardInterrupt:
        sender_func('[---- LEFT ----]')
        print("chat closed")
        sys.exit(0)
