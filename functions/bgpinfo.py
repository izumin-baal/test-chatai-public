# -*- coding: utf-8 -*-
import os
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from dotenv import load_dotenv

BGP_ROUTER_HOST = os.getenv('BGP_ROUTER_HOST')
BGP_ROUTER_USER = os.getenv('BGP_ROUTER_USER')
BGP_ROUTER_PASS = os.getenv('BGP_ROUTER_PASS')

device = Device(host=BGP_ROUTER_HOST, user=BGP_ROUTER_USER, password=BGP_ROUTER_PASS, port="22")

def show_route(prefix=None):
    if prefix:
        command = f'cli -c "show route {prefix} | no-more"'
    else:
        return "[Error] Prefixが必要"
    
    ss = StartShell(device)
    ss.open()
    result = ss.run(command)
    print (result)
    ss.close()
    return result

def show_route_detail(prefix=None):
    if prefix:
        command = f'cli -c "show route {prefix} detail | no-more"'
    else:
        return "[Error] Prefixが必要"
    
    ss = StartShell(device)
    ss.open()
    result = ss.run(command)
    print (result)
    ss.close()
    return result

def show_route_as_regex(asn_regex=None):
    if asn_regex:
        command = f'cli -c "show route aspath-regex {asn_regex} | no-more"'
    else:
        return "[Error] ASN正規表現が必要"
    
    ss = StartShell(device)
    ss.open()
    result = ss.run(command)
    print (result)
    ss.close()
    return result

if __name__ == "__main__":
    show_version()