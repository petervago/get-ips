"""Test Vectors

vector data is stored in list of tuples.
Tuples:
    Cohesive data for the followings:
        - comment: to give a human readable meaning to the test element
        - "ip addr show" output
        - expected "get-ips" result # Task1
        - expected "get-ips --with-prefix" result # Task2
        - expected "get-ips --overlapping" result # Task3
"""

vector = [
    ("01 - My laptop's interfaces",
     """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eno1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether ec:f4:bb:24:5e:4e brd ff:ff:ff:ff:ff:ff
3: wlp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 80:86:f2:10:66:e3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.28/24 brd 192.168.0.255 scope global dynamic noprefixroute wlp2s0
       valid_lft 62037sec preferred_lft 62037sec
    inet6 2001:4c4c:2111:2000::4/128 scope global dynamic noprefixroute
       valid_lft 1119749sec preferred_lft 598436sec
    inet6 2001:4c4c:2111:2000:3955:17d9:c707:55a5/64 scope global temporary dynamic
       valid_lft 598436sec preferred_lft 79587sec
    inet6 2001:4c4c:2111:2000:9a2:1877:d5cc:6ddf/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 1133176sec preferred_lft 604779sec
    inet6 fe80::7fa2:53af:519a:26d/64 scope link noprefixroute
       valid_lft forever preferred_lft forever""",

    """127.0.0.1/8
192.168.0.28/24""",
    """127.0.0.1
    192.168.0.28""",
    ""
    )

]

print(type(vector))
