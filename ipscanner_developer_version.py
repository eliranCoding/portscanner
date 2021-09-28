#! /usr/bin/python3

import multiprocessing, netifaces

from scapy.all import *

def get_gateway():
    return netifaces.gateways()['default'][netifaces.AF_INET][0]

subdomain = get_gateway()[:len(get_gateway())-2]

def ping_ip(index_ip: int, queue):
    ip = subdomain + '.' + str(index_ip)

    resp, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=4, retry=2)
    
    if resp:
        queue.put(ip)

def main():
    processes = []

    queue = multiprocessing.Queue()

    for i in range(0, 256):
        process = multiprocessing.Process(target=ping_ip, args=(i, queue,))
        
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    
    ips = []

    while queue.empty() is False:
        ips.append(queue.get())
    
    print(ips)

if __name__ == '__main__':
    main()
