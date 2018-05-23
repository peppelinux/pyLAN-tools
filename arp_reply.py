#!/usr/bin/env python3
# Giuseppe De Marco

from scapy.all import *

def arp_reply(ipaddr_to_advertise,
              src_mac,
              dst_mac,
              count):
    eth = Ether(dst=dst_mac)
    arp = ARP(psrc=ipaddr_to_advertise, 
              hwsrc=src_mac, 
              #pdst=ipaddr_to_advertise, 
              hwdst=dst_mac, op=2)
    for i in range(count):
        sendp(eth/arp)


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, 
                        help="network interface to use")
    parser.add_argument('-s', required=False, 
                        help="source mac address")
    parser.add_argument('-d', required=False, 
                        default='ff:ff:ff:ff:ff:ff',
                        help=("destination, target mac address"
                              " default is: ff:ff:ff:ff:ff:ff"))
    parser.add_argument('-ip', required=False,
                        help="ip to announce")
    parser.add_argument('-count', required=False, type=int,
                        default=10,
                        help="how many times")
    args = parser.parse_args()
    conf.iface = args.i
    
    if not args.s:
        args.s = get_if_hwaddr(conf.iface)
    if not args.ip:
        args.ip = get_if_addr(conf.iface)
    arp_reply(args.ip, args.s, args.d, args.count)
