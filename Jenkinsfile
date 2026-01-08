pipeline {
    agent any

    environment {
        IMAGE_NAME = "app_demo"
        IMAGE_TAG  = "latest"
        IMAGE      = "${env.IMAGE_NAME}:${env.IMAGE_TAG}"
        CONTAINER  = "app_demo"
        HOST_DATA  = "/home/ec2-user/data"
        CONTAINER_DATA = "/instance"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t "$IMAGE" .
                '''
            }
        }

        stage('Restart Application') {
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
    }
}