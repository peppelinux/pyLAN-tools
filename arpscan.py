#/usr/bin/env python3

# suppress "WARNING: No route found for IPv6 destination :: (no default route?)"
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
# forked from DHCPig - thank you folks!
def get_if_net(iff):
    for net, msk, gw, iface, addr, metric in read_routes():
        if (iff == iface and net != 0):
            return ltoa(net)
    raise ("No net address found for iface %s\n" % iff)

def get_if_msk(iff):
    for net, msk, gw, iface, addr, metric in read_routes():
        if (iff == iface and net != 0):
            return ltoa(msk)
    raise  ("No net address found for iface %s\n" % iff)


def get_if_ip(iff):
    for net, msk, gw, iface, addr, metric in read_routes():
        if (iff == iface and net != 0):
            return addr
    raise ("No net address found for iface %s\n" % iff)

def calcCIDR(mask):
    mask = mask.split('.')
    bits = []
    for c in mask:
        bits.append(bin(int(c)))
    bits = ''.join(bits)
    cidr = 0
    for c in bits:
        if c == '1': cidr += 1
    return str(cidr)
# end fork from folks

def arpscan(debug=False, 
            networks=['192.168.0.0/16',
                      '172.16.0.0/12',
                      '10.0.0.0/8'], 
            excluded=[0, 255],
            only = [1,2,3,4,5,10,50,100,150,200,250,251,252,253,254], 
            timeout=0.05):
    """
    search for LAN neighbors 
    """
    nodes = {}
    addresses = []
    
    # scan only your iface network
    if not networks:
        myip  = get_if_ip(conf.iface)
        mymac = get_if_hwaddr(conf.iface)
        if debug: print("arpscan:  net = %s  : msk = %s  : CIDR = %s" % (get_if_net(conf.iface),get_if_msk(conf.iface),calcCIDR(get_if_msk(conf.iface))))
        pool = Net(myip + "/" + calcCIDR(get_if_msk(conf.iface)))
        if myip in pool:
            nodes[myip] =  mymac
            print(' '.join((myip, mymac, '(%s)' % conf.iface)))
            excluded.append(myip)
        
        if only:
            for peer in only:
               prefix = str(myip).split('.')[0:-1]  
               addresses.append('.'.join(prefix)+'.'+peer)
        else:
            for ip in pool:
                #~ print(ip)
                peer = str(ip).split('.')[-1] 
                if peer not in excluded:
                    addresses.append(ip)
    # scan selected networks
    else:
        for n in networks:
            net, mask = n.split('/')
            if debug: print("arpscan:  net = %s  : CIDR = /%s" % (net, mask))
            pool = Net(n)

            if only:
                prefix = str(pool.choice()).split('.')[0:-1]
                for peer in only:
                   addresses.append('.'.join(prefix)+'.'+peer)
            else:
                for ip in pool:
                    if ip not in excluded:
                        addresses.append(ip)
    
    
    
    for ip in addresses:
        if debug: print('Who-as %s' % ip)
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
        ans, unans = srp(arp_request, timeout=timeout, iface=conf.iface, verbose=debug)
        if ans:
            first_response = ans[0]
            req, res = first_response
            result = res.getlayer(Ether).src
            print(' '.join((ip, result)))
            nodes[ip] = result
        # time.sleep(timeout)
    return nodes


if __name__=="__main__":
    
    # hints: get_if_list() returns all the network interfaces
    #        my_macs = [get_if_hwaddr(i) for i in get_if_list()]
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, 
                        help="local network interface")
    parser.add_argument('-r', required=False, 
                        nargs='+', 
                        # default=[
                                 # '192.168.0.0/16', 
                                 # '172.16.0.0/12',
                                 # '10.0.0.0/8'],
                        help=("networks to test separated by space, "
                              # "defaults are listed in RFC 1918 - "
                              # "Address Allocation for Private Internets \n"
                              "example: "
                              "192.168.0.0/16, \n"
                              "172.16.0.0/12, \n"
                              "10.0.0.0/8 \n"))
    parser.add_argument('-t', required=False, type=float, default=0.05,
                        help="timeout between a request and another")
    parser.add_argument('-exclude', required=False, nargs='+', default=['0', '255'],
                        help="exclude these peers, example: 0 255 1. default: 0 and 255")
    parser.add_argument('-only', required=False, nargs='+', 
                        # default=['1','2','3','4','5','10','50','100','150','200','250','251','252','253','254'],
                        help=("test only these peers. "
                              "Example: 1 2 3 4 5 6 7 8 9 10 50 150 200 250 251 252 253 254"))
    # parser.add_argument('-shuffle', action='store_true', required=False,
                        # help="do not scan address pool in ascending order, shuffle it")
    parser.add_argument('-debug', required=False, action="store_true", 
                        help="interface to start listen to")
    args = parser.parse_args()
    conf.iface = args.i
    # run!
    arpscan(networks=args.r,
            debug=args.debug, 
            excluded=args.exclude, 
            timeout=args.t,
            only=args.only)
