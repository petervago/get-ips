#!/usr/bin/python3
"""get-ips.py - Commannd line script for calling interface_parser class methods
Author: Peter Vago <peter.vago@gmail.com>, 2021
"""

VERSION = "0.9.0"

import os, sys, logging # builtin
import argparse, argcomplete
import utils # custom module
import interface_parser # custom module

def argument_parsing(argv=None):
    """    Argument Parsing
        - parsing command line options and arguments
        - semantic checking of arg values (if needed)

    :param argv:
    :return:
    """
    """
    Argument Parsing
        - parsing command line options and arguments
        - semantic checking of arg values (if needed)

    Args:
        argv:

    Returns:

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug",type=str, help="Debug level. critical, error, warning, info, debug, notset")
    #parser.add_argument("-h","--help", action="store_true",help=parser.print_help(),default=False)
    parser.add_argument("-p","--with-prefix",dest="with_prefix",action="store_true", help="Print prefix lengths.",default=False)
    parser.add_argument("-o","--overlapping",dest="overlapping",action="store_true", help="Print overlaps.",default=False)
    parser.add_argument("-T", "--testfile", type=str, help="Testfile: testing with file based simulated data.", default=None)  # default is IPv4
    parser.add_argument("-v","--version",dest="getversion",action="store_true", help="Show version.",default=False)
    parser.add_argument("-V","--ip-version",type=str, help="IP version: 4 or 6", default="4") # default is IPv4
    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)  # typ_e: NameSpace
    return args

def get_command(args):
    """Command defines what method is called in execution.
    This method creates logical connection between get-ips arguments and class methods in interface_parser class
    Available commands:
        - print_interface_addresses
        - print_interface_addresses_with_prefix
        - print_overlapping_interface_addresses
    """
    # args: Namespace(debug=None, getversion=False, ip_version='4', overlapping=False, with_prefix=False)

    command = "print_interface_addresses"  # default
    if args.getversion: command="version"
    elif args.with_prefix:
        command = "print_interface_addresses_with_prefix"
        if args.overlapping:
            logger.warning("WARNING: Not defined behavior: --overlapping is specified together with other option(s)")
    elif args.overlapping: command = "print_overlapping_interface_addresses"
    else:
        pass

    logger.debug("Command selected: %s"%command)

    return command


def initialize(args):
    """
    Initialization of script
        - processing arguments
        - init logger
        - extend sys.path to reach utils

    Args:
        args:

    Returns:

    """
    appdata = dict()

    # 0. Init logging
    import utils  # custom module
    logfile = "/tmp/get-ips.log"
    l = utils.mylogging(logfile, logging.WARNING)
    global logger
    logger = l.getlogger_reference()

    # 1. ARGUMENT parsing
    # 1.a - Argument parsing
    parsed_args = argument_parsing(args[1:])  # Do not pass the script name. https://stackoverflow.com/questions/17118999/python-argparse-unrecognized-arguments
    #print(parsed_args)  # Namespace(debug=None, getversion=False, ip_version='4', overlapping=False, with_prefix=False)
    # 1.b. - First, apply new debuglevel if requested and check if getversion is requested
    if parsed_args.getversion:
        print(VERSION)
        sys.exit(0)
    if parsed_args.debug: l.change_debuglevel(parsed_args.debug) # Apply new debuglevel if requested
    # 1.b - Semantic/value checking
    # skipped for now...
    # 1.c - Assign API method command based on arguments
    logger.debug("Parsed arguments: %s" % str(parsed_args))
    appdata["command"] = get_command(parsed_args)
    appdata["ip_version"] = parsed_args.ip_version # "4" for IPv4 or "6" for IPv6
    if parsed_args.testfile: # default: None
        appdata["testfile"] = util_get_file_abs_path(parsed_args.testfile)

    return appdata

def main(args):
    """top-level function of get-ips tool

    Args:
        args:

    Returns:

    """
    # I. Initialization
    appdata = initialize(args)
    logger.debug("Appdata: %s"%appdata)

    # II. Core functionality execution
    ifpars = interface_parser.InterfaceParser(ip_version=appdata["ip_version"])  # ip_version: {"4","6"}
    if "testfile" in appdata.keys(): ifpars.testfile = appdata["testfile"] # If testfile was defined (-T argument), then pass it to ifpars class
    ifpars.call_command(appdata["command"]) # Execute actual command.

    # III. Shutdown/release


    return 0

def util_get_file_abs_path(relative_path):
    """Checking if file exists. If exists, return its abs path."""
    logger.debug(relative_path)
    # 1. Check if file exists. If not , raise Exception
    if not os.path.isfile(relative_path):
        raise FileExistsError("(10014) Requested file does not exist: %s"%(relative_path))

    # 2. Convert path to absolute path
    absolute_path = os.path.abspath(relative_path)
    logger.debug("Testfile absolute path: %s"%absolute_path)

    return absolute_path


if __name__ == "__main__":
    arguments = sys.argv

    # Here we can pass any test arguments for testing purposes;)
    additional_args = []
    #additional_args = ["--overlapping", "-T", "../tests/reading_interfaces/examples/05_ip_add_overlaps.txt" ] # testing overlaps
    #additional_args = ["-dbug"]
    #additional_args = ["-h"]
    #additional_args = ["--with-prefix"] # Task2
    # additional_args = ["--overlapping"] # Task3
    for ar_g in additional_args:
        arguments.append(ar_g)
    #print(arguments)
    return_code=main(arguments)
    sys.exit(return_code)