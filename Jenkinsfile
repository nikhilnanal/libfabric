pipeline {
    agent any
    stages {
        stage ('build') {
            steps {
                sh 'rm -rf /var/lib/jenkins/workspace/libfabrics-pipeline'
                sh 'mkdir /var/lib/jenkins/workspace/libfabrics-pipeline'
                sh './autogen.sh'
                sh './configure --prefix="/var/lib/jenkins/workspace/libfabrics-pipeline"'
                sh 'make && make install'
            }
        }
    }
}
