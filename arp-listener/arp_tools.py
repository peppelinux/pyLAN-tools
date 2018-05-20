from __future__ import print_function
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


ARP_REQUEST_THRESHOLD=1
ARP_RESPONSE_THRESHOLD=3

HELP="""
pip3 install scapy-python3
"""

class ArpFaker(object):
    @staticmethod
    def arp_request_trigger(pkt):
        msg = 'Request [who-has]: {} ({}) is asking ({}) about {} '.format(
                                                                pkt[ARP].psrc, 
                                                                pkt[ARP].hwsrc,
                                                                pkt[ARP].hwdst,
                                                                pkt[ARP].pdst,
                                                                )
        print(msg)
    
    @staticmethod  
    def arp_response_trigger(pkt):
        msg = '*Response [is-at]: {} ({}) has address {} ({})'.format(
                                                               pkt[ARP].pdst,
                                                               pkt[ARP].hwsrc, 
                                                               pkt[ARP].psrc,
                                                               pkt[ARP].hwdst,
                                                               )
        print(msg)
        
    
    @classmethod
    def arp_filter(cls, pkt):
        if not pkt[ARP]: return False
        #~ print(pkt[ARP].__dict__)
        #~ for x,y in pkt[ARP].fields.items():
            #~ print(x, y)
        if pkt[ARP].op == 1:  # who-has (request)
            cls.arp_request_trigger(pkt)        
        elif pkt[ARP].op == 2:  # is-at (response)
            cls.arp_response_trigger(pkt)
        
    
    @classmethod
    def arp_listen(cls, stype):
        if stype == 'request':
            req = sniff(prn=cls.arp_filter, filter='arp', store=0, count=ARP_REQUEST_THRESHOLD)
        elif stype == 'response':
            res = sniff(prn=cls.arp_filter, filter='arp', store=0, count=ARP_RESPONSE_THRESHOLD)

    @staticmethod
    def arp_reply(pkt):
        packet = Ether()/ARP(op="who-has",hwsrc=my_mac,psrc=sys.argv[2],pdst=sys.argv[1])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    
    # By default it will fail with multiple arguments.
    parser.add_argument('--default')
    
    # This is the correct way to handle accepting multiple arguments.
    # '+' == 1 or more.
    # '*' == 0 or more.
    # '?' == 0 or 1.
    # An int is an explicit number of arguments to accept.
    parser.add_argument('-ip', nargs='+')
    parser.add_argument('-req', action="store_true", help="listen only for requests")
    parser.add_argument('-res', action="store_true", help="listen for requests and responses")
    #~ parser.add_argument('-h', action="store_true", required=0)    
    args = parser.parse_args()
    
    #~ if args.h:
        #~ print(HELP)
    
    if args.ip:
        print(args.ip)
    
    
    if args.req:
        while 1:
            #~ try: 
            res = ArpFaker.arp_listen('request')
            #~ except Exception as e: print(e)
    elif args.res:
        while 1:
            #~ try: 
            res = ArpFaker.arp_listen('response')
            #~ except Exception as e: print(e)
        
        
