from socket import *
import sys
import time
import signal
import random


########## DECLARATIONS ##########
byte = 8
letter = [byte]
sequence_number = [32]
data_packet = [letter + len(sequence_number)]
data_packet_size = len(data_packet)
timeout = 0.5
holder = 0


######### SENDER ##########
def sender(self_port, peer_port, window_size, timeout_type, timeout_value):
    sport = self_port
    rport = peer_port
    saddr = ('',sport)
    raddr = ('',rport)
    ws = window_size
    type = timeout_type
    val = timeout_value
    seq_index = 0

    #sock init
    sock = socket(AF_INET, SOCK_DGRAM)
    socket.bind(saddr)

    #buffer init
    buffer = [data_packet_size*ws]

    #receiver recognition
    while True:
        hold, addr = sock.recvfrom(4096)
        if hold.decode() == "alive":
            break

    #non-blocking
    sock.setblocking(False)
    sock.settimeout(0.5)

    #message init
    msg = input("sender> ")
    #testing correct user input
    while(msg.split()[0] != "send"):
        msg = input("incorrect pharasing. supposed to be 'send (insert text here)'. try again please\nsender> ")
    reduced_msg = msg[5:]
    letter_list = [char for char in reduced_msg]

    #sending window, curtain method; perfect world
    while seq_index < len(letter_list):
        pass


######### RECEIVER ##########
def receiver(self_port, peer_port, window_size, timeout_type, timeout_value):
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

    #alive receiver
    hi = "alive"
    sock.sendto(hi.encode(), saddr)

    #receiving window
    while True:
        pass




######### SENDING #########
def snd_r():
    pass

def snd_s():
    pass


######### RECEIVING #########
def recv_r():
    pass

def recv_s(sock):
    try:
        data = sock.recvfrom(1048)
        if data:
            buff, addr = data
            sequence_number = bts(buff[0:31])
            data = bts(buff[32:39])
            if sequence_number == 0:
                pass
    except socket.error:
        pass

    


########## BINARY/SYMBOL FUNCTIONS ##########
def bts(bin):
    return int(bin, 2)

def stb(st, isData):
    st = ord(st)
    if isData:
        binary = bin(st)[2:].zfill(8)
    else:
        binary = bin(st)[2:].zfill(32)
    return binary


######### PACKET CREATION & EXTRACTION FUNCTIONS ##########
def make(seq, data):
    d = stb(data, True)
    s = stb(seq, False)
    ret = []
    ret.append(s)
    ret.append(d)
    return ret