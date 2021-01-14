"""
Utilities for get-ips
Author: Peter Vago <peter.vago@gmail.com>, 2021
"""

import sys,argparse # builtin

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
parser.add_argument('foo', nargs='+')
args = parser.parse_args()

