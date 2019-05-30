pipeline {
    agent any
    stages {
        stage ('build') {
            steps {
                sh 'rm -rf /var/lib/jenkins/workspace/libfabrics-pipbuild'
                sh 'mkdir /var/lib/jenkins/workspace/libfabrics-pipbuild'
                sh './autogen.sh'
                sh './configure --prefix="/var/lib/jenkins/workspace/libfabrics-pipbuild"'
                sh 'make && make install'
            }
        }
    }
    post {
        success {
            sh 'echo "hello world"'
        setBuildStatus("Build succeeded", "SUCCESS");
    }
       failure {
        setBuildStatus("Build failed", "FAILURE");
    }
    }
}
