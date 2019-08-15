
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
                     agent {
                        node {
                            label 'FABRIC_1'
                        }
                     }
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin/:$PYTHONPATH'])
                        {
                          sh """
                            env
            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC}
            cd  ${env.WORKSPACE}/contrib/intel/jenkins/
            python3.7 run.py tcp n1 fabtests
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 fabtests
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 fabtests --util=rxd
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1 fabtests

            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1 IMB
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 IMB
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 IMB --util=rxd
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1 IMB

            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1 stress
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 stress
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 stress --util=rxd
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1 stress

            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1 osu_test
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 osu_test
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1 osu_test --util=rxd
            python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1 osu_test
                        
            cd ${env.WORKSPACE}  
                        """
                        } 
                     }       
       
                 }
                 stage('hfi1-test') {
                     agent {
                        node {
                            label 'FABRIC_2'

                        }
                     }
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin:$PYTHONPATH']) {
                          sh """
                            env
                            echo "run fi_info stage"                   
                            echo ${env.NODE_NAME}
                            echo ${env.FABRIC}
                            echo ${env.CI_SITE_CONFIG}
                         
                            
                            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC}
                            
                            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5 fabtests
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 fabtests 
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 fabtests --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 fabtests --util=rxm

        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5 IMB
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 IMB 
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 IMB --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 IMB --util=rxm

        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 stress --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 stress --util=rxm

        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 osu_test --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5 osu_test --util=rxm


                         """
                        } 
                     }       
       
                 }
                 stage('mlx-test') {
                     agent {
                        node {
                            label 'FABRIC_3'
                           
                        }
                     }
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin:$PYTHONPATH']) {
                          sh """
                            env
                            echo "run fi_info stage"                   
                            echo ${env.NODE_NAME}
                            echo ${env.FABRIC}
                            echo ${env.CI_SITE_CONFIG}
                           
                            
                            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC} 
                            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 fabtests
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 fabtests --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 fabtests --util=rxm
       
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 IMB
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 IMB --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 IMB --util=rxm
       
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 stress --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 stress --util=rxm
        
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 osu_test --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65 osu_test --util=rxm
          
 
                         """
                        } 
                     }       
       
                 }    
            } 
   }        

  }
}
