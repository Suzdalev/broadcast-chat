import socket
import threading
import tkinter.scrolledtext
from tkinter import *
from tkinter import ttk
import time

localPORT = 1488


def send_msg(*args):
    global msg_input

    if len(msg_input.get()) == 0:
        return
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_socket.bind(("0.0.0.0", 0))
    send_socket.sendto(msg_input.get().encode(), ("255.255.255.255", localPORT))
    send_socket.close()

    msg_input.set("")
    return


def receiver_func():
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_server_socket.bind(("0.0.0.0", localPORT))

    while True:
        data = udp_server_socket.recvfrom(4096)
        msg_output.config(state='normal')
        msg_output.insert(END, f"\n[{time.localtime()[3]}:{time.localtime()[4]} @ {data[1][0]}]:\n  >> {data[0].decode()}\n")
        msg_output.config(state='disabled')
        msg_output.see(END)


receiverThread = threading.Thread(target=receiver_func, daemon=True)
receiverThread.start()

root = Tk()
root.title("BRD CHAT")

msg_output = tkinter.scrolledtext.ScrolledText(root,
                                               state='disabled',
                                               )
msg_output.pack(side=TOP, fill=BOTH, expand=True)

msg_input = StringVar()
msg_input.set('[---- joined chat ----]')
send_msg()

msg_entry = ttk.Entry(root, textvariable=msg_input)
msg_entry.pack(side=LEFT, fill=X, expand=True)
send_btn = ttk.Button(root, text="send", command=send_msg)
send_btn.pack(side=RIGHT)

root.bind('<Return>', send_msg)
msg_entry.focus()

root.mainloop()

msg_input.set('[---- left chat ----]')
send_msg()

exit(0)
