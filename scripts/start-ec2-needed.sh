#!/bin/bash
set -e

TAG_KEY="${TAG_KEY:-project}"
TAG_VALUE="${TAG_VALUE:-analytics}"
REGION="${AWS_REGION:-ap-south-1}"

echo "Looking for stopped EC2 instances with tag: $TAG_KEY=$TAG_VALUE in region: $REGION"

# Get instance ID and Name tag pairs for stopped instances matching the tag
aws ec2 describe-instances --region "$REGION" \
  --filters "Name=tag:$TAG_KEY,Values=$TAG_VALUE" "Name=instance-state-name,Values=stopped" \
  --query 'Reservations[*].Instances[*].[InstanceId, Tags[?Key==`Name`] | [0].Value]' \
  --output text | while read INSTANCE_ID NAME_TAG; do
    echo "Found stopped instance: ID=$INSTANCE_ID, Name=${NAME_TAG:-<NoName>}"
    echo "Starting instance $INSTANCE_ID..."
    aws ec2 start-instances --region "$REGION" --instance-ids "$INSTANCE_ID"
done

