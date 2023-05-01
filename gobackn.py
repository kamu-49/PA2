from socket import *
from sys import *
import time
import signal
import random

##### DECLARATIONS #####
byte = 9
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
    ddrop = 0

    start_timeout = True # if can set timeout clock
    in_timeout = False #if we are in timeout mode
    timeout = time.time()
    max_timeout = time.time()

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
    #sock.settimeout(0.1)
    while msg_ind < len(message): #while still message left
        anyInput = True
        isDisc_p = False
        isDisc_d = False
        
        diff = len(message) - msg_ind #how many more chars left in the message
        new_ws = min(buffer_len, diff)

        while (len(buffer) < new_ws) and (in_timeout is False):
            seq_index += 1
            if seq_index > max_seq:
                seq_index = 1
            m = make(seq_index, msg[msg_ind])
            buffer.append(m)
            msg_ind += 1
            sock.sendto(m.encode(), ra)
            print("[",time.time(),"] packet%d %s sent "%(seq_index-1, msg[msg_ind-1]))
            if start_timeout:
                timeout = time.time()
                start_timeout = False
        #while loop will not run if the buffer is full
        

        if in_timeout:
            remaining_timeout_time = 0.5-(time.time()-max_timeout)
            if remaining_timeout_time > 0:
                sock.settimeout(remaining_timeout_time)
                try:
                    a, b = sock.recvfrom(1024)
                    start_timeout = True
                except:
                    time.sleep(remaining_timeout_time)

                    in_timeout = False
                    for header in buffer:
                        sock.sendto(header.encode(), ra)
                        seq = header[0:32]
                        packet = header[32:40]
                        fs = bto(seq, False)
                        fd = bto(packet, True)
                        if start_timeout:
                            timeout = time.time()
                            start_timeout = False
                    continue
            elif remaining_timeout_time <= 0:
                try:
                    a, b = sock.recvfrom(1024)
                    start_timeout = True
                except:
                    in_timeout = False
                    for header in buffer:
                        sock.sendto(header.encode(), ra)
                        seq = header[0:32]
                        packet = header[32:40]
                        fs = bto(seq, False)
                        fd = bto(packet, True)
                        print("[",time.time(),"] packet%d %s sent "%(fs-1, fd))
                        if start_timeout:
                            timeout = time.time()
                            start_timeout = False
                    continue
        elif not start_timeout:
            remaining_timeout_time = 0.5-(time.time()-timeout)
            if remaining_timeout_time > 0:
                sock.settimeout(remaining_timeout_time)
                try:
                    a, b = sock.recvfrom(1024)
                    start_timeout = True
                except:
                    start_timeout = False
                    in_timeout = True
                    anyInput = False
                    continue
            elif remaining_timeout_time <= 0:
                start_timeout = False
                in_timeout = True
                anyInput = False
                continue
    
        seq = a.decode()
        seq_num = bto(seq, False)
        ddrop += 1
        p_prob = float(random.randint(0,100)/100)
        cont = True

        if ddrop >= tv and tt == "-d":
            isDisc_d = True
            ddrop = 0
        if p_prob <= tv and tt == "-p":
            isDisc_p = True
    
        if isDisc_p or isDisc_d:
            print("[",time.time(),"] ACK%d discarded"%(seq_num-1))
            dead += 1
            start_timeout = False
            isDisc_p = False
            isDisc_d = False
        else:
            if anyInput:
                if (seq_num-1) < (window_ind % max_seq):
                    print("[",time.time(),"] ACK%d received. window does not move and stays at %d"%(seq_num-1, window_ind))
                    start_timeout = True
                    timeout = time.time()
                else:
                    for i in range(len(buffer)):
                        word = buffer[i]
                        i_num = bto(word[0:32], False)
                        if i_num <= seq_num:
                            window_ind += 1
                            total += 1
                            if i_num == seq_num:
                                print("[",time.time(),"] ACK%d received, window moves to %d"%(seq_num-1, window_ind))
                                start_timeout = True
                                break
                    for j,k in reversed(list(enumerate(buffer))):
                            k_num = bto(k[0:32], False)
                            if k_num <= i_num:
                                throwaway = buffer.pop(j)

        if start_timeout and not in_timeout:
            timeout = time.time()
            start_timeout = False

        if not start_timeout:
            if time.time() - timeout > 0.5:
                max_timeout = time.time()
                in_timeout = True
                timeout = time.time()

    nah = b"finito"
    sock.sendto(nah, ra)
    print("[",time.time(),"] [Summary] %d/%d packets discarded, loss rate = %f%%"%(dead, total, float((dead/total)*100)))
    

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
    ddrop = 0
    exp_pkg = 1
    while True:
        isDisc_p = False
        isDisc_d = False
        a, b = sock.recvfrom(1024)
        ddrop += 1
        disc_seq = None

        p_prob = float(random.randint(0,100)/100)
        if ddrop >= tv and tt == "-d":
            isDisc_d = True
            ddrop = 0
        if p_prob <= tv and tt == "-p":
            isDisc_p = True

        if(a.decode() == "finito"):
            print("[",time.time(),"] [Summary] %d/%d packets dropped, loss rate = %f%%"%(dead, total, float((dead/total)*100)))
            break
        else:
            decoded = a.decode()
            seq = decoded[0:32]
            packet = decoded[32:40]
            
            fs = bto(seq, False)
            fd = bto(packet, True)

            if disc_seq == None:
                if isDisc_p or isDisc_d:
                    print("[",time.time(),"] packet %d %s discarded"%(fs-1, fd))
                    disc_seq = fs
                    dead += 1
                else:
                    print("[",time.time(),"] packet %d %s received"%(fs-1, fd))

                    sock.sendto(seq.encode(), sa)
                    print("[",time.time(),"] ACK%d sent, expecting packet%d"%(fs-1,fs))
                    total += 1
            else:
                if fs == disc_seq:
                    sock.sendto(seq.encode(), sa)
                    print("[",time.time(),"] ACK%d sent, expecting packet%d"%(fs-1,fs))
                    disc_seq = None
                    total += 1



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