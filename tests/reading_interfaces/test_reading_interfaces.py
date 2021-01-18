#!/usr/bin/python3
""" Testing with pytest: Reading interface addresses
Author: Peter Vago <peter.vago@gmail.com>, 2021"""

import os, sys
import logging
import pytest

path_this_file = os.path.abspath(__file__)  # ~/workdir/get-ips/tests/reading_interfaces/test_reading_interfaces.py
path_this_folder = os.path.dirname(path_this_file)  # ~/workdir/get-ips/tests/reading_interfaces/
project_base_path = path_this_folder + "/../../"  # ~/workdir/get-ips/
sys.path.append(project_base_path + "/src")  # ~/workdir/get-ips/src
import interface_parser  # custom module

def init_logging(loglevel=logging.DEBUG):
    # Enable logging
    import utils  # custom module
    logfile = "/tmp/get-ips.log"
    l = utils.mylogging(logfile, loglevel)
    global logger
    logger = l.getlogger_reference()

#@pytest.mark.skip(reason="...")
def test_reading_iface_data():
    """testing if 'ip addr show' parsing works properly"""
    ifpars = interface_parser.InterfaceParser(ip_version="4")
    #ifpars.get_list_of_all_interfaces(interface_parser.AddressFormats.dotted_decimal) # using curent system inteface settings

    # Based on testfile
    tesfiles_dir = project_base_path + "tests/reading_interfaces/examples/"  # ~/workdir/get-ips/tests/reading_interfaces/examples/

    # testfiles: list of tuples. tuples: (<filename>, expected_response)
    testfiles = [
        ("01_ip_addr.txt", ['127.0.0.1', '192.168.0.28']),
        ("02_ip_addr.txt", ['127.0.0.1', '192.168.0.23']),
        ("03_ip_addr.txt", ['127.0.0.1', '192.168.0.28', '192.168.165.143']),
        ("04_ip_addr_show_router.txt", ['127.0.0.1', '212.52.170.126', '212.52.170.115', '10.0.21.13', '10.0.11.4', '10.0.1.158'])
    ]

    # Iterate through on testfiles
    for t in testfiles:
        #testfile=project_base_path + "tests/reading_interfaces/examples/01_ip_addr.txt"
        testfile = tesfiles_dir + t[0]
        print("====== %s ======"%testfile)
        expected_response = t[1]
        ifpars.testfile = testfile # using a testfile
        ifaces_list = ifpars.get_list_of_all_interfaces(interface_parser.AddressFormats.dotted_decimal)
        logger.info(ifaces_list)
        print("Addresses found : %s"%str(ifaces_list))
        assert ifaces_list == expected_response

#@pytest.mark.skip(reason="...")
def test_reading_iface_data_with_netmask():
    """testing if 'ip addr show' parsing works properly. WITH MASK"""
    ifpars = interface_parser.InterfaceParser(ip_version="4")
    #ifpars.get_list_of_all_interfaces(interface_parser.AddressFormats.dotted_decimal) # using curent system inteface settings

    # Based on testfile
    tesfiles_dir = project_base_path + "tests/reading_interfaces/examples/" # ~/workdir/get-ips/tests/reading_interfaces/examples/

    # testfiles: list of tuples. tuples: (<filename>, expected_response)
    testfiles = [
        ("01_ip_addr.txt", ['127.0.0.1/8', '192.168.0.28/24']),
        ("02_ip_addr.txt", ['127.0.0.1/8', '192.168.0.23/24']),
        ("03_ip_addr.txt", ['127.0.0.1/8', '192.168.0.28/24', '192.168.165.143/21']),
        ("04_ip_addr_show_router.txt", ['127.0.0.1/8', '212.52.170.126/24', '212.52.170.115/24', '10.0.21.13/30', '10.0.11.4/24', '10.0.1.158/24'])
    ]

    # Iterate through on testfiles
    for t in testfiles:
        #testfile=project_base_path + "tests/reading_interfaces/examples/01_ip_addr.txt"
        testfile = tesfiles_dir + t[0]
        print("====== %s ======"%testfile)
        expected_response = t[1]
        ifpars.testfile = testfile  # using a testfile
        ifaces_list = ifpars.get_list_of_all_interfaces(interface_parser.AddressFormats.dotted_decimal_with_netmask)
        logger.info(ifaces_list)
        print("Addresses found : %s"%str(ifaces_list))
        assert ifaces_list == expected_response

@pytest.mark.skip(reason="IPv6 version is not implemented")
def test_reading_iface_data_ipv6():
    """testing if 'ip addr show' parsing works properly. IPv6"""
    # ToDo: Not implemented. REQ DOC -> "+Task"
    # Based on testfile
    tesfiles_dir = project_base_path + "tests/reading_interfaces/examples/" # ~/workdir/get-ips/tests/reading_interfaces/examples/
    testfile = tesfiles_dir + "/01_ip_addr.txt"

    ifpars = interface_parser.InterfaceParser(ip_version="6")
    ifpars.testfile = testfile  # using a testfile
    ifaces_list = ifpars.get_list_of_all_interfaces(interface_parser.AddressFormats.ipv6_zero_supression)

    pass


if __name__ == "__main__":
    "When this test script is not called by pytest..but called as standalone script...run the following:"
    #Logging
    init_logging(logging.INFO)

    # Execture test explicitly
    test_reading_iface_data()
    test_reading_iface_data_with_netmask()
    #test_reading_iface_data_ipv6()

else:
    init_logging(logging.ERROR)
