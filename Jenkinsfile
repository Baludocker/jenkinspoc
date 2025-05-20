pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm // Automatically checks out the repository
            }
        }
        stage('Execute Python Script') {
            steps {
                script {
                    def pythonScriptPath = 'start_ec2_if_needed.py' // Path relative to the repository root

                    // If your Python script requires environment variables:
                    withEnv(['AWS_REGION='ap-south-1, 'PROJECT_TAG_KEY=project', 'PROJECT_TAG_VALUE=analytics']) {
                        sh "python ${pythonScriptPath}"
                    }
                }
            }
        }
    }
}
