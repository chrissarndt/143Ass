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
	}



class Dijkstra (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        self.delays = {}
	self.switches = {}
	with open(delayFile, "r") as f:
		reader = csv.DictReader(f)
		for link, delay in reader:
			# match with linkname
			s1, s2 = linkNames[link]
			self.delays[(s1, s2)] = int(delay)
			self.delays[(s2, s1)] = int(delay)

			self.switches.add(s1)
			self.switches.add(s2)

	log.debug("Enabling Dijkstra Module")
	

    def _dijkstras(src, dst):
	# initialize distances
	distanceArray = defaultdict(lambda:float('inf'))
	distanceArray[src] = 0

	#initialize prev storage
	prevArray = {}
	unseen = set.copy(self.switches)
	

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))        

def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
