pipeline {
    agent any

    environment {
        IMAGE_NAME = "app_demo"
        IMAGE_TAG  = "latest"
        IMAGE      = "${env.IMAGE_NAME}:${env.IMAGE_TAG}"
        CONTAINER  = "app_demo"
        HOST_DATA  = "/var/lib/app_demo"
        CONTAINER_DATA = "/app/instance"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install pytest
                    export PYTHONPATH=.
                    pytest
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t "$IMAGE" .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    if [ "$(docker ps -aq -f name=^/${CONTAINER}$)" ]; then
                        docker stop ${CONTAINER} || true
                        docker rm ${CONTAINER} || true
                    fi

                    docker run -d \
                      --name ${CONTAINER} \
                      -v ${HOST_DATA}:${CONTAINER_DATA} \
                      -p 8090:8090 \
                      --restart unless-stopped \
                      ${IMAGE}
                '''
            }
        }
    }

    post {
        success {
            echo "Depliegue completo: ${IMAGE}"
        }
        
        failure {
            echo "Despliegue fallido"
        }

        always {
            sh 'rm -rf venv'
        }
    }
}