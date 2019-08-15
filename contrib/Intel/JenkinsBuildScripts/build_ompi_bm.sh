#!/bin/bash
branchname=$1
buildno=$2

set -e
 
#build ompi
    (
        cd $WORKSPACE
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/  && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/
         
        /home/build/scm/ompi_4.0.1/configure --disable-oshmem --enable-mpi-fortran=no \
            --prefix=/home/build/ofi-Install/libfabric/$branchname/$buildno/ompi \
                --with-libfabric=/home/build/ofi-Install/libfabric/$branchname/$buildno

        make install -j32
	)
		   
#build mpi stress test with ompi
    (
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/stress && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/stress && LD_LIBRARY_PATH=""
       
        /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/bin/mpicc -lz \
            /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o \
                /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/stress/mpi_stress
    )  
#build osu benchmarks with ompi
    (
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/osu && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/osu
    
        export CC=/home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/bin/mpicc
        export CXX=/home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/bin/mpicxx
        export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
        export LD_LIBRARY_PATH=""

        /home/build/scm/osu-micro-benchmarks-5.5/configure \
            --prefix=/home/build/ofi-Install/libfabric/$branchname/$buildno/ompi/osu
        make -j4
        make install
    )

