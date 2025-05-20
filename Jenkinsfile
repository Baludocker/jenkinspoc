pipeline {
  agent any

  parameters {
    string(name: 'TAG_KEY', defaultValue: 'project', description: 'EC2 Tag Key')
    string(name: 'TAG_VALUE', defaultValue: 'analytics', description: 'EC2 Tag Value')
    string(name: 'AWS_REGION', defaultValue: 'ap-south-1', description: 'AWS Region')
  }

  environment {
    AWS_REGION = "${params.AWS_REGION}"
  }

  stages {
    stage('Clone Repo') {
      steps {
        checkout scm
      }
    }

    stage('Start EC2 Instances') {
      steps {
        sh '''
          echo "Running start-ec2-needed.sh with parameters:"
          #echo "TAG_KEY=${TAG_KEY}, TAG_VALUE=${TAG_VALUE}, REGION=${AWS_REGION}"
          chmod +x  ./scripts/start-ec2-needed.sh
          ./scripts/start-ec2-needed.sh "${TAG_KEY}" "${TAG_VALUE}" "${AWS_REGION}"
        '''
      }
    }
  }

  post {
    failure {
      echo "Script failed. Check AWS credentials, tag values, or region."
    }
  }
}

