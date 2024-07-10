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
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'Reverse-IP-Server-Project']], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/EzeChinedumUchenna/Reverse-IP-Server-Project']]])
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
                  dir('Reverse-IP-Server-Project') {
                        // Build the Docker image
                        sh 'pwd'
                        sh 'ls -al'
                        //sh 'cd ..'
                        sh 'ls -al'
                        sh 'pwd'
                        sh 'docker build -t nedumdocker/app:$BUILD_NUMBER .'
                     }
                   }
                }
             }
 
  stage('Pushing To DockerHUB') {
    steps {
        // Push the Docker image to Docker Hub
        script {
            echo "Deploying image to DockerHub ..."
            withCredentials([usernamePassword(credentialsId: 'docker-registry', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                sh '''
                    echo $PASS | docker login -u $USER --password-stdin docker.io
                    docker push nedumdocker/app:$BUILD_NUMBER
                '''
            }
        }
    }
}
        stage('Clean Up Artifact') {
            steps {
              script {
                   sh 'docker rmi nedumdocker/app:$BUILD_NUMBER'
                }
            }
         }

       stage('TRIGGER CD PIPELINE') {
            steps {
                    script {
                      
                       withCredentials([usernamePassword(credentialsId: 'github_Credential', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    // First we are going to attach a metadata to our commit. Like email and username, else Jenkins will complain. This is very important and a must-have at first commit but can be remove aftr that.
                        // Navigate into the 'http-echo-project' directory
                        dir('Reverse-IP-Server-Project') {
                              sh "ls -al"
                            dir('Deployment') {
                              sh "ls -al"
                              sh 'git init . '
                              sh 'git config user.email "Reverse-IP@gmail.com"' 
                              sh 'git config user.name "Reverse-IP"'
                    
                             // Because my Github Password contain special character @, I will need to encode it else it wont work with Jenkins.
                              def encodedPassword = URLEncoder.encode(PASS, "UTF-8")

                            // Set the Git remote URL with the encoded password
                             sh "git remote -v | grep origin || git remote add origin https://${USER}:${PASS}@github.com/EzeChinedumUchenna/Reverse-IP-Server-CD-Project "
                             sh "git remote set-url origin https://${USER}:${PASS}@github.com/EzeChinedumUchenna/Reverse-IP-Server-CD-Project  "
                             sh 'git fetch origin'
                             sh "sed -i 's/app.*/appt:${BUILD_NUMBER}/g' values.yaml"
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
