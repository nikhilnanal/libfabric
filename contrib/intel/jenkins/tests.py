import sys
import os

print(os.environ['CI_SITE_CONFIG'])
sys.path.append(os.environ['CI_SITE_CONFIG']) # for adding path for ci_site_config

import subprocess
import re
import ci_site_config
import common
import shlex

class Test:
    def __init__ (self, branchname, buildno, testname, core_prov, fabric,
                  hosts, util_prov=None, build_mode=None):
        self.branchname = branchname
        self.buildno = buildno
        self.testname = testname
        self.core_prov = core_prov
        self.util_prov = "ofi_{}".format(util_prov) if util_prov != None else "" 
        self.fabric = fabric
        self.hosts = hosts
        self.build_mode = build_mode
        if (len(hosts) == 2):
            self.server = hosts[0]
            self.client = hosts[1]
       
        self.nw_interface = ci_site_config.interface_map[self.fabric]
        if (self.build_mode == None):
            self.libfab_installpath = "{}/{}/{}/reg".format(ci_site_config.install_dir,
                                  self.branchname, self.buildno)
        elif (self.build_mode == 'dbg'):
            self.libfab_installpath =  "{}/{}/{}/dbg".format(ci_site_config.install_dir,
                                  self.branchname, self.buildno)
        elif (self.build_mode == 'dl'):
            self.libfab_installpath =  "{}/{}/{}/dl".format(ci_site_config.install_dir,
                                  self.branchname, self.buildno)

 
        self.env = [("FI_VERBS_MR_CACHE_ENABLE", "1"),\
                    ("FI_VERBS_INLINE_SIZE", "256")] \
                    if self.core_prov == "verbs" else []
    def run_cmd(self, command):
                             
        outputcmd = shlex.split(command)
        print(outputcmd)
        p = subprocess.Popen(outputcmd,stdout=subprocess.PIPE, text=True)
        while True:
            out = p.stdout.read(1)
            if (out == "" and p.poll() != None):
                break
            if (out != ""):
                sys.stdout.write(out)
                sys.stdout.flush()
        
        if (p.returncode != 0):
            print("exiting with " + str(p.poll()))
            sys.exit(p.returncode)


     

class Fabtest(Test):
    
    def __init__(self, branchname, buildno, testname, core_prov, fabric,
                 hosts, util_prov=None, build_mode=None):
        
        super().__init__(branchname, buildno, testname, core_prov, fabric,
                         hosts, util_prov, build_mode)
        self.fabtestpath = "{}/bin".format(self.libfab_installpath) 
    
    def get_exclude_file(self):
        path = self.libfab_installpath
        efile_path = "{}/share/fabtests/test_configs".format(path)

        prov = self.util_prov if self.util_prov else self.core_prov
        efile_old = "{path}/{prov}/{prov}.exclude".format(path=efile_path, 
                      prov=prov)
        
        if self.util_prov:
            efile = "{path}/{util_prov}/{core_prov}/exclude".format(path=efile_path,
                      util_prov=self.util_prov, core_prov=self.core_prov)
        else:
            efile = "{path}/{prov}/exclude".format(path=efile_path,
                      prov=self.core_prov)
           
        if os.path.isfile(efile):
            return efile
        elif os.path.isfile(efile_old):
            return efile_old
        else:
            print("Exclude file: {} not found!".format(efile))
            return None  

    @property    
    def cmd(self):    
        return "{}/runfabtests.sh ".format(self.fabtestpath)
     
    @property
    def options(self):
        opts = "-vvv -p {} -S ".format(self.fabtestpath)
        if (self.core_prov == "verbs" and self.nw_interface):
            opts = "{} -s {} ".format(opts, common.get_node_name(self.server, 
                    self.nw_interface)) # include common.py
            opts = "{} -c {} ".format(opts, common.get_node_name(self.client, 
                    self.nw_interface)) # from common.py
       
        if (self.core_prov == "shm"):
            opts = "{} -s {} ".format(opts, self.server)
            opts = "{} -c {} ".format(opts, self.client)
            opts += "-N "
            
        if not re.match(".*sockets|udp|tcp.*", self.core_prov):
            opts = "{} -t all ".format(opts)

        efile = self.get_exclude_file()
        if efile:
            opts = "{} -R ".format(opts)
            opts = "{} -f {} ".format(opts, efile)  
        
        for key,val in self.env:
            opts = "{options} -E {key}={value} ".format(options = opts, 
                    key=key, value=val)
    
        if self.util_prov:
            opts = "{options} {core};{util} ".format(options=opts, 
                    core=self.core_prov, util=self.util_prov)
        else:
            opts = "{options} {core} ".format(options=opts,
                    core=self.core_prov)
        
        if (self.core_prov == "shm"):
            opts += "{} {} ".format(self.client, self.server)
        else:
            opts += "{} {} ".format(self.server, self.client)
             
        return opts
   
    @property
    def execute_condn(self):
        return True if (self.core!='shm' or \
                        self.build_mode == 'dbg') else False

    def execute_cmd(self):
        command = self.cmd + self.options
        self.run_cmd(command)       

class MpiTests(Test):
    def __init__(self, branchname, buildno, testname, core_prov, fabric,
                 mpitype, hosts, util_prov=None, build_mode=None):
       
        super().__init__(branchname, buildno, testname, core_prov, 
                         fabric, hosts, util_prov, build_mode)
        self.mpi = mpitype


    @property
    def cmd(self):
        if (self.mpi == "impi" or self.mpi == "mpich"):
            self.testpath = ci_site_config.mpi_testpath #"/home/build/ssg_sfi-buildbot/scripts"
            return "{}/run_{}.sh ".format(self.testpath,self.mpi)
        elif(self.mpi =="ompi"):
            self.testpath = "{}/ompi/bin".format(self.libfab_installpath)
            return "{}/mpirun ".format(self.testpath)      
    
    @property
    def options(self):
        opts = [] 
        if (self.mpi == "impi" or self.mpi == "mpich"):
            opts = "-n {} -ppn {} -hosts {},{} ".format(self.n,self.ppn,
                    self.server,self.client)
                
            if (self.mpi == "impi"):
                opts = "{} -mpi_root={} ".format(opts, 
                        ci_site_config.impi_root)
            else:
                opts = "{} -mpi_root={}/mpich".format(opts, 
                        self.libfab_installpath)
            
            opts = "{} -libfabric_path={}/lib ".format(opts, 
                    self.libfab_installpath)
            
            if self.util_prov:
                opts = "{options} -prov {core};{util} ".format(options=opts, 
                        core=self.core_prov, util=self.util_prov)
            else:
                opts = "{} -prov {} ".format(opts, self.core_prov)

            for key, val in self.env:
                opts = "{} -genv {} {} ".format(opts, key, val)
            
        elif (self.mpi == "ompi"):
            opts = "-np {} ".format(self.n)
            hosts = ",".join([":".join([host,str(self.ppn)]) \
                    for host in self.hosts])
            
            opts = "{} --host {} ".format(opts, hosts)
            
            if self.util_prov:
                opts = "{} --mca mtl_ofi_provider_include {};{} ".format(opts, 
                        self.core_prov,self.util_prov)
            else:
                opts = "{} --mca mtl_ofi_provider_include {} ".format(opts, 
                        self.core_prov)
 
            opts += "--mca orte_base_help_aggregate 0 "
            opts += "--mca mtl ofi --mca pml cm -tag-output "
            for key,val in self.env:
                opts = "{} -x {}={} ".format(opts,key,val)
        return opts

    @property
    def mpi_gen_execute_condn(self):
        return True if (self.core_prov != "udp" and \
                        self.core_prov != "shm" and \
                       (self.core_prov != "verbs" or \
                       self.util_prov == "ofi_rxm" or \
                       self.util_prov == "ofi_rxd")) else False

class MpiTestIMB(MpiTests):

    def __init__(self, branchname, buildno, testname, core_prov, fabric,
                 mpitype, hosts, util_prov=None, build_mode=None):
        super().__init__(branchname, buildno, testname, core_prov, fabric,
                         mpitype, hosts, util_prov, build_mode)
        self.additional_tests = [ 
                                   "Biband",
                                   "Uniband",
                                   "PingPingAnySource",
                                   "PingPingAnySource",
                                   "PingPongSpecificSource",
                                   "PingPongSpecificSource"
        ]
        self.n = 4
        self.ppn = 2

  
    @property
    def imb_cmd(self): 
        return "{}/intel64/bin/IMB-MPI1 -include {}".format(ci_site_config.impi_root,
                ','.join(self.additional_tests))
    @property
    def execute_condn(self):
        return True if (self.mpi == "impi") else False
        
    def execute_cmd(self):
        command = self.cmd + self.options + self.imb_cmd
        self.run_cmd(command) 

        
class MpiTestStress(MpiTests):
     
    def __init__(self, branchname, buildno, testname, core_prov, fabric, 
                 hosts, mpitype, util_prov=None, build_mode=None):
        super().__init__(branchname, buildno, testname, core_prov, fabric, 
                         mpitype,  hosts, util_prov, build_mode)
        
         
        if((self.core_prov == "verbs" or self.core_prov =="psm2")):
            self.n = 16
            self.ppn = 8
        else:
            self.n = 4
            self.ppn = 2
      
    @property
    def stress_cmd(self):
        return "{}/{}/stress/mpi_stress -dcr".format(self.libfab_installpath, self.mpi)

    @property
    def execute_condn(self):
        return True if (self.mpi != 'ompi' or \
                        self.build_mode != 'dbg') else  False
    
    def execute_cmd(self):
        command = self.cmd + self.options + self.stress_cmd
        self.run_cmd(command)          
      
class MpiTestOSU(MpiTests):

    def __init__(self, branchname, buildno, testname, core_prov, fabric,
                 hosts, mpitype, util_prov=None, build_mode=None):
        super().__init__(branchname, buildno, testname, core_prov, fabric,
                         mpitype, hosts, util_prov, build_mode)
        
        self.n = 4 
        self.ppn = 2
        self.two_proc_test_pattern = ['osu_latency',
                                   'osu_bibw',
                                   'osu_latency_mt',
                                   'osu_bw','osu_get_latency',
                                   'osu_fop_latency',
                                   'osu_acc_latency',
                                   'osu_get_bw',
                                   'osu_put_latency',
                                   'osu_put_bw',
                                   'osu_put_bibw',
                                   'osu_cas_latency',
                                   'osu_get_acc_latency'
            ]
        self.osu_mpi_path = "{}/{}/osu/libexec/osu-micro-benchmarks/mpi/". \
                            format(self.libfab_installpath,mpitype) 
    
    @property
    def execute_condn(self): 
        return True if (self.mpi != "ompi" or \
                       (self.core_prov != "sockets" and \
                        self.core_prov != "psm2" and \
                        self.build_mode!="dbg")) \
                    else False
    
    def execute_cmd(self):
        assert(self.osu_mpi_path)
        for root, dirs, files in os.walk(self.osu_mpi_path):
            for file in files:
                if file in self.two_proc_test_pattern:
                    self.n=2
                    self.ppn=1
                else:
                    self.n=4
                    self.ppn=2
                
                launcher = self.cmd + self.options
                osu_cmd = os.path.join(root, file)
                command = launcher + osu_cmd
                self.run_cmd(command)
