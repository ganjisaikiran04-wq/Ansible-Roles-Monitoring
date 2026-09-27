###Event bridge AWS events json##
{
  "source": [
    "aws.autoscaling"
  ],
  "detail-type": [
    "EC2 Instance Launch Successful"
  ],
  "detail": {
    "AutoScalingGroupName": [
      "monitoring-node-asg"
    ]
  }
}

##Add these permissions to the Lambda execution role:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:SendCommand"
      ],
      "Resource": "*"
    }
  ]
}

#####lambda_function.py code####import json


import json
import boto3
import time
import ipaddress

REGION = "us-east-1"

# Replace this with your Ansible master EC2 instance ID
ANSIBLE_MASTER_INSTANCE_ID = "i-REPLACE_WITH_MASTER_INSTANCE_ID"

PROJECT_DIR = "/root/Ansible-Roles-Monitoring"
SSH_KEY = "/root/.ssh/ansible.key"

ec2 = boto3.client("ec2", region_name=REGION)
ssm = boto3.client("ssm", region_name=REGION)


def lambda_handler(event, context):
    print("Received EventBridge event:")
    print(json.dumps(event))

    # Get the newly launched ASG instance ID
    instance_id = event.get("detail", {}).get("EC2InstanceId")

    if not instance_id:
        raise ValueError("EC2InstanceId not found in EventBridge event")

    # Get the private IP of the new EC2 instance
    response = ec2.describe_instances(
        InstanceIds=[instance_id]
    )

    reservations = response.get("Reservations", [])
    if not reservations or not reservations[0].get("Instances"):
        raise ValueError(f"Instance not found: {instance_id}")

    instance = reservations[0]["Instances"][0]
    private_ip = instance.get("PrivateIpAddress")

    if not private_ip:
        raise ValueError(f"Private IP not available for {instance_id}")

    # Validate the IP before using it in the Ansible command
    private_ip = str(ipaddress.ip_address(private_ip))

    print(f"New ASG instance: {instance_id}")
    print(f"Private IP: {private_ip}")

    # Wait briefly for SSH to become available
    command = f"""
    set -e
    cd {PROJECT_DIR}

    for attempt in $(seq 1 10); do
      if ssh -o BatchMode=yes \
             -o ConnectTimeout=5 \
             -o StrictHostKeyChecking=no \
             -i {SSH_KEY} ubuntu@{private_ip} 'echo SSH_OK'; then
        break
      fi
      echo "Waiting for SSH: attempt $attempt"
      sleep 15
    done

    ansible-playbook \
      -i '{private_ip},' \
      -u ubuntu \
      --private-key {SSH_KEY} \
      {PROJECT_DIR}/asg-node-exporter.yml
    """

    # Run the command on the Ansible master using SSM
    result = ssm.send_command(
        InstanceIds=[ANSIBLE_MASTER_INSTANCE_ID],
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": [command],
            "executionTimeout": ["900"]
        },
        Comment=f"Install Node Exporter on ASG instance {instance_id}"
    )

    command_id = result["Command"]["CommandId"]

    print(f"SSM command submitted: {command_id}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Ansible command submitted to master",
            "instance_id": instance_id,
            "private_ip": private_ip,
            "ssm_command_id": command_id
        })
    }


######lambda function test code######
{
  "version": "0",
  "id": "test-event-123",
  "detail-type": "EC2 Instance Launch Successful",
  "source": "aws.autoscaling",
  "account": "123456789012",
  "time": "2026-09-26T18:00:00Z",
  "region": "us-east-1",
  "resources": [],
  "detail": {
    "AutoScalingGroupName": "monitoring-node-asg",
    "EC2InstanceId": "i-0123456789abcdef0"
  }
}
