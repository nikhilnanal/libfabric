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
        stage('build-test') {
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
        stage ('execute-tests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']){
                   sh ''' 
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
