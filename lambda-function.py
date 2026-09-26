###Event brudge AWS events json##
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

#####lambda_function.py code####import json

def lambda_handler(event, context):
    print("Event received:")
    print(json.dumps(event, indent=2))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "ASG launch event received successfully"
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
