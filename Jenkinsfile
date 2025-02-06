pipeline {
    agent none

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-credentials')
        DOCKERHUB_REPO = 'mesquitadev/fauves-validator'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
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
            cleanWs()
        }
    }
}