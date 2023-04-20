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

    #message init
    msg = input("sender> ")
    #testing correct user input
    while(msg.split()[0] != "send"):
        msg = input("incorrect pharasing. supposed to be 'send (insert text here)'. try again please\nsender> ")
    letter_list = [char for char in msg]
    
    #im not sure
    while True:
        while wsc < ws:
            






"""
RECEIVER
"""
def receiver(self_port, peer_port, window_size, type, value):
    sport = peer_port
    rport = self_port
    ws = window_size
    pass




"""
SENDING
"""
def send():
    pass




"""
RECEIVING
"""
def recv():
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