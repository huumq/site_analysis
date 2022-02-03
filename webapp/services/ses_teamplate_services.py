'''
Created on 2020/09/02

@author: DXG
'''
import boto3

ses = boto3.client('ses')
def create_template(ses,template_name,subject,text_content,html_content):
    response = ses.create_template(
      Template = {
        'TemplateName' : template_name,
        'SubjectPart'  : subject,
        'TextPart'     : text_content,
        'HtmlPart'     : html_content
      }
      )
    return response

def get_template(ses,template_name):   
    response = ses.get_template(
      TemplateName = template_name
    )
    return response 

def get_list_templates(ses,max_item):
    response = ses.list_templates(
      MaxItems=max_item
    )
    return response

def update_template(ses,template_name,subject,text_content,html_content):
    response = ses.update_template(
      Template={
        'TemplateName': template_name,
        'SubjectPart' : subject,
        'TextPart'    : text_content,
        'HtmlPart'    : html_content
      }
    )
    return response

def send_templated_email(ses,email_address,template_name):
    response = ses.send_templated_email(
      Source=email_address,
      Destination={
        'ToAddresses': [
          email_address,
        ],
        'CcAddresses': [
          email_address,
        ]
      },
      ReplyToAddresses=[
        email_address,
      ],
      Template=template_name,
      TemplateData='{ \"REPLACEMENT_TAG_NAME\":\"REPLACEMENT_VALUE\" }'
    )
    return response