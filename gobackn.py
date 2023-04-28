from socket import *
import sys
import time
import signal
import random

##### DECLARATIONS #####
byte = 8
letter = [byte]
sequence_number = [32]
data_packet = [letter + len(sequence_number)]
data_packet_size = len(data_packet)
timeout = 0.5
holder = 0


##### SENDER #####
def sender(self_port, peer_port, window_size, timeout_type, timeout_value):
    ### Declarations
    sp = self_port
    rp = peer_port
    ws = window_size
    tt = timeout_type
    tv = timeout_value
    seq_index = 0

    ### sock init
    sa = ('',sp)
    ra = ('', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(sa)
    buffer = [data_packet_size*ws]

    ## TEST 1 ##
    t, a = sock.recvfrom(1024)
    hold = t.decode()
    print(hold)

    tst1 = "hi. this is a socket connection test"
    sock.sendto(tst1.encode(), ra)
    ## TEST 1 END ##

##### RECEIVER #####
def receiver(self_port, peer_port, window_size, timeout_type, timeout_value):
    rp = self_port
    sp = peer_port
    ws = window_size
    tt = timeout_type
    tv = timeout_value
    seq_index = 0

    ### sock init
    sa = ('',sp)
    ra = ('', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ra)
    buffer = [data_packet_size*ws]

    ## TEST 1 ##
    tst1 = "hi. this si the receiver side"
    sock.sendto(tst1.encode(), sa)

    t, a = sock.recvfrom(1024)
    hold = t.decode()
    print(hold)
    ## TEST 1 END ##