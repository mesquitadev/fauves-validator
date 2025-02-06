pipeline {
    agent none

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-credentials')
        DOCKERHUB_REPO = 'mesquitadev/fauves-validator'
    }

    stages {
        stage('Checkout') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    sh "docker build -t ${env.DOCKERHUB_REPO}:${commitHash} ."
                }
            }
        }
    }

    post {
        always {
            node {
                cleanWs()
            }
        }
    }
}