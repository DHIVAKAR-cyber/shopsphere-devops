pipeline {
    agent any

   stage('SonarQube Analysis') {
    steps {
        withSonarQubeEnv('sonarqube-server') {
            script {
                def scannerHome = tool name: 'SonarScanner',
                    type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                sh "${scannerHome}/bin/sonar-scanner"
            }
        }
    }
}

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .ci-venv
                    .ci-venv/bin/pip install -r services/product-service/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                dir('services/product-service') {
                    sh '../../.ci-venv/bin/python -m pytest -v'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shopsphere-product:latest services/product-service'
            }
        }
    }
}
