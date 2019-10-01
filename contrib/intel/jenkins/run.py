import tests
import subprocess
import sys
import argparse
import os

sys.path.append(os.environ['CI_SITE_CONFIG'])
import ci_site_config

#parser = argparse.ArgumentParser()

#parser.add_argument("core",help="core provider", choices=["psm2","verbs","sockets","tcp","udp","shm"])
#parser.add_argument("--util", help="utility provider", choices=["rxd","rxm"])
#parser.add_argument("host" , help="comma separated list of hosts, e.g. n1,n2...")
#parser.add_argument("test",help="test name", choices=["fabtests","IMB","stress","osu_test"])
#args = parser.parse_args()
#print(args)


fab = os.environ['FABRIC']#args.fabric
brname = os.environ['BRANCH_NAME']#args.branchname
bno = os.environ['BUILD_NUMBER']#args.buildno
#test = args.test
#host = args.host
#core = args.core
#util = args.util 
#hosts = [host]


#this script is executed from the /tmp/ 
#this is required so that mpi tests find a valid location on the test node
#to execute tests incase the jenkins workspace is not created
#on that node. It is not intended that any build files be stored in this location. 

os.chdir('/tmp/')
#runfabtests
def fabtests(core, hosts, util=None, mode=None):
       print("running fabtests for {}-{}-{}".format(core, util, fab))
       runfabtest = tests.Fabtest(branchname=brname,buildno=bno,\
                    testname="runfabtests", core_prov=core, fabric=fab,\
                         hosts=hosts, util_prov=util, build_mode=mode)

       if (runfabtest.execute_condn):
            runfabtest.execute_cmd()
       else:
            print("skipping {} as execute condition fails"\
                  .format(runfabtest.testname))
       print("----------------------------------------------------------------------------------------\n")
    

#imb-tests
def intel_mpi_benchmark(core, hosts, mpi, util=None, mode=None):
    imb_test = tests.MpiTestIMB(branchname=brname,buildno=bno,\
               testname="IntelMPIbenchmark",core_prov=core, fabric=fab,\
               hosts=hosts, util_prov=util, mpitype=mpi, build_mode=mode)
    
    if (imb_test.execute_condn == True  and imb_test.mpi_gen_execute_condn == True):
        print("running imb-test for {}-{}-{}-{}".format(core, util, fab, mpi))
        imb_test.execute_cmd()
    else:
        print("skipping {} as execute condition fails"\
                    .format(imb_test.testname))
    print("----------------------------------------------------------------------------------------\n")
    
#mpi_stress benchmark tests
def mpistress_benchmark(core, hosts, mpi, util=None, mode=None):
    stress_test = tests.MpiTestStress(branchname=brname,buildno=bno,\
                  testname="stress",core_prov=core, fabric=fab, hosts=hosts, \
                  util_prov=util,mpitype=mpi, build_mode=mode)
 
    if (stress_test.execute_condn == True and stress_test.mpi_gen_execute_condn == True):
        print("running mpistress-test for {}-{}-{}-{}".format(core, util, fab, mpi))
        stress_test.execute_cmd()
    else:
        print("skipping {} as execute condition fails" \
                    .format(stress_test.testname))
    print("----------------------------------------------------------------------------------------\n")

#osu benchmark tests    
def osu_benchmark(core, hosts, mpi, util=None, mode=None):
    osu_test = tests.MpiTestOSU(branchname=brname, buildno=bno, \
               testname="osu-benchmarks",core_prov=core, fabric=fab,  \
               hosts=hosts, mpitype=mpi, util_prov=util, build_mode=mode)
    
    if (osu_test.execute_condn == True and osu_test.mpi_gen_execute_condn == True):
        print("running osu-test for {}-{}-{}-{}".format(core, util, fab, mpi))
        osu_test.execute_cmd()
    else:
        print("skipping {} as execute condition fails" \
                .format(osu_test.testname))
    print("----------------------------------------------------------------------------------------\n")
