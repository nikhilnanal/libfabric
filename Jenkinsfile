pipeline {
    agent any
    triggers {
        pollSCM('H/2 * * * *')
    }
   /* environment {
         //AN_ACCESS_KEY=credentials() //'e9869883-1493-4950-b6be-05283212f145'
         withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin'])
    }*/
    stages {
        stage ('fetch-opa-psm2')  {
             steps {
                 withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) { 
                     dir('opa-psm2-lib') {
                        checkout changelog: false, poll: false, scm: [$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '1024568c-672f-4132-8dab-65c437b8655e', url: 'https://github.com/nikhilnanal/opa-psm2.git']]]
                      sh '''
                         pwd   
                       '''
                      }
                 }
             }
        }
        
        stage ('build') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) { 
                sh 'rm -rf /home/build/jenkinsbuild/workspace/libfabrics-pipbuild'
                sh 'mkdir -p /home/build/jenkinsbuild/workspace/libfabrics-pipbuild'
                sh './autogen.sh'
                sh './configure --prefix="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild" --with-psm2-src="$WORKSPACE/opa-psm2-lib"'
                sh  'make clean' 
                sh 'make && make install'
                sh 'echo "Hello World" '
                }
            }
          /*  post {
                success {
                        sh 'echo "Built successfully"'
                }
                failure {
                        sh ' echo "Build Failure"'   
                }
            }*/
        }
        stage('build-fabtests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) { 
                sh '''
                    echo "to-do tests here"    
                    rm -rf  /home/build/jenkinsbuild/workspace/libfabric-fabtests/
            
                    cd $WORKSPACE/fabtests
                    ./autogen.sh
                    ./configure --prefix="/home/build/jenkinsbuild/workspace/libfabric-fabtests" --with-libfabric="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild"
                    make clean
                    make && make install
                    cd /home/build/jenkinsbuild/workspace/libfabric-fabtests/
                    ls -l
                    echo "Hello World 2"
                '''
                }
                }
            }
        stage ('build-benchmarks') {
            steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                sh '''
                   #build shmem
                   rm -rf /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem
                   mkdir /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem
                   cd  /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem
                   mkdir SOS && tar -xf /home/build/v1.4.2.tar.gz -C SOS --strip-components 1 && cd SOS
                   ./autogen.sh
		   ./configure --prefix=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem --disable-fortran --enable-remote-virtual-addressing --disable-aslr-check --enable-pmi-simple --with-ofi=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ LDFLAGS="-fno-pie"
		   make -j4
		   make check TESTS=
		   make install
		   
		   #build ISx
		   cd /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem
		   git clone --depth 1 https://github.com/ParRes/ISx.git ISx && cd ISx/SHMEM
		   make CC=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem/bin/oshcc LDLIBS=-lm
		   
		   #build PRK
		  # cd /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem
		  # git clone --depth 1 https://github.com/ParRes/Kernels.git PRK && cd PRK
		  # echo -e 'SHMEMCC=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem/bin/oshcc -std=c99 SHMEMTOP=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem/SOS' > common/make.defs
		  # make allshmem
		   
		   #build test-uh
		   cd /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem
		   git clone --depth 1 https://github.com/openshmem-org/tests-uh.git tests-uh && cd tests-uh
		   PATH=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/shmem/bin:$PATH make -j4 C_feature_tests
		   
		   #build ompi benchmarks
		   cd $WORKSPACE
		   mkdir -p /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/  && cd /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/
		   /home/build/scm/ompi_4.0.1/configure --disable-oshmem --enable-mpi-fortran=no --prefix=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi --with-libfabric=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/
		   make install -j32
		   
		   #build mpi stress test with ompi
		   mkdir -p /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/stress && cd /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/stress && LD_LIBRARY_PATH=""
		   /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/bin/mpicc -lz /home/build/scm/wfr-mpi-tests/mpi_stress/mpi_stress.c -o /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/stress/mpi_stress
		   
		   #build osu benchmarks with ompi
		   mkdir -p /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/osu && cd /home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/osu
		   export CC=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/bin/mpicc
		   export CXX=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/ompi/bin/mpicxx
		   export CFLAGS="-I/home/build/scm/osu-micro-benchmarks-5.5/util/"
		   export LD_LIBRARY_PATH=""
		   /home/build/scm/osu-micro-benchmarks-5.5/configure --prefix=/home/build/buildbot/install/ofi/ofi_rhel7/08/ompi/osu
		   make -j4
		   make install
                '''
              }
            }
        }
                    
        stage ('execute-tests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']){
              /*     sh ''' 
                        echo "execute-tests"
                        cd /home/build/jenkinsbuild/workspace/libfabric-fabtests/bin/
                        pwd
                        fi_info -p psm2
                        ./runfabtests.sh -vvv -p /home/build/jenkinsbuild/workspace/libfabric-fabtests/bin/ -S -t all -R -f /home/build/jenkinsbuild/workspace/libfabric-fabtests/share/fabtests/test_configs/psm2/psm2.exclude psm2 n105 n107
                        cd /home/build/ssg_sfi-buildbot/scripts/
                        ./run_impi.sh -n 4 -ppn 2 -hosts n105,n107 -mpi_root=/home/build/intel/impi_2019.0.4 -libfabric_path=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/lib -prov psm2 /home/build/intel/impi_2019.0.4/intel64/bin/IMB-MPI1 -include Biband,Uniband,PingPingAnySource,PingPingAnySource,PingPongSpecificSource,PingPongSpecificSource
                        ./run_impi.sh -n 16 -ppn 8 -hosts n105,n107 -mpi_root=/home/build/intel/impi_2019.0.4 -libfabric_path=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/lib -prov psm2 /home/build/buildbot/install/ofi/ofi_rhel7-debug/10/impi/stress/mpi_stress -dcr
                         echo "The return status of runfabtests.sh is :"
                         echo $?
                         
                 
                    '''
		    */
                }
                
		// sh 'cd /var/lib/jenkins/worksapce/libfabric-fabtests'
            }
        }
    }
  /*  post {  
        success{
          githubNotify account: 'nikhilnanal', context: '', credentialsId: $AN_ACCESS_KEY, description: 'pipelinesuccess', gitApiUrl: 'https://github.com/nikhilnanal/libfabric/blob/master/Jenkinsfile', repo: 'libfabric', sha: '', status: 'SUCCESS', targetUrl: 'http://sfs-login.jf.intel.com:8916/job/'
        }
    }*/
}
