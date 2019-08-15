
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
                #build opa-psm2
                buildno=${env.BUILD_NUMBER}
                rm -rf ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
                mkdir -p ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
                ./autogen.sh
                ./configure --prefix=${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER} --enable-usnic=no --enable-psm=no --enable-psm2=yes --enable-verbs=yes --enable-rxd=yes --enable-rxm=yes --enable-sockets=yes --enable-tcp=yes --enable-udp=yes --enable-rxd=yes --enable-shm=yes --with-psm2-src="$WORKSPACE/opa-psm2-lib"
                make clean 
                make && make install
                
                 """
                }
            }
        }
        stage('build-fabtests') {
            steps {
                withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) { 
                sh """
                    echo "to-do tests here"    
                    
                     cd $WORKSPACE/fabtests
                    ./autogen.sh
                    ./configure --prefix="${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/" --with-libfabric=${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}
                    make clean
                    make && make install
                """
                }
            }
        }
        
        stage ('build-shmem') {
            steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                sh """
                 branchname="${env.BRANCH_NAME}"
                 buildno="${env.BUILD_NUMBER}"
                  chmod 777 contrib/intel/jenkins/build_shmem.sh
                 ./contrib/intel/jenkins/build_shmem.sh \$branchname \$buildno
                """
                }
              }
          }
  
        stage ('build-benchmarks-with-ompi') {
              steps {
              withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                  sh """
                 branchname="${env.BRANCH_NAME}"
                 buildno="${env.BUILD_NUMBER}"
                 chmod 777 contrib/intel/jenkins/build_ompi_bm.sh 
                 ./contrib/intel/jenkins/build_ompi_bm.sh \$branchname \$buildno  
                 echo "run completed"
                 """
                }
              }
          }
    
    stage('build Intel MPI + benchmarks') {
        steps {
          withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                sh """
                echo "run IntelMPI stage"                                
                branchname="${env.BRANCH_NAME}"
                buildno="${env.BUILD_NUMBER}"
                chmod 777 contrib/intel/jenkins/build_impi_bm.sh 

                ./contrib/intel/jenkins/build_impi_bm.sh \$branchname \$buildno  
              """
            }
          }
      }  
    
    stage('build MPICH + Benchmarks') {
        steps {
          withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin']) {
                sh """
          echo "run Mpich stage"                    
          branchname="${env.BRANCH_NAME}"
          buildno="${env.BUILD_NUMBER}"
          echo ${env.CI_SITE_CONFIG}
          chmod 777 contrib/intel/jenkins/build_mpich_bm.sh 
          ./contrib/intel/jenkins/build_mpich_bm.sh \$branchname \$buildno  
                """
              }
            }
        }
   stage('parallel-fi_getinfo-stage') {
            parallel {
                stage('eth-test') {
                     agent {
                        node {
                            label 'eth'
                          
                        }
                     }
                     steps{
                        withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin/:$PYTHONPATH']) {
                          sh """
                            env
                            echo "run fi_info stage"                   
                            echo ${env.NODE_NAME}
                            echo ${env.FABRIC}
                            echo ${env.CI_SITE_CONFIG}
     
                            ${env.ofi_install_dir}/${env.BRANCH_NAME}/${env.BUILD_NUMBER}/bin/fi_info -f ${env.FABRIC}
                                                        
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1,n2 fabtests
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 fabtests
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 fabtests --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1,n2 fabtests
       
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1,n2 IMB            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 IMB
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 IMB --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1,n2 IMB 
      
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1,n2 stress            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 stress --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1,n2 stress 
       
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py tcp n1,n2 osu_test            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py udp n1,n2 osu_test --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py sockets n1,n2 osu_test         
                         """
                        } 
                     }       
       
                 }
                 stage('hfi1-test') {
                     agent {
                        node {
                            label 'hfi1'

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
                            
                            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5,n6 fabtests
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 fabtests 
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 fabtests --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 fabtests --util=rxm

        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5,n6 IMB
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 IMB 
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 IMB --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 IMB --util=rxm

        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5,n6 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 stress --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 stress --util=rxm

        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py psm2 n5,n6 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 osu_test --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n5,n6 osu_test --util=rxm


                         """
                        } 
                     }       
       
                 }
                 stage('mlx-test') {
                     agent {
                        node {
                            label 'mlx5'
                           
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
                            
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 fabtests
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 fabtests --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 fabtests --util=rxm
       
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 IMB
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 IMB --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 IMB --util=rxm
       
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 stress
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 stress --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 stress --util=rxm
        
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 osu_test
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 osu_test --util=rxd
        python3.7 ${env.WORKSPACE}/contrib/intel/jenkins/run.py verbs n65,n66 osu_test --util=rxm
          
 
                         """
                        } 
                     }       
       
                 }    
            } 
   }        

  }
}
