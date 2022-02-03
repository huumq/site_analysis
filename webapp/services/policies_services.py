'''
Created on 2020/09/02

@author: DXG
'''
import json
import boto3
iam = boto3.client('iam')

def create_policy(iam):
    my_managed_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "RESOURCE_ARN"
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": "RESOURCE_ARN"
        }
    ]
    }
    response = iam.create_policy(
      PolicyName='myDynamoDBPolicy',
      PolicyDocument=json.dumps(my_managed_policy)
    )
    return response


def get_policy(iam,policy_arn):
    response = iam.get_policy(
    PolicyArn=policy_arn
    )
    return response['Policy']


def attach_role_policy(iam,policy_arn,role_name):
    iam.attach_role_policy(
    PolicyArn=policy_arn,
    RoleName=role_name
)
    
def detach_role_policy(iam,policy_arn,role_name):   
    iam.detach_role_policy(
    PolicyArn=policy_arn,
    RoleName=role_name
) 