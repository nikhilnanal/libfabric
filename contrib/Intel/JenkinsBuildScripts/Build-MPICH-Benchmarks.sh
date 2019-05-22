#build mpich
        BranchName=$1
        BuildNo=$2
		    (
		    cd $WORKSPACE
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich_build/  && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich_build/
		    /home/build/scm/mpich/configure --disable-oshmem --enable-fortran=no --prefix="/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/" --with-libfabric="/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/"
		    make clean
		    make install -j32
		    )

		    #build mpi stress test with mpich
		    (
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/stress && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/stress 
		    /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/mpich/bin/mpicc -lz /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/mpich/stress/mpi_stress
		    )
		    #build osu benchmarks with mpich
		    (
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/osu && cd /home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/osu
		    export CC=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/bin/mpicc
		    export CXX=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/bin/mpicxx
		    export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		    export LD_LIBRARY_PATH=""
		    /home/build/scm/osu-micro-benchmarks-5.5/configure --prefix=/home/build/ofi-Install/libfabric/$BranchName/$BUILD_NO/mpich/osu
		    make -j4
		    make install
		    )
