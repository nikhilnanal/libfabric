import os
import sys

sys.path.append(os.environ['CI_SITE_CONFIG'])

import ci_site_config
import argparse
import subprocess
import shlex

branchname = os.environ['BRANCH_NAME']
buildno = os.environ['BUILD_NUMBER']
workspace = os.environ['WORKSPACE']
install_path = "{installdir}/{brname}/{bno}" \
                .format(installdir=ci_site_config.install_dir,
                        brname=branchname, bno=buildno)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--builditem", help="build libfabric or fabtests",
                     choices=['libfabric','libfabirc-dbg','libfabric-dl', 'fabtests'])
group.add_argument("--mpi", help="select mpi type for building mpi benchmarks",
                    choices=['impi', 'ompi', 'mpich'])
group.add_argument("--other_benchmarks", help="build other non mpi benchmarks",
                           choices=['shmem'])

args = parser.parse_args()

builditem = args.builditem
mpi = args.mpi
other_bm = args.other_benchmarks


def runcommand(command):
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    print(p.returncode)
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

def build_libfabric():
    if (os.path.exists(install_path) != True):
        os.makedirs(install_path)  
    runcommand(['./autogen.sh'])
    runcommand(shlex.split(" ".join(['./configure','--prefix={}'.format(install_path),
                            '--enable-usnic=no', '--enable-psm=no', '--enable-psm2=yes',
                            '--enable-verbs', '--enable-rxd=yes', '--enable-rxm=yes', 
                            '--enable-sockets=yes', '--enable-tcp=yes', '--enable-udp=yes',
                            '--enable-shm=yes','--with-psm2-src={}/opa-psm2-lib'.format(workspace)])))
    runcommand(['make','clean'])
    runcommand(['make'])
    runcommand(['make','install'])

def build_fabtests():
    os.chdir('{}/fabtests'.format(workspace))
    runcommand(['./autogen.sh'])
    runcommand(['./configure','--prefix={}'.format(install_path),
                '--with-libfabric={}'.format(install_path)])
    runcommand(['make','clean'])
    runcommand(['make'])
    runcommand(['make', 'install'])


def build_mpi(mpi, mpisrc, mpi_install_path):
   
    build_mpi_path ="/mpibuilddir/{}-build-dir/{}/{}/".format(mpi, branchname, buildno)
    if (os.path.exists(build_mpi_path) == False):
        os.makedirs(build_mpi_path)
    
    os.chdir(build_mpi_path)
    if (mpi == 'ompi'):
        mpistr = '-mpi-'
    elif (mpi == 'mpich'):
        mpistr= '-'

    cmd = " ".join(["{}/configure".format(mpisrc),
                              "--disable-oshmem", "--enable{}fortran=no". format(mpistr),
                              "--prefix={}".format(mpi_install_path),
                              "--with-libfabric={}".format(install_path)])
    
    configure_cmd = shlex.split(cmd)
    print(configure_cmd)
    print("make clean")
    print("make install -j32")

    runcommand(configure_cmd)
    runcommand(["make", "clean"])
    runcommand(["make", "install", "-j32"])


def build_stress_bm(mpi, mpi_install_path):
    
    stress_install_path = "{}/stress".format(mpi_install_path)
    if (os.path.exists(stress_install_path) == False):
        os.makedirs(stress_install_path)
    os.chdir(stress_install_path)
 
    if (mpi == 'mpich'):
        os.environ['LD_LIBRARY_PATH'] = "{}/lib".format(install_path)

    cmd=" ".join(["{}/intel64/bin/mpicc" \
                    .format(ci_site_config.impi_root), \
                    '-lz', "{}/mpi_stress/mpi_stress.c" \
                    .format(ci_site_config.benchmarks['wfr-mpi-tests']),
                    '-o', "{}/mpi_stress".format(stress_install_path)])
    runcmd = shlex.split(cmd)
    runcommand(runcmd)
 


def build_osu_bm(mpi, mpi_install_path):
    
    osu_install_path = "{}/osu".format(mpi_install_path)
    if (os.path.exists(osu_install_path) == False):
        os.makedirs(osu_install_path)
    os.chdir(osu_install_path)
    
    if (mpi == 'impi'):
        os.environ['CC']="{}/intel64/bin/mpicc".format(ci_site_config.impi_root)
        os.environ['CXX']="{}/intel64/bin/mpicxx".format(ci_site_config.impi_root)
    else: 
        os.environ['CC']="{}/bin/mpicc".format(mpi_install_path)
        os.environ['CXX']="{}/bin/mpicxx".format(mpi_install_path)
    
    os.environ['CFLAGS']="-I{}/util/".format(ci_site_config.benchmarks['osu'])
    cmd = " ".join(["{}/configure".format(ci_site_config.benchmarks['osu']),
                    "--prefix={}".format(osu_install_path)])
   
    configure_cmd = shlex.split(cmd) 
    
    runcommand(configure_cmd)
    runcommand(["make", "-j4"])
    runcommand(["make", "install"])

if (builditem):
    if (builditem == 'libfabric'):
        build_libfabric()
    elif (builditem == 'fabtests'):
        build_fabtests()

if (mpi):

    mpi_install_path = "{}/{}".format(install_path, mpi)   
    if (os.path.exists(mpi_install_path) == False):
        os.makedirs(mpi_install_path) 
    if (mpi == 'impi'):
        os.environ['LD_LIBRARY_PATH'] = "{}/lib".format(install_path)
    else:
        mpisrc = ci_site_config.mpich_src if mpi == 'mpich' \
                 else ci_site_config.ompi_src
        build_mpi(mpi, mpisrc, mpi_install_path)
        os.environ['LD_LIBRARY_PATH']=""
                   
    #build mpi + mpistress benchmark
    build_stress_bm(mpi, mpi_install_path)
    #build mpi + osu benchmark
    build_osu_bm(mpi, mpi_install_path)

if (other_bm):
    pass
    #build-shmem here


