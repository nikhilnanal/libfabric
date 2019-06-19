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
                    cd fabtests
                    ./autogen.sh
                    ./configure --prefix="/var/lib/jenkins/workspace/libfabric-fabtests" --with-libfabric="/var/lib/jenkins/workspace/libfabrics-pipbuild"
                    make && make install
                    echo "Hello World 2"
                '''
                }
                }
            }
        stage ('execute-tests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']){

                   sh ' echo "execute-tests"'
                   sh 'ls -l /var/lib/jenkins/workspace/'
                  // sh 'cd /var/lib/jenkins/worksapce/libfabric-fabtests/'
                  // sh 'ls -al'

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
