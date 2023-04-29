from socket import *
from sys import *
import time
import signal
import random

##### DECLARATIONS #####
byte = 8
letter = [byte]
sequence_number = [32]
data_packet = []
data_packet_size = len(data_packet)+len(sequence_number)
timeout = 0.5
holder = 0
max_seq = 2**32


##### SENDER #####
def sender(sp, pp, ws, tt, tv):
    ### Declarations
    seq_index = 0

    ### sock init
    sa = ('localhost',sp)
    ra = ('localhost', pp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(sa)
    buffer = [None] * ws

    while True:
        hold, addr = sock.recvfrom(1024)
        print(hold)
        h = hold.decode()
        print(h)
        break
  
    msg = input("sender> ")
    mmsg = "the message received was: " + msg
    sock.sendto(mmsg.encode(), ra)
    test3 = []
    for i in msg:
        test3.append(i)
    t3h = 0
    while t3h < len(test3):
        while None in buffer:
            seq_index += 1
            if seq_index > max_seq:
                seq_index = 1
            m = make(seq_index, msg[i])
            print(m)
            sock.sendto(m.encode(), ra)
            time.sleep(0.15)
    nah = b"finito"
    sock.sendto(nah, ra)
    ## test 4 done ##
    print("shutting down sender...")
    time.sleep(3)

def receiver(rp, pp, ws, tt, tv):
    print("hello. in receiver")
    seq_index = 0

    ### sock init
    sa = ('localhost',pp)
    ra = ('localhost', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ra)
    buffer = [None] * 1

    ## test 1 ##
    print("sending to: ", sa)
    print("Test1")
    hi = b"hi. receiver to sender"
    sock.sendto(hi, sa)
    ## test 1 done ##

     ## test 2 ##
    while True:
        s, a = sock.recvfrom(1024)
        print(s)
        print(s.decode())
        break
    ## test 2 done ##
    while True:
        a, b = sock.recvfrom(1024)
        if(a.decode() == "finished"):
            print("we done here chief")
            break
        else:
            print("Received: ", a.decode())
    ## test 3 done ##

    ## test 4 ##
    while True:
        a, b = sock.recvfrom(1024)
        if(a.decode() == "finito"):
            print("done again chief")
            break
        else:
            print("received pkg: ", a.decode())
            seq = a[0:32]
            d_hold = a[32:40]
            print("RARARAAAAA : ", d_hold)
            data = d_hold
            fs = bto(seq, False)
            fd = bto(data, True)
            print("converted to: ", fs)
            print("as well as ", fd)
    ## test 4 done ##
    print("shutting down receiver...")
    time.sleep(3)

def bto(bi, isData): #bts
    print("this is so frustrating: ", type(bi), bi)
    if not isData:
        returner = int(bi, 2)
    elif isData:
        inp_str = int(bi, 2)
        inp_char = inp_str.to_bytes(1, "big")
        returner = inp_char.decode()
    return returner

def otb(st, isData): #stb
    #st = ord(st)
    if not isData:
        binary = bin(st)[2:].zfill(32)
    elif isData:
        ia = st.encode()
        ba = int.from_bytes(ia, "big")
        binary = bin(ba)[2:].zfill(8)
    return binary

def make(seq, data):
    d = otb(data, True)
    s = otb(seq, False)
    ret = ""
    ret= s + d
    print(s, d, "make ", ret)
    return ret

if __name__ == "__main__":
    sp = int(argv[1])
    pp = int(argv[2])
    ws = int(argv[3])
    pt = argv[4]
    pn = float(argv[5])

    mp = int((sp + pp)/ 2)
    s = socket(AF_INET, SOCK_DGRAM)
    time.sleep(0.5)
    try:
        print("attempting bind...")
        s.bind(('localhost',mp))
        print("no sender yet")
        sender(sp,pp,ws,pt,pn)
    except OSError as e:
        print("sender already alive")
        s.close()
        time.sleep(5)
        receiver(sp,pp,ws,pt,pn)