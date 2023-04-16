from socket import * #for socket programming
import threading #for multithreading for multiple clients
import sys #for exit calls and input calls
import time #for sleep
import signal #for silent quit

"""
python3 gobackn.py <self-port> <peer-port> <window-size> [-d <d-value> | -p <p-value>]
"""

PAK_LEN = [16] #in bits, first half is seq #, second half is data packet
#buffer length will be packetsize * windowsize = 16*n (in bits)
TM_LMT = 0.5

def sender(sport, rport, ws, type, val):
    #create sock
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('', sport))

    #creation and validation of buffer 
    buff = (len(PAK_LEN)*ws)
    msg, addr = sock.recvfrom()
    msg = msg.decode()
    if int(msg) != int(buff):
        bad = "no"
        sock.sendto(bad.encode(), ())
        time.sleep(1)
        sys.exit("receiver and sender window size are not the same (assuming need them to be the same size).")

    send = input("node> ")
    ss = send.splitlines()
    #end of step 2


def receiver(rport, sport, ws, type, val):
    #create sock
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', rport))

    #creation and validation of buffer
    buff = (len(PAK_LEN)*ws)


def bts(dec): #binary to symbol
    pass

def stb(letter): #symbol to binary
    pass