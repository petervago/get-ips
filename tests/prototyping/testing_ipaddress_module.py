#!/usr/bin/python3
"""Author: Peter Vago, 2021
Dependencies: ipaddress Python package
"""

from ipaddress import IPv4Interface
import ipaddress

import itertools # builtin, Py >=3.5

def get_combinations(list):
    """Get Combinations of list elements.
     Example: ([1,2,3] -> 1-2, 1-3, 2-3)

    Args:
        list: list of items, items can be any data type

    Returns:
        combination, object, tuple of pairs
    """

    # print(list)

    # Example: (list:[1,2,3] -> combinations: [(1,2), (1,3), (2,3)])
    combinations=itertools.combinations(list,2) # https://docs.python.org/3/library/itertools.html#module-itertools
    # for pair in combinations:
    #     print(pair)
    return combinations



def check_overlaps(if_list):
    """Using ipaddress module: network.overlaps(other_network) return True if they overlap
    BUT: "Multiple IPs in the same subnet are still fine" !!!

    Args:
        if_list:

    Returns:
        overlaps: list of overlapping interface names. names are elements of if_list
    """

    # # overlaps method is "symmetric" -> Enough to test combination excluding duplicates ([1,2,3] -> 1-2, 1-3, 2-3)
    #combinations = get_combinations([1,2,3,4]) # Testing
    combinations = get_combinations(if_list)  # Testing

    overlaps = list()
    # Test each pairs for overlapping
    for pair in combinations:
        try:
            addr_a = pair[0] # string
            addr_b = pair[1]
            if_a = IPv4Interface(addr_a) # object
            if_b = IPv4Interface(addr_b)
            net_a = if_a.network # "network"
            net_b = if_b.network
        except:
            raise ValueError("(10001) unexpected inteface-pair: %s"%str(pair))
        #print(pair, if_a, if_b)

        if net_a.overlaps(net_b): # True if if_a and if_b overlap
            # If networks overlap, but IPs are in the same network , that is fine. Otherwise add ifaces to overlaps list.
            if (if_a.network == if_b.network):
                pass # Do not append 'overlaps' list, because it's 'still fine'
            else:
                overlaps.append(addr_a)
                overlaps.append(addr_b)
        else:
            pass


    return overlaps

def print_basic_iface_data(if_list):
    for iface in if_list:
        interface = IPv4Interface(iface)
        print("=== iface: %s ==="%iface)
        print(interface.ip)
        print(interface.with_netmask)
        print(interface.network)
        print(interface.version)
        #print(interface.network.overlaps())

def main(if_list):
    """Main function"""
    print(if_list)

    #1. Print basic data of interfaces
    #print_basic_iface_data(if_list)

    # 2. Check for overlappig network on intefaces
    overlaps = check_overlaps(if_list)
    print(overlaps)

if __name__ == "__main__":
    list_of_interfaces_with_prefix = [
        "4.5.0.3/16",
        "4.5.2.1/24",
        "10.50.60.70/16",
        "10.50.60.71/16",
        "127.0.0.1/8"
    ]
    main(list_of_interfaces_with_prefix)
