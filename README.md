# pyLAN-tools

Python Scapy tools developed for LAN tests and advanced reconnaissance.

## Requirements

````
pip2 install scapy
````

## arpscan
This tools is a personal revision about netdiscover and arp-scan feature sets.


#### arpscan usage 
````
python2 arpscan.py --help

usage: arpscan.py [-h] -i I [-r R [R ...]] [-t T]
                  [-exclude EXCLUDE [EXCLUDE ...]] [-only ONLY [ONLY ...]]
                  [-shuffle] [-debug]

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

  -debug                interface to start listen to
````

#### arpscan examples
````
# scans only selected peers on the localnetwork configured on eth2 interface
python2 arpscan.py -i eth2 -t 0.01 -only 1 2 3 4 5 6 7 8 9 10 50 150 200 250 251 252 253 254
10.21.0.75 bc:5f:f4:f4:d0:d9 (eth2)
10.21.0.254 d4:ca:6d:e6:6a:d7


# scans only selected networks
python2 arpscan.py -i eth2 -t 0.01 -r 192.168.0.0/24 192.168.1.0/24
192.168.1.1 08:00:27:7c:f9:41
````
#### arpscan todo

- -only option improvements for CIDR lower than /24 (performance improvements)
- parallelization with subprocess per every -r lans (performance improvements)
- vendor database intergration (as netdiscover and arp-scan does)

## Arp-listener
Arp-listener is an old proof-of-concept of a ARP event listener with the ability to sniff
ARP requests and run callback based on filtered event. It was written in few hours
and will be continued in the future.

It hopefully wants to implement a pro-active defense when ARP poisoning 
activities are detected.

## gateway-finder-ng
This is a rework of the famous: https://github.com/pentestmonkey/gateway-finder

I just want to clean the code and integrate a native arp scanner to avoid the use of thirdy-party app as arp-scan.
This and some other general improvements.
