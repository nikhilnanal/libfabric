pipeline {
    agent any
    triggers {
        pollSCM('H/2 * * * *')
    }
   
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
                sh """
                #build opa-psm2
                rm -rf /home/build/ofi-Install/libfabric/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
	             	mkdir -p /home/build/ofi-Install/libfabric/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
                ./autogen.sh
		            ./configure --prefix=/home/build/ofi-Install/libfabric/${env.BRANCH_NAME}/${env.BUILD_NUMBER} --with-psm2-src="$WORKSPACE/opa-psm2-lib"
                make clean 
                make && make install
                echo "Hello World"
	              """
                }
            }
        }
        stage('build-fabtests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) { 
                sh """
                    echo "to-do tests here"    
                    rm -rf  /home/build/ofi-Install/libfabric-fabtests/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
            	      cd $WORKSPACE/fabtests
                    ./autogen.sh
                    ./configure --prefix="/home/build/ofi-Install/libfabric-fabtests/${env.BRANCH_NAME}/${env.BUILD_NUMBER}" --with-libfabric=/home/build/ofi-Install/libfabric/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
                    make clean
                    make && make install
                """
                }
            }
        }
	    
        stage ('build-shmem') {
            steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                sh """
                 BranchName="${env.BRANCH_NAME}"
                 BuildNo="${env.BUILD_NUMBER}"
                  chmod 777 contrib/Intel/JenkinsBuildScripts/Build-SHMEM.sh
                 ./contrib/Intel/JenkinsBuildScripts/Build-SHMEM.sh \$BranchName \$BuildNo
                """
	            }
	          }
	      }
  
        stage ('build-benchmarks-with-ompi') {
	          steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
	              sh """
                 BranchName="${env.BRANCH_NAME}"
                 BuildNo="${env.BUILD_NUMBER}"
                 chmod 777 contrib/Intel/JenkinsBuildScripts/Build-OMPI-Benchmarks.sh 
                 ./contrib/Intel/JenkinsBuildScripts/Build-OMPI-Benchmarks.sh \$BranchName \$BuildNo  
                 echo "run completed"
                 """
	            }
	          }
	      }
	
    stage('build Intel MPI + benchmarks') {
        steps {
          withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                sh """
                echo "run IntelMPI stage"				                 
                BranchName="${env.BRANCH_NAME}"
                BuildNo="${env.BUILD_NUMBER}"
                chmod 777 contrib/Intel/JenkinsBuildScripts/Build-IntelMPI-Benchmarks.sh 

                ./contrib/Intel/JenkinsBuildScripts/Build-IntelMPI-Benchmarks.sh \$BranchName \$BuildNo  
              """
	        }
	      }
	  }  
	
	stage('build MPICH + Benchmarks') {
	    steps {
	      withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                sh """
		  echo "run Mpich stage"				    
		  BranchName="${env.BRANCH_NAME}"
		  BuildNo="${env.BUILD_NUMBER}"
		  chmod 777 contrib/Intel/JenkinsBuildScripts/Build-MPICH-Benchmarks.sh 
		  ./contrib/Intel/JenkinsBuildScripts/Build-MPICH-Benchmarks.sh \$BranchName \$BuildNo  
                """
              }
            }
        }
 /*                   
        stage ('execute-hfi-psm2-tests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']){
                  /*sh ''' 
                        echo "execute-tests"
                        cd /home/build/jenkinsbuild/workspace/libfabric-fabtests/bin/
                        pwd
                        fi_info -p psm2
                        ./runfabtests.sh -vvv -p /home/build/jenkinsbuild/workspace/libfabric-fabtests/bin/ -S -t all -R -f /home/build/jenkinsbuild/workspace/libfabric-fabtests/share/fabtests/test_configs/psm2/psm2.exclude psm2 n105 n107
                        cd /home/build/ssg_sfi-buildbot/scripts/
                        ./run_impi.sh -n 4 -ppn 2 -hosts n105,n107 -mpi_root=/home/build/intel/impi_2019.0.4 -libfabric_path=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/lib -prov psm2 /home/build/intel/impi_2019.0.4/intel64/bin/IMB-MPI1 -include Biband,Uniband,PingPingAnySource,PingPingAnySource,PingPongSpecificSource,PingPongSpecificSource
                        ./run_impi.sh -n 16 -ppn 8 -hosts n105,n107 -mpi_root=/home/build/intel/impi_2019.0.4 -libfabric_path=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/lib -prov psm2 /home/build/buildbot/install/ofi/ofi_rhel7-debug/10/impi/stress/mpi_stress -dcr
                    
			sh '''
			(
			   set -e
			   install_path="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/"
			   cd /home/build/ssg_sfi-buildbot/scripts/
			   launchern='./run_impi.sh -n 4 -ppn 2 -hosts n105,n107 -mpi_root=/home/build/intel/impi_2019.0.4 -libfabric_path=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/lib -prov psm2'
			   launcher2='./run_impi.sh -n 2 -ppn 1 -hosts n105,n107 -mpi_root=/home/build/intel/impi_2019.0.4 -libfabric_path=/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/lib -prov psm2'
			   two_proc_test_pattern='osu_latency|osu_bibw|osu_latency_mt|osu_bw|osu_get_latency|osu_fop_latency|osu_acc_latency|osu_get_bw|osu_put_latency|osu_put_bw|osu_put_bibw|osu_cas_latency|osu_get_acc_latency'
				
		for cmd in $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/startup/osu_hello $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/startup/osu_init $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_latency $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_mbw_mr $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bibw $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_multi_lat $install_path/impi/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_latency_mt /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_gatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_alltoall /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iscatter /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_scatter /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_reduce /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_igather /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iallreduce /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ialltoall /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ireduce /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iscatterv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_allgather /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_allreduce /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iallgather /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_reduce_scatter /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_gather /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_allgatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ialltoallv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_barrier /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ialltoallw /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_scatterv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_bcast /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iallgatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ibcast /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_igatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ibarrier /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_alltoallv /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_get_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_fop_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_acc_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_get_bw /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_put_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_put_bw /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_put_bibw /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_cas_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/impi/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_get_acc_latency; do
				if [[ $cmd =~ $two_proc_test_pattern ]]; then
					launcher=$launcher2
				else
					launcher=$launchern
				fi
				(set -x; eval $launcher $cmd)	# Doesn't work without eval!
			   done
		        )
			
			(
			 install_path="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/"
			 cd /home/build/ssg_sfi-buildbot/scripts/
			 ./run_mpich.sh -n 16 -ppn 8 -hosts n105,n107 -mpi_root=$install_path/mpich -libfabric_path=$install_path/lib -prov psm2 $install_path/mpich/stress/mpi_stress -dcr
			)
			
			(
			  set -e
			  install_path="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/"
			  cd /home/build/ssg_sfi-buildbot/scripts/
			  launchern='./run_mpich.sh -n 4 -ppn 2 -hosts n105,n107 -mpi_root=/home/build/buildbot/install/ofi/ofi_rhel7/12/mpich -libfabric_path=/home/build/buildbot/install/ofi/ofi_rhel7/12/lib -prov psm2'
			  launcher2='./run_mpich.sh -n 2 -ppn 1 -hosts n105,n107 -mpi_root=/home/build/buildbot/install/ofi/ofi_rhel7/12/mpich -libfabric_path=/home/build/buildbot/install/ofi/ofi_rhel7/12/lib -prov psm2'
			  two_proc_test_pattern='osu_latency|osu_bibw|osu_latency_mt|osu_bw|osu_get_latency|osu_fop_latency|osu_acc_latency|osu_get_bw|osu_put_latency|osu_put_bw|osu_put_bibw|osu_cas_latency|osu_get_acc_latency'
			   for cmd in $install_path/mpich/osu/libexec/osu-micro-benchmarks/mpi/startup/osu_hello $install_path/mpich/osu/libexec/osu-micro-benchmarks/mpi/startup/osu_init $install_path/mpich/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_latency $install_path/mpich/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_mbw_mr /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bibw /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_multi_lat /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_latency_mt /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_gatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_alltoall /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iscatter /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_scatter /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_reduce /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_igather /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iallreduce /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ialltoall /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ireduce /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iscatterv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_allgather /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_allreduce /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iallgather /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_reduce_scatter /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_gather /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_allgatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ialltoallv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_barrier /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ialltoallw /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_scatterv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_bcast /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_iallgatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ibcast /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_igatherv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_ibarrier /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/collective/osu_alltoallv /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_get_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_fop_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_acc_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_get_bw /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_put_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_put_bw /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_put_bibw /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_cas_latency /home/build/buildbot/install/ofi/ofi_rhel7/12/mpich/osu/libexec/osu-micro-benchmarks/mpi/one-sided/osu_get_acc_latency; do
				 if [[ $cmd =~ $two_proc_test_pattern ]]; then
				 	 launcher=$launcher2
				 else
					 launcher=$launchern
				 fi
				 (set -x; eval $launcher $cmd)	# Doesn't work without eval!
			    done
		       )
		       (
		       #ompi - mpi stress test
		        install_path="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/"
		       	$install_path/ompi/bin/mpirun -np 16 --host n105:8,n107:8 --mca mtl_ofi_provider_include psm2 --mca orte_base_help_aggregate 0 --mca mtl ofi --mca pml cm -tag-output $install_path/ompi/stress/mpi_stress -dcr
		       )	
			
			echo "The return status of runfabtests.sh is :"
                         echo $?
                         
                 
                    '''
                }
                
		// sh 'cd /var/lib/jenkins/worksapce/libfabric-fabtests'
            }
        }
	    
	stage ('execute-hfi-rxd-verbs-tests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']){    
		   sh '''
		   	install_path="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild/"
		   	cd /home/build/jenkinsbuild/workspace/libfabric-fabtests/bin/
                        pwd
			./runfabtests.sh -vvv -p $install_path/bin -S -s n105-hfi1_0_1 -c n107-hfi1_0_1 -t all -R -f $install_path/share/fabtests/test_configs/ofi_rxd/ofi_rxd.exclude -E FI_VERBS_MR_CACHE_ENABLE=1 -E FI_VERBS_INLINE_SIZE=256 "verbs;ofi_rxd" 			   n105 n107
			
	
		   '''		
		}
	    }
	}*/
    }
  /*  post {  
        success{
          githubNotify account: 'nikhilnanal', context: '', credentialsId: $AN_ACCESS_KEY, description: 'pipelinesuccess', gitApiUrl: 'https://github.com/nikhilnanal/libfabric/blob/master/Jenkinsfile', repo: 'libfabric', sha: '', status: 'SUCCESS', targetUrl: 'http://sfs-login.jf.intel.com:8916/job/'
        }
    }*/
}
