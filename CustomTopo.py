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
	for i in range(1, fanout + 1):
		cur = self.addSwitch('a%i' % i)
		agg.append(cur)
		self.addLink(cur, c1, **linkopts1)
		
	# Create edge layer
	edg = []
	for i in range(0, fanout):
		for j in range(1, fanout + 1):
			cur = self.addSwitch('e%i' % ((i * fanout) + j))
			edg.append(cur)
			self.addLink(cur, agg[i], **linkopts2)

	# Create host layer
	for i in range(0, fanout * fanout):
		for j in range(1, fanout + 1):
			cur = self.addHost('h%i' % ((i * fanout) + j))
			self.addLink(cur, edg[i], **linkopts3)


lo1 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
lo2 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
lo3 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)

# topos = { 'custom': ( lambda: CustomTopo(lo1, lo2, lo3)) }
topos = { 'custom': ( lambda: CustomTopo({},{},{})) }
