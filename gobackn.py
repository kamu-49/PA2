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
    ws = window_size
    type = timeout_type
    val = timeout_value


######### RECEIVER ##########
def receiver(self_port, peer_port, window_size, timeout_type, timeout_value):
    rport = self_port
    sport = peer_port
    ws = window_size
    type = timeout_type
    val = timeout_value


######### SENDING #########
def snd_r():
    pass

def snd_s():
    pass


######### RECEIVING #########
def recv_r():
    pass

def recv_s():
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