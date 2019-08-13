import subprocess
import os
import sys

brname = sys.argv[1]
buildno = sys.argv[2]
prov	= sys.argv[3]
print('hello-python');

libfabricpath = "/home/build/ofi-Install/libfabric/" + brname + "/" + buildno +"/"
fabtestroot = "/home/build/ofi-Install/libfabric-fabtests/" + brname + "/" + buildno + "/"

hfi_nodes = ["n105"]
#run_osu_bm
def run_osu_bm(mpitype,impi_test, mpiroot):
	
	 lfabric = "-libfabric_path=" + libfabricpath + "lib"
	 os.chdir('/home/build/ssg_sfi-buildbot/scripts/')


	 launchern = [impi_test,"-n","4","-ppn","2","-hosts","n105,n107",mpiroot,lfabric,"-prov",prov]
	 launcher2 = [impi_test,"-n","2","-ppn","1","-hosts","n105,n107",mpiroot,lfabric,"-prov",prov]

	 two_proc_test_pattern = ['osu_latency','osu_bibw','osu_latency_mt','osu_bw','osu_get_latency','osu_fop_latency','osu_acc_latency','osu_get_bw','osu_put_latency','osu_put_bw','osu_put_bibw','osu_cas_latency','osu_get_acc_latency']
	 osu_mpi_path = libfabricpath + mpitype +  "/osu/libexec/osu-micro-benchmarks/mpi/"
	 for subdir, dirs, files in os.walk(osu_mpi_path):
		 for file in files:
			 if file in two_proc_test_pattern:
				cmd = [os.path.join(subdir,file)]
				print(cmd)
				launcher = launcher2
			 else:
				launcher = launchern
				cmd = [os.path.join(subdir,file)]
				print(cmd)

			
			 exec_cmd =  launcher + cmd
			 print(exec_cmd)
			 ret = subprocess.call(exec_cmd)
		 	 if (ret !=0):
			 	sys.exit(ret)
	
#fi_info_test
def run_fi_info():
	fi_info_path = libfabricpath + "bin/fi_info"
	fi_info_options = ["-p", prov]
	fi_info_test=[fi_info_path]
	fi_info_test = fi_info_test + fi_info_options
	print(fi_info_test)
	ret = subprocess.call(fi_info_test)
	if (ret != 0):
  	 sys.exit(ret)


#run_fabtest
def run_fabtests():
	
	fabtests_path =  fabtestroot  + "bin/"
	fabtests = "./" + "runfabtests.sh"
	run_fabtests = [fabtests]
	excludepath = "/home/build/jenkinsbuild/workspace/libfabric-fabtests/share/fabtests/test_configs/psm2/psm2.exclude"
	run_fabtests_options = ["-vvv", "-p", fabtests_path, "-S", "-t", "all", "-R", "-f", excludepath, prov, "n105", "n107"]  
	os.chdir(fabtests_path);
	
	run_fabtests = run_fabtests + run_fabtests_options
	print(run_fabtests)
	ret = subprocess.call(run_fabtests)
	if (ret != 0):
 	 sys.exit(ret)


# impi-mpich benchmark tests
def run_imb_mpistress(mpitype):
	os.chdir('/home/build/ssg_sfi-buildbot/scripts/')
	
	impi_test =  mpitype[1] # ["./" + "run_impi.sh"]
	mpi_root =   mpitype[2] # "-mpi_root=/home/build/intel/impi_2019.0.4"
	


	lfabric = "-libfabric_path=/home/build/ofi-Install/libfabric/" + brname + "/" + buildno + "/" + "lib"
	
	#imb-test
	if (mpitype[0] == "impi"):
		imb_test = "/home/build/intel/impi_2019.0.4/intel64/bin/IMB-MPI1"
		imb_include = "Biband,Uniband,PingPingAnySource,PingPingAnySource,PingPongSpecificSource,PingPongSpecificSource"
		imb_options = ["-n","4","-ppn","2","-hosts","n105,n107",mpi_root,lfabric,"-prov",prov,imb_test,"-include",imb_include]
		run_imb_test = [impi_test] + imb_options
		print(run_imb_test);
		ret = subprocess.call(run_imb_test)
		if (ret != 0):
 	 	  sys.exit(ret)

	#mpistress-test
	mpistress_test = libfabricpath + mpitype[0] + "/stress/mpi_stress"
	mpistress_options = ["-n", "16", "-ppn","8","-hosts","n105,n107",mpi_root, lfabric,"-prov",prov,mpistress_test,"-dcr"]
	
	run_mpistress_test = [impi_test] + mpistress_options 
	print(run_mpistress_test)
	ret = subprocess.call(run_mpistress_test)
	if (ret != 0):
 	  sys.exit(ret)

	#osu_bm
	run_osu_bm(mpitype[0],impi_test,mpi_root)



def ompi_mpistress():
	ompirun = [libfabricpath + "ompi/bin/mpirun"]
	mpistress_test = libfabricpath + "ompi/stress/mpistress -dcr"
	ompistress_options =["-np", "16", "--host","n105:8,n107:8","--mca", "mtl_ofi_provider_include", "psm2", "--mca", "orte_base_help_aggregate", "0", "--mca", "mtl", "ofi", "--mca", "pml", "cm", "-tag-output", mpistress_test]
	run_ompi_mpistress = ompirun + ompistress_options
 	print(run_ompi_mpistress)                                             
        ret = subprocess.call(run_ompi_mpistress)                                    
        if (ret != 0):                                                          		
	   sys.exit(ret)	

	
run_fi_info()
run_fabtests()
intelmpi = ("impi","./run_impi.sh","-mpi_root=/home/build/intel/impi_2019.0.4")
run_imb_mpistress(intelmpi)
mpich = ("mpich","./run_mpich.sh","-mpi_root=" + libfabricpath + "/mpich")
run_imb_mpistress(mpich)

#ompi_mpistress()

