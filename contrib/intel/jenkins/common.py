import itertools
import collections
import re
import copy
import math
import ci_site_config
import collections

def get_node_name(host, interface):
   # This is the pattern we follow in SFS team cluster
   return "%s-%s" % (host, interface)

Prov = collections.namedtuple('Prov', 'core util')
    

prov_list = [

   Prov("psm2", None),
   Prov("verbs", None),
   Prov("verbs", "rxd"),
   Prov("verbs", "rxm"),
   Prov("sockets", None),
   Prov("tcp", None),
   Prov("udp", None),
   Prov("udp", "rxd"),
   Prov("shm", None),
]

