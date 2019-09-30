import argparse
import os
import sys
sys.path.append(os.environ['CI_SITE_CONFIG'])
import ci_site_config
import run
import common

parser = argparse.ArgumentParser()
parser.add_argument("test_node",help="the test node on which this test must be executed")
parser.add_argument("core", help="core provider", choices=["psm2", "verbs", "tcp",
                    "udp", "sockets", "shm"])
parser.add_argument("--build_mode", help="specify the build configuration", 
                     choices = ["debug", "dl"])
args = parser.parse_args()
node = args.test_node
args_prov = args.core
build_mode = args.build_mode
node_fabric = os.environ['FABRIC'] #ci_site_config.fabric_map(node)

mpilist = ['impi', 'mpich', 'ompi']
hosts = [node]

#this script is executed from /tmp
#this is done since some mpi tests
#look for a valid location before running
# the test on the secondary host(client)
# but jenkins only creates a valid path on 
# the primary host (server/test node)

os.chdir('/tmp/')

for host in ci_site_config.node_map[node]:
    hosts.append(host)

for prov in common.prov_list:
    if (prov.core == args_prov):
            #fabtests
        if (prov.util == None):
            run.fabtests(prov.core, hosts)
            for mpi in mpilist:
                run.intel_mpi_benchmark(prov.core, hosts, mpi)   
                #run.mpistress_benchmark(prov.core, hosts, mpi)
                run.osu_benchmark(prov.core, hosts, mpi)  
        else:
            run.fabtests(prov.core, hosts, prov.util)
            for mpi in mpilist:
                run.intel_mpi_benchmark(prov.core, hosts, mpi, prov.util)
                #run.mpistress_benchmark(prov.core, hosts, mpi, prov.util)
                run.osu_benchmark(prov.core, hosts, mpi, prov.util)        
