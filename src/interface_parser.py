"""Interface parser

Author: Peter Vago <peter.vago@gmail.com>, 2021
Dependencies: ipaddress Python package
"""

import subprocess, re
import logging
logger = logging.getLogger("app") # Get logger that was initialized in the main function, https://docs.python.org/2/library/logging.html

from enum import Enum
class ExtendedEnum(Enum): # These type of "util" classes usually go to a more global python file (e.g. my_project_global.py) -  Peter Vago
    """Class for Enums with smart methods"""
    @classmethod
    def listnames(cls):
        return list(map(lambda c: c.name, cls))
    @classmethod
    def listvalues(cls):
        return list(map(lambda c: c.value, cls))

class AddressFormats(ExtendedEnum):
    dotted_decimal = 0 # e.g. 127.0.0.0
    dotted_decimal_with_netmask = 1 # e.g. 127.0.0.1/8
    binary = 2 # e.g. 11011111 00111010 00000001 00001010
    ipv6_hex =3 # not used yet
    ipv6_zero_supression = 4 # not used yet

class IPVersion(ExtendedEnum):
    IPv4 = 4
    IPv6 = 6

class InterfaceParser(object):
    """Interface parser class.
    Reading and listing (printing) interface configurations"""
    ip_version=IPVersion.IPv4
    testfile = None

    def __init__(self, **kwargs):

        # If ip_version is specified....else it is set to '4'
        try:
            ip_version = kwargs.get("ip_version") # "4" or "6"
        except:
            ip_version="4"
        self._switch_to_ip_version_specific_class(ip_version)  # IPv4 / IPv6

    def call_command(self, command):
        """Method for calling a method by passing method name as string ("command").
        This help keeping the main method of this class centralized. (error handling etc.)"""

        if command in dir(self): # If command string represents a valid method in this class...
            method = getattr(self, str(command), lambda: "Invalid mode.") # convert "command" string into method
            # Executing the actual method. This could be in a try-except structure and Exception could be handled here.
            method()
        else:
            raise ValueError("Invalid command: %s. Refer to help for available commands."%command)

    def _check_overlaps(self, if_list):
        """Using ipaddress module: network.overlaps(other_network) return True if they overlap
        BUT: "Multiple IPs in the same subnet are still fine" !!!

        Args:
            if_list: list of strings. Each string should represent a network address

        Returns:
            overlaps: list of overlapping interface names. names are elements of if_list
        """
        from ipaddress import IPv4Interface

        # # overlaps method is "symmetric" -> Enough to test combination excluding duplicates ([1,2,3] -> 1-2, 1-3, 2-3)
        # combinations = get_combinations([1,2,3,4]) # Testing
        combinations = self._get_combinations(if_list)  # Testing

        overlaps = list()
        # Test each pairs for overlapping
        for pair in combinations:
            try:
                addr_a = pair[0]  # string
                addr_b = pair[1]
                if_a = IPv4Interface(addr_a)  # object
                if_b = IPv4Interface(addr_b)
                net_a = if_a.network  # "network"
                net_b = if_b.network
            except:
                raise ValueError("(10001) unexpected inteface-pair: %s" % str(pair))
            # print(pair, if_a, if_b)

            if net_a.overlaps(net_b):  # True if if_a and if_b overlap
                # If networks overlap, but IPs are in the same network , that is fine. Otherwise add ifaces to overlaps list.
                if (if_a.network == if_b.network):
                    pass  # Do not append 'overlaps' list, because it's 'still fine'
                else:
                    overlaps.append(addr_a)
                    overlaps.append(addr_b)
            else:
                pass

        return overlaps

    def _filter_ip_addresses(self, ip_addr_show_output, format=AddressFormats.dotted_decimal):
        """Filter for IP addresses in text and insert them to a list.
        IPv4 version

        Args:
            ip_addr_show: multiline text, format is identical with 'ip addr show' command output format. (https://man7.org/linux/man-pages/man8/ip-address.8.html)
            format: Enum (AddressFormats). Specifies the format of elements in ifaces list

        Returns:
            ifaces_list: list of strings
        """
        ifaces_list = list()

        # Define regexp patters for finding IPv4 format
        # Wanted address lines starting with 'inet '. So we exclude the sit0 type interfaces , e.g. "link/sit 0.0.0.0 brd 0.0.0.0"
        pattern_ipv4_without_mask = re.compile('inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}') # # 127.0.0.1, 192.168.0.28
        pattern_ipv4_with_mask = re.compile('inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}') # 127.0.0.1/8, 192.168.0.28/24

        # Select te proper regexp patter based on format argument
        if format == AddressFormats.dotted_decimal:
            pattern = pattern_ipv4_without_mask
        elif format == AddressFormats.dotted_decimal_with_netmask:
            pattern = pattern_ipv4_with_mask
        else:
            raise ValueError("(10010) Requested address format is not implemented:%s"%(str(format.name)))

        # Search for the actual addresses and append ifaces_list
        lines = ip_addr_show_output.split("\n")
        for line in lines:
            #ipv4_addr = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            ipv4_addr = re.search(pattern, line)
            if ipv4_addr:
                ipv4_addr = ipv4_addr.group()
                ifaces_list.append(ipv4_addr[5:]) # cut down "inet " from the beginning

        return ifaces_list

    def _formatted_print(self, ifaces_list, separator="\n"):
        """ Printing only.
        Printing list elements separated by 'separator'. Default separator is new line '\n'.

        Args:
            ifaces_list: list of strings to print
            separator: elements separated by 'separator'. Default separator is new line '\n'.

        Returns:

        """
        # 1. Basic format and/or datatype checking..
        if not isinstance(ifaces_list, list):
            raise TypeError("(10013) Improper data type: %s" % (type(ifaces_list)))

        # 2. Concatenate list elements
        string_to_print = separator.join(ifaces_list)

        # 3. Actual printing to stdout
        print(string_to_print)

        return 0

    def _get_combinations(self, list):
        """Get Combinations of list elements.
         Example: ([1,2,3] -> 1-2, 1-3, 2-3)

        Args:
            list: list of items, items can be any data type

        Returns:
            combination, object, tuple of pairs
        """
        import itertools  # builtin, Py >=3.5

        # print(list)

        # Example: (list:[1,2,3] -> combinations: [(1,2), (1,3), (2,3)])
        combinations = itertools.combinations(list, 2)  # https://docs.python.org/3/library/itertools.html#module-itertools
        # for pair in combinations:
        #     print(pair)
        return combinations

    def get_list_of_all_interfaces(self, format=AddressFormats.dotted_decimal):
        """Getting the list of interfaces of current system.
        /This can be system-type specific. Can be different on Windows and Linux systems. But now we focus on Debian/Ubuntu like Linux OSs/

        Args:
            format: Enum (AddressFormats). Specifies the format of elements in ifaces list
            testfile: Filename to pass test vectors. If not passed ,then current system interfaces will be listed. default=None

        Returns:
            ifaces_list: list of strings. Strings are in the required format (-> format Arg)
        """
        logger.debug("List of ifaces.")

        # 1. Reading interface setting. Either from system or from a testfile
        if not self.testfile:
            logger.debug("Reading ifaces from current os")
            ip_addr_show = self._read_interfaces_on_current_system()
        else:
            logger.debug("Reading ifaces from testfile: %s"%self.testfile)
            ip_addr_show = self._read_interfaces_from_testfile(self.testfile)
        logger.debug(ip_addr_show)

        # 2. Filter text for IP addresses
        ifaces_list = self._filter_ip_addresses(ip_addr_show, format)
        logger.info(ifaces_list)

        return ifaces_list

    def print_interface_addresses(self):
        """Write all IPv4 addresses to stdout, separated by newlines"""
        ifaces = self.get_list_of_all_interfaces(format=AddressFormats.dotted_decimal) # list of all interfaces
        self._formatted_print(ifaces,separator="\n")

    def print_interface_addresses_with_prefix(self):
        """Write all IPv4 addresses to stdout, separated by newlines. WITH NETMASK"""
        ifaces = self.get_list_of_all_interfaces(format=AddressFormats.dotted_decimal_with_netmask)  # list of all interfaces
        self._formatted_print(ifaces, separator="\n")

    def print_overlapping_interface_addresses(self):
        """Write ovelapping IPv4 addresses to stdout, separated by newlines"""
        logger.debug(self.testfile)
        ifaces = self.get_list_of_all_interfaces(format=AddressFormats.dotted_decimal_with_netmask)  # list of all interfaces
        overlaps = self._check_overlaps(ifaces)
        self._formatted_print(overlaps, separator="\n")

    def _read_interfaces_from_testfile(self, testfile):
        """Reading network interface settings from a testfile.
        Testfile should contain a text that's format is identical to 'ip addr show' command output on Linux systems

        Returns:
            ifaces: string. Output of ip addr show command
        """
        # 1. Check testfile format
        # ToDo: this is not implemented. Some basic cehcking would be required

        # 2. Read file content
        f = open(testfile, "r")
        ifaces = f.read()
        f.close()
        return ifaces

    def _read_interfaces_on_current_system(self):
        """Reading network interface settings. This could be moved to an OS-specific class and could be based on 'ifconfig' and 'ip' commands.
         Current implementation uses 'ip' command.

         Returns:
             ifaces: string. Output of ip addr show command
        """
        cmd = "ip addr show"
        cmd = cmd.split(" ")
        s = subprocess.run(cmd, stdout=subprocess.PIPE, check=True) # throws exception in case of any issue
        ifaces = s.stdout.decode("utf-8")
        return ifaces

    def _switch_to_ip_version_specific_class(self, ip_version):
        """Switch to class specific to IPv4 / IPv6.
        IPv4: it does not have separate class for now -> no swithcing needed
        IPv6: switching to InterfaceParser_IPv6

        self.ip_version will be set to IPVersion.IPv4 or IPVersion.IPv6 for later usage in class methods
        """
        if ip_version == "4":
            self.ip_version=IPVersion.IPv4
            logger.debug("IPv4 has been selected")
        elif ip_version == "6":
            self.__class__= InterfaceParser_IPv6 # Switching to more specific class
            self.ip_version=IPVersion.IPv6
            logger.debug("IPv6 has been selected")
        else:
            raise ValueError("Invalid IP Version has been selected: %s"%ip_version)


class InterfaceParser_IPv6(InterfaceParser):
    """Child class of InterfaceParser for replacing IPv4 method to IPv6.
    Switching to this child class happens in __init__() of parent class, based on IP version."""

    def read_system_addresses(self):
        pass

    def _filter_ip_addresses(self, ip_addr_show_output, format=AddressFormats.dotted_decimal):
        """Filter for IP addresses in text and insert them to a list.
        IPv6 version

        Args:
            ip_addr_show: multiline text, format is identical with 'ip addr show' command output format. (https://man7.org/linux/man-pages/man8/ip-address.8.html)
            format: Enum (AddressFormats). Specifies the format of elements in ifaces list

        Returns:
            ifaces_list: list of strings
        """
        raise Exception("This method is not implemented yet.")
        ifaces_list = list()

        # Define regexp patters for finding IPv4 format
        # Wanted address lines starting with 'inet '6.

        # Select te proper regexp patter based on format argument
        #AddressFormats.ipv6_hex , AddressFormats.ipv6_hex etc.

        # Search for the actual addresses and append ifaces_list
        # lines = ip_addr_show_output.split("\n")
        # for line in lines:
        #     #ipv4_addr = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        #     ipv4_addr = re.search(pattern, line)
        #     if ipv4_addr:
        #         ipv4_addr = ipv4_addr.group()
        #         ifaces_list.append(ipv4_addr[5:]) # cut down "inet " from the beginning

        return ifaces_list


