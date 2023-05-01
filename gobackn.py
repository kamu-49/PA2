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
    buffer_len = ws
    buffer = []
    det_num = 1
    canTime = False # if can set timeout clock
    cando = True #if we are in timeout mode

    total = 0
    dead = 0
    while True:
        hold, addr = sock.recvfrom(1024)
        h = hold.decode()
        if h == "alive":
            break

    msg = input("sender> ")
    message = []
    for i in msg:
        message.append(i)
    
    window_ind = 0
    msg_ind = 0
    while msg_ind < len(message):
        print("cando staatus: ", cando)
        timeout = 0.0
        buff_ind = 0
        diff = len(message) - msg_ind #how many more chars left in the message
        new_ws = min(buffer_len, diff)
        while len(buffer) < new_ws and cando is True:
            seq_index += 1
            if seq_index > max_seq:
                seq_index = 1
            m = make(seq_index, msg[msg_ind])
            buffer.append(m)
            msg_ind += 1
            sock.sendto(m.encode(), ra)
            print("packet%d %s sent "%(seq_index-1, msg[msg_ind-1]))
            if canTime:
                timeout = time.time()
        
        #the buffer is full. wait for a recv
        a, b = sock.recvfrom(1024)
        canTime = True
        seq = a.decode()
        seq_num = bto(seq, False)
        if (seq_num-1) < (window_ind % max_seq):
            print("ACK%d received. window does not move and stays at %d"%(seq_num-1, window_ind))
            canTime = True
            timeout = time.time()
        else:
            for i in range(len(buffer)):
                word = buffer[i]
                i_num = bto(word[0:32], False)
                if i_num <= seq_num:
                    throwaway = buffer.pop(i)
                    window_ind += 1
                    total += 1
                    if i_num == seq_num:
                        print("ACK%d received, window moves to %d"%(seq_num-1, window_ind))
                        canTime = True
                        break
        print("cantime stat: ", canTime)
        if canTime:
            timeout = time.time()
            print("quick test: ", time.time())
            canTime = False
        

        if time.time() - timeout > 0.5:
            print("nah we timing out boi")
            finished_timeout = time.time()
            cando = False
            timeout = 0.0
        
        if cando is False:
            if time.time() - finished_timeout >= 1:
                cando = True
                timeout = time.time()
                

    nah = b"finito"
    sock.sendto(nah, ra)
    print("[Summary] %d/%d packets discarded, loss rate = %f%%"%(dead, total, float((dead/total)*100)))
    

def receiver(rp, pp, ws, tt, tv):
    seq_index = 0

    ### sock init
    sa = ('localhost',pp)
    ra = ('localhost', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ra)
    buffer = [None] * 1

    hi = b"alive"
    sock.sendto(hi, sa)
    
    dead = 0
    total = 0
    exp_pkg = 1
    while True:
        a, b = sock.recvfrom(1024)
        total += 1
        if(a.decode() == "finito"):
            print("[Summary] %d/%d packets dropped, loss rate = %f%%"%(dead, total, float((dead/total)*100)))
            break
        else:
            decoded = a.decode()
            seq = decoded[0:32]
            packet = decoded[32:40]
            
            fs = bto(seq, False)
            fd = bto(packet, True)
            print("packet %d %s received"%(fs-1, fd))
            # ADD PROBABILITY HERE
            #dead += 1
            sock.sendto(seq.encode(), sa)
            print("ACK%d sent, expecting packet%d"%(fs-1,fs))


def bto(bi, isData): #bts
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
    return ret

def decoder(encoded, isACK):
    decoded = encoded.decode()
    seq = decoded[0:32]

    if isACK:
        fs = bto(seq, False)
        fd = 0
    else:
        packet = decoded[32:40]
        fs = bto(seq,False)
        fd = bto(packet, True)
    
    return fs, fd

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
        s.bind(('localhost',mp))
        sender(sp,pp,ws,pt,pn)
    except OSError as e:
        s.close()
        time.sleep(0.5)
        receiver(sp,pp,ws,pt,pn)