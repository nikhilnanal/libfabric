          
      #!/bin/bash
      BranchName=$1
      BUILD_NO=$2	 
       
      #build mpi stress test with Intel MPI
		   (
		   mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/impi/stress && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/impi/stress && LD_LIBRARY_PATH="/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/lib"
		   /home/build/intel/impi_2019.0.4/intel64/bin/mpicc -lz /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/impi/stress/mpi_stress
		   )
		   #build osu benchmarks with Intel MPI
		   (
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/impi/osu && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/impi/osu
		    export CC=/home/build/intel/impi_2019.0.4/intel64/bin/mpicc
		    export CXX=/home/build/intel/impi_2019.0.4/intel64/bin/mpicxx
		    export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		    export LD_LIBRARY_PATH="/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/lib"
		    /home/build/scm/osu-micro-benchmarks-5.5/configure --prefix=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/impi/osu
		    make -j4
		    make install
		   )
