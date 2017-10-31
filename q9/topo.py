from mininet.topo import Topo

class Q9Topo(Topo):
    def __init__(self,**opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
	# Add hosts
	h13 = self.addHost('h13')
	h15 = self.addHost('h15')
	h17 = self.addHost('h17')
	h19 = self.addHost('h19')
	
	# Add switches
	s11 = self.addSwitch('s11')
	s12 = self.addSwitch('s12')
	s14 = self.addSwitch('s14')
	s16 = self.addSwitch('s16')
	s18 = self.addSwitch('s18')

	# Add switch/host links
	self.addLink(h13, s12)
	self.addLink(h15, s14)
	self.addLink(h17, s16)
	self.addLink(h19, s18)

	# Add switch/switch links
	self.addLink(s11, s12, delay='10ms')
	self.addLink(s12, s14, delay='50ms')
	self.addLink(s14, s16, delay='10ms')
	self.addLink(s16, s18, delay='30ms')
	self.addLink(s18, s11, delay='30ms')
	self.addLink(s12, s18, delay='10ms')
	self.addLink(s12, s16, delay='100ms')
	self.addLink(s18, s14, delay='20ms')


	
        
                    
topos = { 'custom': ( lambda: Q9Topo() ) }
