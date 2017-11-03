from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from collections import defaultdict
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

hosts = {
	
}


class Dijkstra (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        self.delays = {}
	self.nodeList = set()
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

			self.nodeList.add(s1)
			self.nodeList.add(s2)
	
	
	# adding switch <-> host latency to list of delays
	self.delays[('h13', 's12')] = 1
	self.delays[('s12', 'h13')] = 1
	self.delays[('h15', 's14')] = 1
	self.delays[('s14', 'h15')] = 1
	self.delays[('h19', 's18')] = 1
	self.delays[('s18', 'h19')] = 1
	self.delays[('h17', 's16')] = 1
	self.delays[('s16', 'h17')] = 1

	# adding hosts to nodeList
	self.nodeList.add('h13')
	self.nodeList.add('h15')
	self.nodeList.add('h17')
	self.nodeList.add('h19')
	log.debug("Enabling Dijkstra Module")
	

    def _dijkstras(self, src, dst):
	# initialize distances
        print "starting dijkstras"
	distanceArray = defaultdict(lambda:float('inf'))
        distanceArray[src] = 0
	print "src"
	print src
	#initialize prev storage
	prevArray = {}
	
	print "initialized arrays"
	unseen = set.copy(self.nodeList)
	
	print "starting while loop"
	while unseen:
		# find min dist node
		print distanceArray
		u = min(unseen, key=lambda x:distanceArray[x])
		unseen.remove(u)
		print "u"
		print u	
		# print distanceArray[u]
		for neighbor in graph[u]:
			# print neighbor
			# normal dijkstras
			if neighbor in unseen:
				cur = distanceArray[u] + self.delays[(u, neighbor)]
				# print "cur"
				# print cur
				print distanceArray[neighbor]
				if cur < distanceArray[neighbor]:
					distanceArray[neighbor] = cur
					prevArray[neighbor] = u 
					# print prevArray
			# skip condition
			else:
				continue
	print prevArray				
	return prevArray



    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
	
	# iterate through all combinations of src, dest
	for host1 in hostIP.iteritems():
		for host2 in hostIP.iteritems():
			node1 = host1[0]
			node2 = host2[0]
			prevArray = self._dijkstras(node1, node2)
			cur = node2
			while cur != node1:
				prev = prevArray[cur]
				if prev != node1:
					doubleprev = prevArray[prev]
					msg = of.ofp_flow_mod()
                			print hostIP[node1][1]
					print hostIP[node2][1]
					msg.match.dl_src = hostIP[node1][1]
                			msg.match.dl_dst = hostIP[node2][1]
					msg.match.in_port = graph[doubleprev][prev]
					msg.actions.append(of.ofp_action_output(port = graph[prev][cur]))
					event.connection.send(msg)
				cur = prev
				
                		
			        
        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))        
	
def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)
