from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
delayFile = "delay.csv"

''' Add your global variables here ... '''

# letter names for each link
linkNames = {
	'g': ('s11', 's12'),
	'h': ('s12', 's14'),
	'i': ('s14', 's16'),
	'j': ('s16', 's18'),
	'k': ('s18', 's11'),
	'l': ('s12', 's18'),
	'm': ('s12', 's16'),
	'n': ('s14', 's18'),
	}



class Dijkstra (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        self.delays = {}
	with open(delayFile, "r") as f:
		reader = csv.DictReader(f)
		for link, delay in reader:
			# match with linkname
			s1, s2 = linkNames[link]
			self.delays.add[(s1, s2)] = int(delay)
			self.delays.add[(s2, s1)] = int(delay)
	log.debug("Enabling Dijkstra Module")
	

    def _dijkstras(src, dst):
	

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))        

def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
