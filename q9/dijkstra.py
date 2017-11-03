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
delayFile = "%s/pox/pox/misc/delay.csv" % os.environ[ 'HOME' ]

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

graph = {
	's11': {'s12':1, 's18':2},
	's12': {'h13':1, 's11':2, 's14':3, 's16':4, 's18':5},
	's14': {'h15':1, 's12':2, 's16':3, 's18':4},
   	's16': {'h17':1, 's12':2, 's14':3, 's18':4},
    	's18': {'h19':1, 's11':2, 's12':3, 's14':4, 's16':5},
    	'h13': {'s12':0},
    	'h15': {'s14':0},
    	'h17': {'s16':0},
    	'h19': {'s18':0},
}

hostIP = {
	'h13': ('10.0.0.1', '00:00:00:00:00:01'),
    	'h15': ('10.0.0.2', '00:00:00:00:00:02'),
    	'h17': ('10.0.0.3', '00:00:00:00:00:03'),
    	'h19': ('10.0.0.4', '00:00:00:00:00:04'),
}


class Dijkstra (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        self.delays = {}
	self.switchList = set()
	with open(delayFile, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		reader.next() # skip header line
		for link, delay in reader:
			if link == 'link':
				continue
			# match with linkname
			s1, s2 = linkNames[link]
			self.delays[(s1, s2)] = int(delay)
			self.delays[(s2, s1)] = int(delay)

			self.switchList.add(s1)
			self.switchList.add(s2)

	# adding switch <-> host latency to list of delays
	self.delays[('h13', 's12')] = 1
	self.delays[('s12', 'h13')] = 1
	self.delays[('h15', 's14')] = 1
	self.delays[('s14', 'h15')] = 1
	self.delays[('h19', 's18')] = 1
	self.delays[('s18', 'h19')] = 1
	self.delays[('h17', 's16')] = 1
	self.delays[('s16', 'h17')] = 1

	log.debug("Enabling Dijkstra Module")
	

    def _dijkstras(src, dst):
	# initialize distances
        distanceArray = defaultdict(lambda:float('inf'))
        distanceArray[src] = 0

	#initialize prev storage
	prevArray = {}

	unseen = set.copy(self.switches)
	
	while unseen:
		# find min dist node
		u = min(unseen, key=lambda node:distanceArray[node])
		unseen.remove(u)
		
		for neighbor in graph[u]:
			# normal dijkstras
			if neighbor in unseen:
				cur = distanceArray[u] + self.delays[(u, neighbor)]
				if cur < distanceArray[neighbor]:
					distanceArray[neighbor] = cur
					prevArray[neighbor] = u 
			# skip condition
			else:
				continue
				
	return prevArray



    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
	
	# iterate through all combinations of src, dest
	for node1 in graph:
		for node2 in graph:
			prevArray = self._dijkstras(node1, node2)
			cur = node2
			while cur is not node1:
				prev = prevArray[cur]
				doubleprev = prevArray[prev]
				msg = of.ofp_flow_mod()
                		msg.match.dl_src = hostIP[node1]
                		msg.match.dl_dst = hostIP[node2]
				msg.match.in_port = graph[doubleprev][prev]
				event.actions.append(of.ofp_action_output(port = graph[prev][cur]))
				event.connection.send(msg)
				cur = prev
				
                		
			        
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))        
	
def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
