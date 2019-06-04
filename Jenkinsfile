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
        stage ('execute-tests') {
            steps {
                sh 'cd /var/lib/jenkins/worksapce/libfabric-fabtests'
            }
    }
        post {
            success {
             githubNotify account: 'nikhilnanal', context: '', credentialsId: 'e9869883-1493-4950-b6be-05283212f145', description: '', gitApiUrl: '', repo: 'libfabric', sha: '', status: 'SUCCESS', targetUrl: ''
            }
        }
}
