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
                sh 'echo "Hello World" '
            }
        }
      
    }
      post {
          success {
        setBuildStatus("Build succeeded", "SUCCESS");
        }
       failure {
        setBuildStatus("Build failed", "FAILURE");
        }
      }
}
