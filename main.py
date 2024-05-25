import socket
import sys
import threading

localPORT = 1488

def senderFunc(message):
    if len(message) == 0:
        return
    sendsock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    sendsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sendsock.bind(("0.0.0.0", 0))
    sendsock.sendto(message.encode(), ("255.255.255.255", localPORT))
    sendsock.close()
    return


def receiverFunc():
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPServerSocket.bind(("0.0.0.0", localPORT))

    while (True):
        data = UDPServerSocket.recvfrom(4096)
        print(f"{data[1]}:  >> {data[0].decode()}")


receiverThread = threading.Thread(target=receiverFunc, daemon=True)
receiverThread.start()

senderFunc('[---- JOINED ----]')

while (True):
    try:
        senderFunc(input())
    except KeyboardInterrupt:
        senderFunc('[---- LEFT ----]')
        print("chat closed")
        sys.exit(0)
