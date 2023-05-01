### IMPORTS
from socket import *
import time
###IMPLEMENTATIONS
IP = 'localhost'
nplr = {}
kn = []
### MAIN ###
def main(input):
    np = [] #neighbor ports
    lr = [] #loss rates
    i = 0
    d = {}
    local_port = input[0]
    lpl = len(local_port)
    maxx = 1
    for i in range(1,len(input), 2):
        if maxx == 16:
            print("asked for too much. will only do the first 16 nodes")
            break
        else:
            if input[i] != "last":
                np.append(int(input[i]))
                kn.append(int(input[i]))
                lr.append(float(input[i+1]))
            maxx += 1
    lrnp_assign(np, lr)
    d = init_node(local_port)
    c = nplr

    sock = socket(AF_INET, SOCK_DGRAM)
    addr = (IP, local_port)
    sock.bind(addr)

    if input[-1] == "last":
        isLast = True
    
    final_table = steps(sock, local_port, lpl, d, c, isLast)
    print(final_table)

def lrnp_assign(np, lr):
    for i in range(len(np)):
        nplr[int(np[i])] = float(lr[i])
    nplr = sorted(nplr)


"""
INIT NODE
creates my table that I am trying to make
pretty much it keeps the D (or c. however I wanna view it) of the connecting nodes of the given node.
for example from textbook: initializing node z
zw: 0.5
zy: 0.2
"""
def init_node(local_port): #{wwww: 0.5, yyyy: 0.2} => {zzzzwwww:0.5, zzzzyyyy: 0.2} (but sorted)
    c = {}
    for i in nplr:
        r = []
        r.append(local_port)
        r.append(i)
        rr = ''.join(r)
        c[rr] = nplr[i]
    c = sorted(c)
    return c

def steps(sock, port, lpl, d, c, isLast):
    final_table = d
    if isLast:
        snd(sock, d, c)
        while True:
            timeout = time.time() + 3
            final_table = recv(sock, port, lpl, final_table, c)
            if time.time() > timeout:
                return final_table
    else:
        final_table = recv(sock, port, lpl, final_table, c)
        snd(sock, final_table, c)
        while True:
            timeout = time.time() + 3
            final_table = recv(sock, port, lpl, final_table, c)
            if time.time() > timeout:
                return final_table


"""
table will be a dictionary that contains the D route as the key and the length as the value.
for exa: initializing node z:
ze 0.5 0.2

next step with y for ex:
yz 0.2 
yw 0.1
yx 0.1
...
yz 0.2
yw 0.1
yx 0.1
(since there are no quicker routes, it will stay teh sae,)
"""
def recv(sock, port, port_len, table, init_table): #table is the d table, kn = known nodes
    a, b = sock.recvfrom(4096)
    dist = a.decode() #distance
    p = b[1] #port number
    split = dist.splitlines #[zzzzyyyy 0.2, zzzzeeee 0.5]
    dn = len(split) #2
    final_port_start = len(table)-port_len
    for pair in dn: #for loop that goes through each destination
        pl = pair.split() #pair  lsit, [zzzzyyyy, 0.2] / [zzzzeeee, 0.5]
        D = pl[0]
        ln = float(pl[1])
        split_ports = psf(port_len, D) #[zzzz, yyyy] / [zzzz, eeee]
        destination_port = split_ports[-1] #eeee since rnd 2
        if destination_port not in kn:
            ndp = int(str(port) + str(D))
            ndpl = float(ln + init_table[split_ports[0]])
            table[ndp] = ndpl
            kn.append(destination_port)
        else:
            for item in table:
                if item[final_port_start:len(table)] == destination_port:
                    #commence the algorithm
                    old_path = item
                    new_path = int(str(port) + str(old_path))
                    old_len = table(item)
                    new_len = ln
                    if new_len < old_len:
                        table[new_path] = new_len
                        del table[item]
                        break
    return table

def table_converter(table):
    small_str = ""
    big_str = ""
    for i in table:
        small_str = "%s %s\n"%(str(i), str(table[i]))
        big_str += small_str
    big_str = big_str[:-2]
    return big_str.encode()

def snd(sock, table, init_table): #table is returned from recv. or jus kept if you're the lat one
    timer = init_table
    timer = sorted(timer)
    encoded = table_converter(table)

    for i in timer:
        addr = (IP, i)
        finish = time.time() + timer[i]
        while True:
            if time.time() >= finish:
                sock.sendto(encoded, addr)



    
def psf(port_len, D): #port splitter function. just making this to make it easier on the eyes
    split_ports = []

    for i in range(0, len(D), port_len):
        part = int(D[i:i+port_len])
        split_ports.append(part)
    return split_ports

if __name__ == "__main__":
    main()