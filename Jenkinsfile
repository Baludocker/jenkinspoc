pipeline {
  agent any

  parameters {
    string(name: 'TAG_KEY', defaultValue: 'project', description: 'EC2 Tag Key')
    string(name: 'TAG_VALUE', defaultValue: 'analytics', description: 'EC2 Tag Value')
    string(name: 'AWS_REGION', defaultValue: 'ap-south-1', description: 'AWS Region')
  }

  // Define environment for AWS credentials within the context of 'withAWS'
  // No need for a global 'environment' block here for AWS related variables.

  stages {
    stage('Test AWS Credentials') {
      steps {
        // Use the withAWS step provided by the AWS SDK plugin
        // Replace 'my-aws-credentials' with the ID you gave your credentials
        withAWS(credentials: 'awsid', region: "${params.AWS_REGION}") {
          echo "AWS Region: ${params.AWS_REGION}"
          echo "Verifying AWS credentials using STS Get Caller Identity..."
          // The awscli might still be used here if not fully removed,
          // but the primary action will be through the plugin's steps.
          // This line is good for quick confirmation, but the plugin's steps are independent.
          sh 'aws sts get-caller-identity' // This will now use the PATH-fixed AWS CLI, or fail gracefully
        }
      }
    }

    stage('Start EC2 Instances via AWS Plugin') {
      steps {
        script {
          def tagKey = params.TAG_KEY
          def tagValue = params.TAG_VALUE
          def awsRegion = params.AWS_REGION

          echo "Looking for stopped EC2 instances with tag: ${tagKey}=${tagValue} in region: ${awsRegion}"

          // Use the withAWS step to bind credentials and region
          withAWS(credentials: 'my-aws-credentials', region: awsRegion) {
            // Describe instances using the EC2 client provided by the plugin
            // This is Groovy/Java code interacting directly with AWS SDK
            def reservations = ec2.describeInstances(
              filters: [
                [name: "tag:${tagKey}", values: [tagValue]],
                [name: "instance-state-name", values: ["stopped"]]
              ]
            ).reservations

            def instanceIdsToStart = []

            if (reservations) {
              reservations.each { reservation ->
                reservation.instances.each { instance ->
                  def instanceId = instance.instanceId
                  def instanceName = instance.tags.find { it.key == 'Name' }?.value ?: '<NoName>'
                  echo "Found stopped instance: ID=${instanceId}, Name=${instanceName}"
                  instanceIdsToStart.add(instanceId)
                }
              }
            } else {
              echo "No stopped EC2 instances found with tag: ${tagKey}=${tagValue} in region: ${awsRegion}"
            }

            if (instanceIdsToStart) {
              echo "Starting instances: ${instanceIdsToStart.join(', ')}..."
              ec2.startInstances(instanceIds: instanceIdsToStart)
              echo "Successfully initiated start for instances."
            } else {
              echo "No instances to start."
            }
          }
        }
      }
    }
  }

  post {
    failure {
      echo "Jenkins job failed. Check AWS credentials, tag values, or region. See build logs for details."
    }
    success {
      echo "Jenkins job completed successfully."
    }
  }
}
