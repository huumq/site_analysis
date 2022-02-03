'''
Created on 2020/08/31

@author: DXG
'''
import boto3
iam = boto3.client('iam')
def create_user(iam,user_name):
    response = iam.create_user(
    UserName=user_name
    )
    return response

def get_paginator_user(iam):
    list_user=[]
    paginator = iam.get_paginator('list_users')
    for response in paginator.paginate():
        list_user.append(response)
    return list_user

def update_user(iam,old_name,new_name):    
    iam.update_user(
    UserName=old_name,
    NewUserName=new_name
)
    
def delete_user(iam,username):
    iam.delete_user(
    UserName=username
    )   
def create_access_key(iam,user_name):
    response = iam.create_access_key(
    UserName=user_name
    )
    return response['AccessKey']

def delete_access_key(iam,access_key,user_name):
    iam.delete_access_key(
    AccessKeyId=access_key,
    UserName=user_name
)