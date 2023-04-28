from socket import *
from sys import *
import time
import signal
import random

##### DECLARATIONS #####
byte = 8
letter = [byte]
sequence_number = [32]
data_packet = [len(letter) + len(sequence_number)]
data_packet_size = len(data_packet)
timeout = 0.5
holder = 0


##### SENDER #####
def sender(self_port, peer_port, window_size, timeout_type, timeout_value):
    isOn = False
    print("hello. inside sender")
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
    print(sa)
    buffer = [data_packet_size*ws]

    ## TEST 1 ##
    #sock.setblocking(False)
    print("gonna start waiting...")
    t, a = sock.recvfrom(4096)
    print(t)
    hold = t.decode()
    print(hold)

    """
    tst1 = "hi. this is a socket connection test"
    sock.sendto(tst1.encode(), ra)
    ## TEST 1 END ##
    """
    print("hi. leaving send")

##### RECEIVER #####
def receiver(self_port, peer_port, window_size, timeout_type, timeout_value):
    print("hello. in receiver")
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

    t, a = sock.recvfrom(4096)
    hold = t.decode()
    print(hold)
    ## TEST 1 END ##

def connection_test(pp):
    pa = ('', pp)
    isSender = False

    s = socket()
    try:
        s.connect(pa)
    except Exception:
        isSender = True
    finally:
        s.close()
    
    return isSender

if __name__ == "__main__":
    sp = int(argv[1])
    pp = int(argv[2])
    ws = int(argv[3])
    pt = argv[4]
    pn = float(argv[5])

    mp = int((sp + pp)/ 2)
    while mp == sp or mp == pp:
        mp = random.randint(80,65000)

    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.bind(('',mp))
    except:
        print("already exists?")

    print("fuck this")
    time.sleep(1)

    w1 = "this is the try for connecting to self port"
    print(w1)
    print("personal port: %d. other port: %d"%(sp, pp))
    aaa = ('', pp)
    print(aaa)
    s.sendto(w1.encode(), ('', pp))

    """
    try:
        w1 = "this is the try for connecting to self port"
        print(w1)
        print("personal port: %d. other port: %d"%(sp, pp))
        aaa = ('', pp)
        print(aaa)
        s.sendto(w1.encode(), ('', pp))
        print("about to trigger receiver")
        receiver(sp, pp, ws, pt, pn)
        s.close()
        print("closing socket from receiver side")
    except:
        print("about to trigger sender")
        sender(sp, pp, ws, pt, pn)
        s.close()
        print("closing socked tfomr sender side") """