# pyLAN-tools

Python Scapy tools developed for LAN tests and advanced reconnaissance.

## Requirements

````
pip3 install scapy
pip3 install netaddr
````

## ARP Scanning
Arpscan.py is a personal revision about netdiscover and arp-scan feature sets.
 
````
sudo python2 arpscan.py --help

usage: arpscan.py [-h] -i I [-r R [R ...]] [-t T]
                  [-exclude EXCLUDE [EXCLUDE ...]] [-only ONLY [ONLY ...]]
                  [-debug]

optional arguments:
  -h, --help            show this help message and exit
  -i I                  local network interface
  -r R [R ...]          networks to test separated by space, example:
                        192.168.0.0/16, 172.16.0.0/12, 10.0.0.0/8
  -t T                  timeout between a request and another
  -exclude EXCLUDE [EXCLUDE ...]
                        exclude these peers, example: 0 255 1. default: 0 and
                        255
  -only ONLY [ONLY ...]
                        test only these peers. Example: 1 2 3 4 5 6 7 8 9 10
                        50 150 200 250 251 252 253 254

  -debug                prints things to stdout
````

#### arpscan usage examples
````
# scans only selected peers in the local network configured on eth2 interface
python2 arpscan.py -i eth2 -t 0.01 -only 1 2 3 4 5 6 7 8 9 10 50 150 200 250 251 252 253 254
10.21.0.75 bc:5f:f4:f4:d0:d9 (eth2)
10.21.0.254 d4:ca:6d:e6:6a:d7

# scans only selected networks
python2 arpscan.py -i eth2 -t 0.01 -r 192.168.0.0/24 192.168.1.0/24
192.168.1.1 08:00:27:7c:f9:41
````
#### arpscan todo

- -only option improvements for CIDR lower than /24 (performance improvements)
- parallelization with subprocess per every -r lan (performance improvements)
- choose a number of worker to delegate a subset of addresses (address_pool/num_workers)
- vendor database intergration and representation (as netdiscover and arp-scan does)

## Gratuitous ARP response
Create an unsolicited ARP RESPONSE to a target.
This technic can be used to ARP poison the neighbour's caches or
send unsolicitated ARP response to mitigate ARP poison attacks.
This means that the same thing that is used to attack would be the only
solution to defense from it.

Another solution would be we having a static ARP definition in our systems... But, really, who have this?

[addrwatch](https://github.com/fln/addrwatch) is a good monitoring system for this kind of attacks.

````
# gratuitous arp reply regarding you
python3 arp_reply.py -i wlp2s0

# gratuitous arp reply to defend your gateway :)
arp_reply.py -i wlp2s0 -s 10:fe:ed:78:34:ae -ip 10.87.7.1

# arp poison to broadcast, target is ff:ff:ff:ff:ff:ff
python3 arp_reply.py -i wlp2s0 -s 00:45:a2:ef:ff:ea -ip 192.168.7.2

# arp poison attack to a specific target (10:fe:ed:78:34:ae)
python3 arp_reply.py -i wlp2s0 -s 00:45:a2:ef:ff:ea -ip 192.168.7.2 -d 10:fe:ed:78:34:ae
````
While running gratuitous ARP responses, even if you are running an
attack or a defense, you can always test if an ARP cache is poisoned, testing
it with arping or locally with arp -an.

````
# this is what your want to be pushed to neighbors arp cache
while [ 1 ]; do python3 arp_reply.py -i wlp2s0 -s 00:45:a2:ef:ff:ea -ip 192.168.7.2; done

# this what you can do for test the efficiency of the previous command

root@yogurt:/home/wert/DEV/pyLAN-tools# arping -I wlp2s0 192.168.7.2
ARPING 192.168.7.2
42 bytes from 00:45:a2:ef:ff:ea (192.168.7.2): index=0 time=770.032 msec
42 bytes from 00:45:a2:ef:ff:ea (192.168.7.2): index=1 time=802.075 msec
42 bytes from 00:45:a2:ef:ff:ea (192.168.7.2): index=2 time=833.749 msec
````

### TODO
- create different workers to parallelize arp sending
- scan neighbours and use their MAC address to randomly craft ARP response with them

## Arp-listener
Arp-listener is an old proof-of-concept of an ARP event listener. It would sniff
ARP requests and run callback based on filtered event. It was written in few hours during a summer night
and will be continued in the future... This should sound a bit more romantic.

It hopefully wants to implement a pro-active defense when ARP poisoning 
activities are detected.

## gateway-finder-ng
This is a rework of the famous: https://github.com/pentestmonkey/gateway-finder

I just want to clean the code and integrate a native arp scanner to avoid the use of thirdy-party app as arp-scan.
This and some other general improvements. 
