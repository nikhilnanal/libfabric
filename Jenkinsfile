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
                sh 'rm -rf /var/lib/jenkins/workspace/libfabrics-pipbuild'
                sh 'mkdir /var/lib/jenkins/workspace/libfabrics-pipbuild'
                sh './autogen.sh'
                sh './configure --prefix="/var/lib/jenkins/workspace/libfabrics-pipbuild"'
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
                    if [ -d "/var/lib/jenkins/workspace/libfabric-fabtests" ]; then
                        echo "found fabtests installdir"
                        rm -rf  /var/lib/jenkins/workspace/libfabric-fabtests/
                    fi
                    cd fabtests
                    ./autogen.sh
                    rm -rf $WORKSPACE/libfabrics-fabtests
                    ./configure --prefix="$WORKSPACE/libfabric-fabtests" --with-libfabric="/var/lib/jenkins/workspace/libfabrics-pipbuild"
                    make && make install
                    cd /$WORKSPACE/libfabric-fabtests/
                    ls
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
                        cd libfabric-fabtests/bin/               
                        ./runfabtests.sh
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
