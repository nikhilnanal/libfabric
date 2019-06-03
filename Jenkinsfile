pipeline {
    agent any
    triggers {
        pollSCM('H/2 * * * *')
    }
    stages {
        stage ('build') {
            steps {
                sh 'rm -rf /var/lib/jenkins/workspace/libfabrics-pipbuild'
                sh 'mkdir /var/lib/jenkins/workspace/libfabrics-pipbuild'
                sh './autogen.sh'
                sh './configure --prefix="/var/lib/jenkins/workspace/libfabrics-pipbuild"'
                sh 'make && make install'
                sh 'echo "Hello World" '
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
                sh 'echo "to-do tests here" '
                sh 'cd fabtests'
                sh './autogen.sh'
                sh './configure --prefix="/var/lib/jenkins/workspace/libfabric-fabtests" --with-libfabric="/var/lib/jenkins/workspace/libfabrics-pipbuild"'
                sh 'make && make install'
                sh 'echo "Hello World 2"'
            }
        }
    }
}
