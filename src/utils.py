"""
Utilities for get-ips
Author: Peter Vago <peter.vago@gmail.com>, 2021
"""

import os, sys, logging, time # builtin

class mylogging():
    """Logging class, Peter Vago, 2019"""
    mylogger = "" # declare only
    recovery_code, recovery_info = 3, "default"
    logfile = ""

    def __init__(self, logfile="/tmp/mylogger.log", LOGGINGLVL=logging.DEBUG, logger_session="app"):
        import logging
        self.logfile = logfile
        # .deleted. log_file recovery

        # Initialize logger
        logformat = "%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s"
        datefmt = "%m-%d %H:%M"
        logging.basicConfig(filename=logfile, level=LOGGINGLVL, filemode="a", format=logformat, datefmt=datefmt)
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(logging.Formatter(fmt=logformat, datefmt=datefmt))
        self.mylogger = logging.getLogger(logger_session)
        self.mylogger.addHandler(stream_handler)
        self.mylogger.setLevel(LOGGINGLVL) # Needs to set explicitly...because basicConfig line does not set ..hmm.

        # if self.recovery_code != 0: #
        #     self.mylogger.info(self.recovery_info) # if logfile has been chown'ed or deleted or any other issue happened...

    def getlogger_reference(self):
        # Data accessor
        return self.mylogger

    def change_debuglevel(self, newlevel):
        # critical, error, warning, info, debug, notset" # https://docs.python.org/2/library/logging.html

        # If new level is given as integer number in string
        try: nl=int(newlevel)
        except:
            nl = newlevel
            pass
        #print(type(nl))
        if isinstance(nl, int):
            self.mylogger.setLevel(nl)
            #logging.getLogger().level = 10
            nl = str(self.mylogger.level)
            #self.mylogger.debug("newlevel:%s" % nl)
            #return 0
        else:
            lvl_list = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
            nl = newlevel.upper()
            if any(nl in l for l in
                   lvl_list):  # True if nl is matching to any string or ANY SUBSTRING in the list. E.g. "NING" -> WARNING :D
                nl_suppl = [s for s in lvl_list if nl in s]  # Type: list!, Supplements , eg. "WARN" -> "WARNING"
                #logging.getLogger().setLevel(nl_suppl[0])
                #logging.getLogger().setLevel(10)
                self.mylogger.setLevel(nl_suppl[0])
                #self.mylogger.debug("\n==================================================================\nnewlevel:%s (%s)" % (nl_suppl[0], str(self.mylogger.level)))
                #self.mylogger.debug(nl_suppl)

                if self.recovery_code != 0:  # This is from __init__, but applying new loglevel...hacking, I know..
                    self.mylogger.info(self.recovery_info)  # if logfile has been chown'ed or deleted or any other issue happened...
                nl=nl_suppl
            else:
                info="Debug level is invalid: '%s' (expected: %s) /non case-sensitive/" % (newlevel, str(lvl_list))
                raise ValueError("(30027) %s"%info)
        self.mylogger.debug("\n==================================================================\nDebug level requested:%s,  level set: %s" % (nl, str(self.mylogger.level)))
        return 0

    def write_to_log(self, entry_to_log="default", prefix="CUSTOM_ENTRY", timestamp="timestamp_enabled"):
          """Write custom entry into the logfile
                e.g. 2020-09-07 14:56: CUSTOM_ENTRY; This is my entry.

          :prefix:
          """
          ts_now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
          # print(ts_now)
          # dt_gmt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
          entry = ts_now + ";" + prefix + ";" + entry_to_log
          try:
              cmd = """echo "%s" >> %s """ % (entry, self.logfile)
              os.popen(cmd)
          except:
              return 2

          return 0

