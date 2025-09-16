pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'mlops-471720'
        GCLOUD_PATH = '/usr/bin'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[
                        url: 'https://github.com/rhythmparashar/MlOps-Hotel.git', 
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh """
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                """
            }
        }

        stage('Build and Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR...'
                        sh """
                            export PATH=${GCLOUD_PATH}:\$PATH
                            gcloud auth activate-service-account --key-file=\$GOOGLE_APPLICATION_CREDENTIALS
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Google Cloud Run...'
                        sh """
                            export PATH=${GCLOUD_PATH}:\$PATH
                            gcloud auth activate-service-account --key-file=\$GOOGLE_APPLICATION_CREDENTIALS
                            gcloud config set project ${GCP_PROJECT}

                            gcloud run deploy ml-project \
                                --image gcr.io/${GCP_PROJECT}/ml-project:latest \
                                --platform managed \
                                --region asia-south1 \
                                --allow-unauthenticated
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
