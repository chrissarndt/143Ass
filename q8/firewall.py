from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        # blacklist (firewall implementation)
        self.blacklist = []
        with open(policyFile, "r") as f:
                reader = csv.DictReader(f)
                for entry in reader:
                        self.blacklist.append((EthAddr(entry['mac_0']), EthAddr(entry['mac_1'])))
                        self.blacklist.append((EthAddr(entry['mac_1']), EthAddr(entry['mac_0'])))

    # for any switch
    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        for (src, dst) in self.blacklist:
                # create a flow entry that triggers on this (src, dest)
		msg = of.ofp_flow_mod()
                msg.match.dl_src = src
		msg.match.dl_dst = dst
		# gives the firewall higher priority than l2_learning
		msg.priority = 2;

		# by not setting an action for this flow entry, packets that match will be dropped
                event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
