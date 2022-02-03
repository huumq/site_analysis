'''
Created on 2020/09/01

@author: DXG
'''
import boto3

ses = boto3.client('ses')
def verify_email_identity(ses,email_adrress):    
    response = ses.verify_email_identity(
      EmailAddress = email_adrress
    )
    return response

def verify_domain_identity(ses,domain_name):
    response = ses.verify_domain_identity(
      Domain=domain_name
    )
    return response

def list_identities_address(ses,email_adrress,max_item):
    response = ses.list_identities(
      IdentityType = email_adrress,
      MaxItems=max_item
    )
    return response
    
def list_identities_domain(ses,domain_name, max_item):
    response = ses.list_identities(
      IdentityType = domain_name,
      MaxItems=max_item
    )
    return response

def delete_identity_address(ses,email_adrress):
    response = ses.delete_identity(
      Identity = email_adrress
    )
    return response


def delete_identity_domain(ses,domain_name):
    response = ses.delete_identity(
      Identity = domain_name
    )
    return response
    