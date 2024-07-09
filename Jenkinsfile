#!/usr/bin/env groovy

pipeline {
  agent any
    environment {
        SONARSCANNER_HOME = tool 'sonarqube-scanner' // Tool name configured in Jenkins Global Tool Configuration
        JENKINS_API_TOKEN = credentials("JENKINS_API_TOKEN")
          }
 
    stages {

        stage('CLEAN WORKSPACE & CHECKOUT CODE') {
            steps {
                script {
                    // Clean workspace before checking out
                    deleteDir()

                    // Checkout the code from the GitHub repository
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'http-echo-project']], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/EzeChinedumUchenna/http-echo-project.git']]])
                }
            }
        }

        stage('SONARQUBE SCAN') {
            steps {
                script {
                    // Use the configured SonarScanner installation
                    withSonarQubeEnv('sonarqube-server') {
                        sh """
                            ${SONARSCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=Reverse-IP-Server-Project \
                            -Dsonar.projectName="Reverse-IP-Server-Project" \
                            -Dsonar.sources=. \
                            -Dsonar.go.coverage.reportPaths=coverage.out \
                        
                        """
                    }
                }
            }
        }
      
    
      // stage('QUALITY GATE ANALYSIS') {
      //   steps {
      //      script {
      //       timeout(time: 10, unit:'MINUTES') {
             // waitForQualityGate abortPipeline: true
         //    waitForQualityGate abortPipeline: false, credentialsId: 'sonar-last'
         //   }
        //  }
       // }
      //} 
    
      
   
        stage("BUILD IMAGE") {
            steps {
                script {
                    // Navigate to the directory containing the Dockerfile
                   // dir('Reverse-IP-Server-Project') {
                        // Build the Docker image
                        sh 'docker build -t nedumdocker/reverse-ip-server-project:$BUILD_NUMBER .'
                     }
                   }
                }
            // }
 
         stage('Pushing To DockerHUB') {
            steps {
                // Push the Docker image to Azure Container Registry
                script {
                    echo "deploying image to DokerHub ...."
                    withCredentials([usernamePassword(credentialsId: 'docker-registry', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin nedumdocker"
                    sh 'docker push nedumdocker/Reverse-IP-Server-Project:$BUILD_NUMBER'
                  }
               }
            }
         }
        stage('Clean Up Artifact') {
            steps {
              script {
                   sh 'docker rmi anpauthuser.azurecr.io/http-echo-project:$BUILD_NUMBER'
                }
            }
         }

       stage('TRIGGER CD PIPELINE') {
            steps {
                    script {
                      
                       withCredentials([usernamePassword(credentialsId: 'github_Credential', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    // First we are going to attach a metadata to our commit. Like email and username, else Jenkins will complain. This is very important and a must-have at first commit but can be remove aftr that.
                        // Navigate into the 'http-echo-project' directory
                        dir('http-echo-project') {
                              sh "ls -al"
                            dir('helm-Chart') {
                              sh "ls -al"
                              sh 'git init . '
                              sh 'git config user.email "http-echo@gmail.com"' 
                              sh 'git config user.name "http-echo"'
                    
                             // Because my Github Password contain special character @, I will need to encode it else it wont work with Jenkins.
                              def encodedPassword = URLEncoder.encode(PASS, "UTF-8")

                            // Set the Git remote URL with the encoded password
                             sh "git remote -v | grep origin || git remote add origin https://${USER}:${PASS}@github.com/EzeChinedumUchenna/http-echo-project-CD "
                             sh "git remote set-url origin https://${USER}:${PASS}@github.com/EzeChinedumUchenna/http-echo-project-CD "
                             sh 'git fetch origin'
                             sh "sed -i 's/http-echo-project.*/http-echo-project:${BUILD_NUMBER}/g' values.yaml"
                             sh "cat values.yaml"
                             sh 'git add .'
                             sh 'git commit -m "updated file"'
                             sh 'git checkout -b main'
                             sh 'git push --force-with-lease origin main:main'
                             }
                          }
                       }
                    }
                 }
              } 
           }

    //PUSHING NOTIFICATION TO MY EMAIL. this will send email to me if the build fails or succeeds
  post {
      failure {
         script {
                mail (to: 'ezechinedum504@gmail.com',
                        subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) failed",
                        body: "Please visit ${env.BUILD_URL} for further information.",
                        attachmentsPattern: 'trivy.txt,trivyimage.txt'
                     );
                   }
                }
      success {
             script {
                mail (to: 'ezechinedum504@gmail.com',
                        subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) success.",
                        body: "Please visit ${env.BUILD_URL} for further information.",
                        attachmentsPattern: 'trivy.txt,trivyimage.txt'
                   );
                }
             }      
         } 
      }
