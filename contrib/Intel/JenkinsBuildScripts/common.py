import itertools
import collections
import re
import copy
import math
import cisite_config

def get_node_name(host, interface):
   # This is the pattern we follow in SFS team cluster
   return "%s-%s" % (host, interface)
