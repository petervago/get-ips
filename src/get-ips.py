#!/usr/bin/python3
"""Author: Peter Vago <peter.vago@gmail.com>, 2021
Dependencies: ipaddress Python package
"""

VERSION = "0.1.0"


import os, sys, argparse, logging # builtin

def print_usage():
    """Print usage"""

def argument_parsing(argv=None):
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
    parser.add_argument("-h","--help", action="store_true",help=parser.print_help(),default=False)
    parser.add_argument("-p","--with-prefix",dest="with_prefix",action="store_true", help="Print prefix lengths.",default=False)
    parser.add_argument("-o","--overlapping",dest="overlapping",action="store_true", help="Print overlaps.",default=False)
    parser.add_argument("-v","--version",dest="getversion",action="store_true", help="Show version.",default=False)
    argcomplete.autocomplete(parser)
    args = parser.parse_args(argv)  # type:dict
    return args

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

    options = argument_parsing(args[1:])  # Do not pass the script name. https://stackoverflow.com/questions/17118999/python-argparse-unrecognized-arguments
    print(options)

def main(args):
    """top-level of get-ips tool

    Args:
        args:

    Returns:

    """
    appdata = dict()

    # I. Initialization
    options = initialize(args)

    # II .Core functionality execution

    # III. Shutdown/release


    return 0

if __name__ == "__main__":
    arguments = sys.argv

    # Here we can pass any test arguments for testing purposes;)
    additional_args = []
    additional_args = ["-h"]
    #additional_args = ["--with-prefix"] # Task2
    # additional_args = ["--overlapping"] # Task3
    for ar_g in additional_args:
        arguments.append(ar_g)
    #print(arguments)
    return_code=main(arguments)
    sys.exit(return_code)