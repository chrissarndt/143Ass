## RUNNING THE CODE
## 
## Q7: CustomTopo.py
## To create a mininet with the custom topology laid out in 
## the CustomTopo class in CustomTopo.py, run the line:
 
   sudo mn --custom *filepath* --topo custom
 
## where *filepath* is substituted with the filepath to
## CustomTopo.py
## 
## Q8: firewall.py, firewall-policies.csv
## To create a mininet governed by the rules laid out in
## firewall.py and firewall-policies.csv, run the line:
  
    pox.py forwarding.l2_learning misc.firewall & sudo mn *topo* --controller remote --mac
  
## where *topo* is a topography with at least as many hosts
## as firewall-policies.csv mandates from the home directory.
## 
## Q9: topo.py, dijkstra.py, delay.csv
## To create a mininet in which switches are governed by dijkstra's 
## algorithm as laid out in dijkstra.py using the topography 
## laid out in topo.py, run the lines:
  
    pox.py misc.dijkstra & sudo mn --custom topo.py --prtopo custom --controller remote --mac
 
## The weights can be changed by altering delay.csv appropriately; to 
## change the topography, you must change topo.py and the 
## linkNames data structure in dijkstra.py as well.
