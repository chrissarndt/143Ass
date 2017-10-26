from mininet.topo import Topo

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
	# Create core layer
	c1 = self.addSwitch('c1')

	# Create aggregation layer
	agg = []
	for i in irange(1, fanout):
		cur = self.addSwitch('a%i' % i)
		agg.append(cur)
		self.addLink(cur, c1, **linkopts1)
		
	# Create edge layer
	edg = []
	for i in irange(0, fanout - 1):
		for j in irange(1, fanout):
			cur = self.addSwitch('e%i' % ((i * fanout) + j))
			edg.append(cur)
			self.addLink(cur, agg[i], **linkopts2)

	# Create host layer
	for i in irange(0, fanout * fanout - 1):
		for j in irange(1, fanout):
			cur = self.addHost('h%i' & ((i * fanout) + j))
			self.addLink(cur, edg[i], **linkopts3)


linkopts1 = dict(bw=10, delay=’5ms’, loss=10, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay=’5ms’, loss=10, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay=’5ms’, loss=10, max_queue_size=1000, use_htb=True)

                    
topos = { 'custom': ( lambda: CustomTopo( lambda: CustomTopo(linkopts1, linkopts2, linkopts3)) ) }
