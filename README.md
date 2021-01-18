# get-ips
Tool for listing IP addresses

## About the project

get-ips is small tool written in Python3 to list network interface settings.

## Gettin source code

git clone https://github.com/petervago/get-ips
chmod +x <workdir>/src/get-ips

## Dependencies

*Python modules
** argparse - processign command line arguments
** argcomplete - command line arguments
** ipaddress - network address tweaking
** pytest - unti testing

* Optional Python modules
** pdoc3 - for generating html documentation

## Usage Examples

Get help on usage

...
cd <workdir>/src/
./get-ips.py -h
...

Get version

...
./get-ips.py -v
...

Get current IPv4 addresses, printed to stdout, seaparetd by newlines

...
./get-ips.py
...

Get current IPv4 addresses with netmask

...
./get-ips.py --with-prefix
...

Get overlapping interfaces (Multiple IPs in the same subnet are allowed)

...
./get-ips.py --overlapping
...

Testing with testfiles (-T option). Testfiles can containd any text in the format of 'ip addr show' output format.

...
./get-ips.py --overlapping -T ../tests/reading_interfaces/examples/05_ip_add_overlaps.txt -dnfo
...

