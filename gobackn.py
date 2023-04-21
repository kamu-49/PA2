from socket import * #for socket programming
import threading #for multithreading for multiple clients
import sys #for exit calls and input calls
import time #for sleep
import signal #for silent quit
import random

"""
DECLARATIONS
"""
byte = 8
letter = [byte]
sequence_number = [16]
data_packet = [letter + len(sequence_number)]
data_packet_size = len(data_packet)
time_limit = 0.5
# probability = 0.15
# determine = random.randint(3,7)
holder = 0




"""
SENDER
"""
def sender(self_port, peer_port, window_size, type, value):
    #declarations
    sport = self_port
    rport = peer_port
    ws = window_size
    saddr = ('', sport)
    raddr = ('', rport)
    wsc = 0 #window size counter

    #socket init
    sock = socket(AF_INET, SOCK_DGRAM)
    socket.bind(saddr)

    #buffer init
    buffer = [data_packet_size*ws]
    buff_hold = [data_packet*ws]

    while True:
        #wait for receiver recognition
        hold, addr = sock.recvfrom(4096)
        print("test break\n")
        if hold.decode() == "alive":
            break

    #message init
    msg = input("sender> ")
    #testing correct user input
    while(msg.split()[0] != "send"):
        msg = input("incorrect pharasing. supposed to be 'send (insert text here)'. try again please\nsender> ")
    reduced_msg = msg[5:]
    letter_list = [char for char in reduced_msg]

    #sending window
    while wsc < len(letter_list):            # if we haven't reached the end yet
        true_ws = min(ws, len(letter_list)-(wsc+ws))
        if true_ws < 0:
            t = ws + true_ws
            true_ws = t
        buffer = snd_s() #needs the window size for sure and the char lsit
        recv_s()
        wsc+=1
    print("Summary: this is where I will put the summary for everything")
    sys.exit()




"""
RECEIVER
"""
def receiver(self_port, peer_port, window_size, type, value):
    #declarations
    sport = peer_port
    rport = self_port
    saddr = ('', sport)
    raddr = ('', rport)
    ws = window_size
    wsl = 0
    
    #socket init
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(raddr)

    #buffer init
    buffer = [data_packet_size*ws]
    buff_hold = [data_packet*ws]

    #receiver is alive
    hi = "alive"
    sock.sendto(hi.encode(), saddr)

    #receiving window
    while True:
        recv_r()
        snd_r()





"""
SENDING
"""
def snd_r():
    pass




def snd_s():
    pass




"""
RECEIVING
"""
def recv_r():
    pass




def recv_s():
    pass




"""
BINARY TO SYMBOL
"""
def bts():
    pass




"""
SYMBOL TO BINARY
"""
def stb():
    pass