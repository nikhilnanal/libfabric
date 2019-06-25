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
        stage ('build') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) { 
                sh 'rm -rf /home/build/jenkinsbuild/workspace/libfabrics-pipbuild'
                sh 'mkdir -p /home/build/jenkinsbuild/workspace/libfabrics-pipbuild'
                sh './autogen.sh'
                sh './configure --prefix="/home/build/jenkinsbuild/workspace/libfabrics-pipbuild"'
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
                        ./runfabtests.sh -vvv -p /home/build/jenkinsbuild/workspace/libfabric-fabtests/bin/ -S -t all -R -f /home/build/jenkinsbuild/workspace/libfabric-fabtests/share/fabtests/test_configs/psm2/psm2.exclude psm2 n105 n107
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
