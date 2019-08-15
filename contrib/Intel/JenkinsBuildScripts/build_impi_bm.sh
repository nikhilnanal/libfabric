#!/bin/bash
branchname=$1
buildno=$2	 

set -e
       
#build mpi stress test with Intel MPI
    (
         mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/impi/stress && \
            cd /home/build/ofi-Install/libfabric/$branchname/$buildno/impi/stress && \
                LD_LIBRARY_PATH="/home/build/ofi-Install/libfabric/$branchname/$buildno/lib"
		   
         /home/build/intel/impi_2019.0.4/intel64/bin/mpicc -lz /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c \
            -o /home/build/ofi-Install/libfabric/$branchname/$buildno/impi/stress/mpi_stress
    )

#build osu benchmarks with Intel MPI
   (
        mkdir -p /home/build/ofi-Install/libfabric/$branchname/$buildno/impi/osu && \
        cd /home/build/ofi-Install/libfabric/$branchname/$buildno/impi/osu
		export CC=/home/build/intel/impi_2019.0.4/intel64/bin/mpicc
		export CXX=/home/build/intel/impi_2019.0.4/intel64/bin/mpicxx
		export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		export LD_LIBRARY_PATH="/home/build/ofi-Install/libfabric/$branchname/$buildno/lib"
		/home/build/scm/osu-micro-benchmarks-5.5/configure --prefix=/home/build/ofi-Install/libfabric/$branchname/$buildno/impi/osu
		make -j4
		make install
   )
