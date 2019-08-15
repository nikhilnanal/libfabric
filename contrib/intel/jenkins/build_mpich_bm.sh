#!/bin/bash

branchname=$1
buildno=$2

set -e
set -x
#build mpich
    (
	    cd $WORKSPACE
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich_build/  && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich_build/
		    
        /home/build/scm/mpich/configure --disable-oshmem --enable-fortran=no \
            --prefix="/home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/" \
                --with-libfabric="/home/build/ofi-Install/libfabric/$branchname/$buildno/"
		    
        make clean
        make install -j32
    )


#build mpi stress test with mpich
    (
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/stress && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/stress && LD_LIBRARY_PATH=""
		    
        /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/bin/mpicc -lz \
            /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o \
                /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/stress/mpi_stress
    )

#build osu benchmarks with mpich
    (
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/osu && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/osu
		    
            export CC=/home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/bin/mpicc
		    export CXX=/home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/bin/mpicxx
		    export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		    export LD_LIBRARY_PATH=""

        /home/build/scm/osu-micro-benchmarks-5.5/configure \
            --prefix=/home/build/ofi-Install/libfabric/$branchname/$buildno/mpich/osu
		    
        make -j4
        make install
    )
