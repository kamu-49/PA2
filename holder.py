from socket import * #for socket programming
import threading #for multithreading for multiple clients
import sys #for exit calls and input calls
import time #for sleep
import signal #for silent quit
import random

"""
python3 gobackn.py <self-port> <peer-port> <window-size> [-d <d-value> | -p <p-value>]
"""

"""
DECLARATIONS
everything is in bits. stuff will be converted fro bytes to bits

1 byte = 8 bits.
buffer length = data packet * windowsize
data packet = data + seq number
seq number = 16 bits
"""
byte = 8
letter = [byte]
seq_num = [16]
data_packet = [letter+16] #in bits, first half is seq #, second half is data packet
dps = 24 #data packet size
#buffer length will be packetsize * windowsize = 16*n (in bits)
t_lim = 0.5
prob = 0.15
det = 5
holder = 0

"""
SENDER
"""
    
def sender(sport, rport, ws, type, val):
    #address creation
    saddr = ('localhost', sport)
    raddr = ('localhost', rport)

    #create sock
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(saddr)

    #creation and validation of buffer. old version
    """
    buff_len = (len(data_packet)*ws)
    msg, addr = sock.recvfrom()
    msg = msg.decode()
    print("addr test: ", addr, "\n", raddr) #test

    #if the buffers are not the
    if int(msg) != int(buff_len):
        bad = "no"
        sock.sendto(bad.encode(), raddr)
        time.sleep(1)
        sys.exit("receiver and sender window size are not the same (assuming need them to be the same size).")
    """

    #creation of buffer
    bs = len(data_packet)*ws #one-time usage
    buffer = [bs]

    #creating send window
    msg = input("sender> ")
    splitup = msg.split()
    newsplit = msg.split(' ',1)[1]
    listsplit = list(newsplit)
    if splitup[0] != "send":
        msg = input("incorrect input. Must do 'send' then message. \nsender> ")

    #opening messaging window
    for x in range(len(listsplit)):
        print(x)
"""
RECEIVER
"""

def receiver(rport, sport, ws, type, val):
    saddr = ('localhost', sport)
    raddr = ('localhost', rport)
    #create sock
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(raddr)

    #creation and validation of buffer. receive does not have a buffer
    """
    buff_size = (len(data_packet)*ws)
    sock.sendto(buff_size.encode(), saddr)
    msg, addr = sock.recvfrom(4096)
    print("addr test: ", addr, "\n", raddr)
    msg = msg.decode()
    if msg == "no":
        time.sleep(1)
        sys.exit("receiver and sender window size are not the same (assuming need them to be the same size).")
    """

    #sending creation of the receiver

     
    #opening messaging window
    while True:
        pass

"""
BIN TO SYMB
"""

def bts(dec): #binary to symbol
    pass

"""
SYMB TO BIN
"""

def stb(letter): #symbol to binary
    pass

"""
SEND
"""

def send(sock, encoded, ip, port, fail):
    addr = (ip, port)
    if fail == "-d":
        #send
        holder += 1
    elif fail == "-p":
        if random.random() <= prob:
            #send
            pass
    else:
        exit("error with the 'fail' thing") 

"""
RECEIVE
"""

def recv():
    pass