#!/bin/bash
  BranchName=$1
  BUILD_NO=$2

 
 #build ompi
	     (
		   cd $WORKSPACE

		   mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/  && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/
		   /home/build/scm/ompi_4.0.1/configure --disable-oshmem --enable-mpi-fortran=no --prefix=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi --with-libfabric=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO
		   make install -j32
		   )
		   
		   #build mpi stress test with ompi
		   (

		   mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/stress && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/stress && LD_LIBRARY_PATH=""
		   /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/bin/mpicc -lz /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/stress/mpi_stress
		   )
		   
		    #build osu benchmarks with ompi
		   (

		   mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/osu && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/osu
		   export CC=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/bin/mpicc
		   export CXX=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/bin/mpicxx
		   export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		   export LD_LIBRARY_PATH=""
		   /home/build/scm/osu-micro-benchmarks-5.5/configure --prefix=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/ompi/osu
		   make -j4
		   make install
		    )

