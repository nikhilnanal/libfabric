
pipeline {
    agent any
    triggers {
        pollSCM('H/2 * * * *')
    }
    environment {
    // variables are referenced as ${env.VarName} in shell script.
        ofi_install_dir="/home/build/ofi-Install/libfabric"
    fabtests_install_dir="/home/build/ofi-Install/libfabric-fabtests"
    } 
    stages {
        stage ('fetch-opa-psm2')  {
             steps {
                 withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) { 
                     dir('opa-psm2-lib') {

                        checkout changelog: false, poll: false, scm: [$class: 'GitSCM', branches: [[name: '*/master']], \
                        doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], \
                        userRemoteConfigs: [[url: 'https://github.com/intel/opa-psm2.git']]]                        
                      }
                 }
             }
        }
        
        stage ('build') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) { 
                sh """
                  python3.7 contrib/intel/jenkins/build.py --builditem='libfabric'
                  echo "libfabric build completed"  
                 """
                }
            }
        }
        stage('build-fabtests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) { 
                sh """
                python3.7 contrib/intel/jenkins/build.py --builditem='fabtests'
                echo 'fabtests build completed' 
                """
                }
            }
        }
        
        stage ('build-shmem') {
            steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                sh """
                python3.7  contrib/intel/jenkins/build.py --other_benchmarks='shmem'
                echo 'shmem benchmarks built successfully'
                """
                }
              }
          }
  
        stage ('build OMPI + benchmarks') {
              steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                  sh """
                  python3.7 contrib/intel/jenkins/build.py --mpi='ompi' 
                  echo 'mpi benchmarks with ompi - built successfully'
                 """
                }
              }
          }
    
    stage('build Intel MPI + benchmarks') {
        steps {
          withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                sh """
                python3.7 contrib/intel/jenkins/build.py --mpi='impi'                
                echo 'mpi benchmarks with impi - built successfully'
                """
            }
          }
      }  
    
    stage('build MPICH + benchmarks') {
        steps {
          withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                sh """
                python3.7 contrib/intel/jenkins/build.py --mpi='mpich'
                echo "mpi benchmarks with mpich - built successfully"
                """
              }
            }
        }
   stage('parallel-fi_getinfo-stage') {
            parallel {
                stage('eth-test') {
                     agent {node {label 'FABRIC_1'}}
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin/:$PYTHONPATH'])
                        {
                          sh """
                            env
                            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC}
                            cd  ${env.WORKSPACE}/contrib/intel/jenkins/
                            python3.7 runtests.py n1 tcp
                            python3.7 runtests.py n1 udp 
                            python3.7 runtests.py n1 sockets               
                            cd ${env.WORKSPACE}  
                        """
                        } 
                     }       
       
                 }
                 stage('hfi1-test') {
                     agent {node {label 'FABRIC_2'}}
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin:$PYTHONPATH']) {
                          sh """
                            env
                            echo "run fi_info stage"                   
                            echo ${env.NODE_NAME}
                            echo ${env.FABRIC}
                            echo ${env.CI_SITE_CONFIG}
                         
                            
                            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC}
                            cd ${env.WORKSPACE}/contrib/intel/jenkins/
                            python3.7 runtests.py n5 psm2
                            python3.7 runtests.py n5 verbs                   
                            cd ${env.WORKSPACE} 

                         """
                        } 
                     }       
       
                 }
                 stage('mlx-test') {
                     agent {node {label 'FABRIC_3'}}
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin:$PYTHONPATH']) {
                          sh """
                            env
                            echo "run fi_info stage"                   
                            echo ${env.NODE_NAME}
                            echo ${env.FABRIC}
                            echo ${env.CI_SITE_CONFIG}
                           
                            
                            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC}
                            cd ${env.WORKSPACE}/contrib/intel/jenkins/
                            python3.7 runtests.py n65 verbs                   
                            cd ${env.WORKSPACE}  

                            """
                        } 
                     }       
       
                 }    
            } 
   }        

  }
}
