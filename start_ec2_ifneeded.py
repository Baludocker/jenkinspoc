import boto3
import os

def start_ec2_instances_by_tag(region, tag_key, tag_value):
    ec2 = boto3.client('ec2', region_name=region)

    filters = [
        {'Name': f'tag:{tag_key}', 'Values': [tag_value]}
    ]

    running_instances = ec2.describe_instances(Filters=filters,
                                               Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    running_ids = [instance['InstanceId'] for reservation in running_instances['Reservations'] for instance in reservation['Instances']]

    if not running_ids:
        print(f"No running instances found with tag {tag_key}:{tag_value}. Checking for stopped instances...")
        stopped_instances = ec2.describe_instances(Filters=filters,
                                                   Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        stopped_ids = [instance['InstanceId'] for reservation in stopped_instances['Reservations'] for instance in reservation['Instances']]

        if stopped_ids:
            print(f"Found stopped instances: {stopped_ids}")
            ec2.start_instances(InstanceIds=stopped_ids)
            print(f"Successfully started instances: {stopped_ids}")
        else:
            print(f"No stopped instances found with tag {tag_key}:{tag_value}.")
    else:
        print(f"Found running instances with tag {tag_key}:{tag_value}: {running_ids}")

if __name__ == "__main__":
    aws_region = os.environ.get('AWS_REGION')
    project_tag_key = os.environ.get('PROJECT_TAG_KEY')
    project_tag_value = os.environ.get('PROJECT_TAG_VALUE')

    if not all([aws_region, project_tag_key, project_tag_value]):
        print("Error: AWS_REGION, PROJECT_TAG_KEY, and PROJECT_TAG_VALUE environment variables must be set.")
        exit(1)

    start_ec2_instances_by_tag(aws_region, project_tag_key, project_tag_value)
