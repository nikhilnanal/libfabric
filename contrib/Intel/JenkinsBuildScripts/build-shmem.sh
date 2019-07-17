#!/bin/bash

	( 
	       #build shmem
		rm -rf /home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem
		mkdir /home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem
		cd  /home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem
		mkdir SOS && tar -xf /home/build/v1.4.2.tar.gz -C SOS --strip-components 1 && cd SOS
		./autogen.sh
		./configure --prefix=/home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem --disable-fortran --enable-remote-virtual-addressing --disable-aslr-check --enable-pmi-simple --with-ofi=/home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}" LDFLAGS="-fno-pie"
		make -j4
		make check TESTS=
		make install
	)
		   
      #build ISx
      (
	   cd /home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem
	   git clone --depth 1 https://github.com/ParRes/ISx.git ISx && cd ISx/SHMEM
	   make CC=/home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem/bin/oshcc LDLIBS=-lm
      )
      #build PRK 
      (
	   cd /home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem
	   git clone --depth 1 https://github.com/ParRes/Kernels.git PRK && cd PRK
	   echo -e 'SHMEMCC=/home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem/bin/oshcc -std=c99\nSHMEMTOP=/home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem/SOS\n' > common/make.defs
	   make allshmem
      )
     #build test-uh
      (
	   cd /home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem
	   git clone --depth 1 https://github.com/openshmem-org/tests-uh.git tests-uh && cd tests-uh
	   PATH=/home/build/ofi-Install/libfabric/"${env.CHANGE_ID}"/"${env.BUILD_NUMBER}"/shmem/bin:$PATH make -j4 C_feature_tests
      )
