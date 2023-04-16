# PA2: CSEE W4119 Computer Networks Programming Assignment 2 - Network Protocols Emulation

## PART1: GBN
### Notes
* sender/receiver in UDP protocol
* implementation of GBN on top of UDP on both sender and receiver
* >guarantee packets be sent in correct order to higher layers<
* unreliable channel emulation:
    * sender/receiver drops incoming packet/ACK w/ prob
* [python3 gobackn.py <self-port> <peer-port> <window-size> [-d <value-of-d> | -p <value-of-p>]]
* argv[0] = file name
* argv[1] = sender port
* argv[2] = receiver port
* argv[3] = window size
* argv[4] = d/p
* argv[5] = value
#### Protocol
* packet
    * each char = one packet (packet max len = 1 byte)
    * data packet = seq # (no format requirement) + data
    * ACK = seq #
* buffer
    * sender/receiver have sending buffer
    * data packets put in buffer before send
    * data packets removed from buffer when corresp. ACK received
    * sending buff should be long enough to avoid conflict of packet #s
    * full buffer -> wait until more space is available
* window
    * moves along sending buff
    * window should wrap if implemented as array
    * packets in window = sent out immediately
    * >window size = passed as argument<
* timer
    * starts after first packet sent out, stops when ACK received
    * timer restarts when window moves
    * timeout = 500ms
#### Emulation
* GBN nodes to send packets over UDP protocol
* receiver = deilberately discard data packets (probability)
* sender = deliberately discard ACKs before handling them (probability)
* probability = determinstic and probabilistic (passed as an arg)
#### Loss Rate Calculations (5pts/40pts)
* a summary at the end of transmission
* both sender and receiver print out ratioof packet failures/total packets received
* tests provided

## PART2: DISTANCE-VECTOR ROUTING ALG
###     Notes
####        Protocol

## PART3: COMBINATION
###     Notes
- Will be done later. Will see if have enough time


## helpful links that sometimes slow my computer down like crazy so I save them all:
* https://www.tutorialspoint.com/a-protocol-using-go-back-n#:~:text=Go%2DBack%2DN%20protocol%2C,receiving%20window%20size%20of%201.
* https://www.baeldung.com/cs/networking-go-back-n-protocol
* https://docs.oracle.com/cd/E19620-01/805-4041/6j3r8iu2e/index.html