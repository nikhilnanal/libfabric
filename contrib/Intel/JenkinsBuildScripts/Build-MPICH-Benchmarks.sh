#build mpich
        BranchName=$1
        BuildNo=$2
		    (
		    cd $WORKSPACE
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich_build/  && cd /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich_build/
		    /home/build/scm/mpich/configure --disable-oshmem --enable-fortran=no --prefix="/home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/" --with-libfabric="/home/build/ofi-Install/libfabric/$BranchName/$BuildNo/"
		    make clean
		    make install -j32
		    )

		    #build mpi stress test with mpich
		    (
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/stress && cd /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/stress && LD_LIBRARY_PATH=""
		    /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/bin/mpicc -lz /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/stress/mpi_stress
		    )
		    #build osu benchmarks with mpich
		    (
		    mkdir -p /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/osu && cd /home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/osu
		    export CC=/home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/bin/mpicc
		    export CXX=/home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/bin/mpicxx
		    export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		    export LD_LIBRARY_PATH=""
		    /home/build/scm/osu-micro-benchmarks-5.5/configure --prefix=/home/build/ofi-Install/libfabric/$BranchName/$BuildNo/mpich/osu
		    make -j4
		    make install
		    )
