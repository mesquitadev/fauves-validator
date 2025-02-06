pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

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
                    def version = sh(script: 'git describe --tags --abbrev=0 || echo "0.0.0"', returnStdout: true).trim()
                    def tag = "${version}-${commitHash}"

                    sh "docker build -t ${env.DOCKERHUB_REPO}:${tag} ."
                    sh "docker tag ${env.DOCKERHUB_REPO}:${tag} ${env.DOCKERHUB_REPO}:latest"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKERHUB_CREDENTIALS') {
                        sh "docker push ${env.DOCKERHUB_REPO}:${tag}"
                        sh "docker push ${env.DOCKERHUB_REPO}:latest"
                    }
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