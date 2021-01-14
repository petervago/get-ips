#!/usr/bin/python3
"""Author: Peter Vago, 2021
Dependencies: ifparser Python package
"""

#import commands
import subprocess
from ifparser import Ifcfg

cmd = "ip addr show"
cmd = cmd.split(" ")
ifs = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
ifdata = Ifcfg(commands.get)

