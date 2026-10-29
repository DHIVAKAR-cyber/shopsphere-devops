
pipeline {
    agent any

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
                    sh 'which sonar-scanner'
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shopsphere-product:latest services/product-service'
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                    set -e

                    docker rm -f shopsphere-smoke-test || true

                    docker run -d \
                        --name shopsphere-smoke-test \
                        -p 5001:5000 \
                        shopsphere-product:latest

                    trap 'docker rm -f shopsphere-smoke-test >/dev/null 2>&1 || true' EXIT

                    for i in $(seq 1 15); do
                        if curl -fsS http://localhost:5001/health; then
                            echo "Container smoke test passed"
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Container smoke test failed"
                    docker logs shopsphere-smoke-test
                    exit 1
                '''
            }
        }
    }
}
