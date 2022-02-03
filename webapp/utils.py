'''
Created on 2020/06/29

@author: DXG
'''
import csv
import os 
import pandas
from django.core.files.storage import FileSystemStorage

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, "resources",'csv')
JSON_FOLDER = os.path.join(BASE_DIR, "resources",'json')

def convert_file_csv_to_other(data_list,data_new):
    new_list= []
    news_list = []
    for x in data_list:
        for y in data_new:
            if x[1] == y[1]:
                new_list= x
                new_list.append(y[0])
                new_list.append(y[2])
        news_list.append(new_list)                                                 
    with open(CSV_FOLDER + '/' + 'convert_file.csv', mode='w' ,encoding="utf-8_sig" ,newline='') as csv_file:
        fieldnames=['HANEI_DATE', 'SEI_NM','MEI_NM','ID_NO' ,'PRIORITY_MAILADDRESS', 'SHAIN_HAKEN_KBN','GROUP_ID','JINJI_SHOKUI_CD2',
                    'SEI_NMK','MEI_NMK',
                    'SEI_MCC_NME',
                    'MEI_MCC_NME',
                    'SEI_NME',
                    'MEI_NME',
                    'INTERNET_SUB_DOMAIN',
                    'SHINSEI_USER_ID','SHINSEI_SEIMEI_NM','SHONIN_USER_ID','SHONIN_SEIMEI_NM','SHINSEI_KAISHA_CD']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
        for obj in news_list:
            writer.writerow({'HANEI_DATE': '', 'SEI_NM': obj[7] , 'MEI_NM' : obj[8] ,
                             'ID_NO': 'OA' + obj[1],'PRIORITY_MAILADDRESS' : obj[28],
                             'SHAIN_HAKEN_KBN' : 3,
                             'GROUP_ID' : ';'.join([str(x) for x in obj[35]]),
                             'JINJI_SHOKUI_CD2' : ';'.join([i for i in obj[36]]),
                             'SEI_NMK' : 1,
                             'MEI_NMK' : 1,
                             'SEI_MCC_NME': '' ,
                             'MEI_MCC_NME': '' ,'SEI_NME': '' ,'MEI_NME': '' ,'INTERNET_SUB_DOMAIN': '' ,
                             'SHINSEI_USER_ID': '' ,'SHINSEI_SEIMEI_NM': '' ,'SHONIN_USER_ID': '' ,'SHONIN_SEIMEI_NM': '' ,
                             'SHINSEI_KAISHA_CD':  1
                             })

def check_nan_data(item):
    if pandas.isna(item) == True:
        item = ''
    return item  
  
def write_user_csv(data_list,data_user):
    news_list = []
    for x in data_list:
        for y in data_user:
            if x[3] == y[3]:
                x[0] = y[0]
                x[5] = y[5]
                x[19] = ''
        news_list.append(x)                                                                     
    with open(CSV_FOLDER + '/' + 'new_file.csv', mode='w' ,encoding="utf-8_sig" ,newline='') as csv_file:
        fieldnames=['HANEI_DATE', 'SEI_NM','MEI_NM','ID_NO' ,'PRIORITY_MAILADDRESS', 'SHAIN_HAKEN_KBN','GROUP_ID','JINJI_SHOKUI_CD2',
                    'SEI_NMK','MEI_NMK',
                    'SEI_MCC_NME',
                    'MEI_MCC_NME',
                    'SEI_NME',
                    'MEI_NME',
                    'INTERNET_SUB_DOMAIN',
                    'SHINSEI_USER_ID','SHINSEI_SEIMEI_NM','SHONIN_USER_ID','SHONIN_SEIMEI_NM','SHINSEI_KAISHA_CD','NEW_COL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
        for obj in news_list:
            writer.writerow({'HANEI_DATE': check_nan_data(obj[0]), 'SEI_NM': obj[1] , 'MEI_NM' : obj[2] ,
                             'ID_NO': obj[3],'PRIORITY_MAILADDRESS' : obj[4],
                             'SHAIN_HAKEN_KBN' : obj[5],
                             'GROUP_ID' :check_nan_data(obj[6]) ,
                             'JINJI_SHOKUI_CD2' : check_nan_data(obj[7]),
                             'SEI_NMK' : check_nan_data(obj[8]),
                             'MEI_NMK' : check_nan_data(obj[9]),
                             'SEI_MCC_NME': check_nan_data(obj[10]) ,
                             'MEI_MCC_NME': check_nan_data(obj[11]) ,'SEI_NME': '' ,'MEI_NME': '' ,'INTERNET_SUB_DOMAIN': '' ,
                             'SHINSEI_USER_ID': '' ,'SHINSEI_SEIMEI_NM': '' ,'SHONIN_USER_ID': '' ,'SHONIN_SEIMEI_NM': '' ,
                             'SHINSEI_KAISHA_CD':  check_nan_data(obj[19]),
                             'NEW_COL' : ''
                             })
                 
def read_data_csv(list_table):
    temp_dict = {}
    for x in list_table:
        if x[1] in temp_dict:
            temp_dict[x[1]][0].append(x[0])
        else:
            temp_dict[x[1]] = [[x[0]], x[1]]
    
    news_list = []
    for s in list(temp_dict.values()):
        new_list = []
        sokui_cd2_list=[]
        for i in list_table:
            if s[1] == i[1] and i[2] != '00' and pandas.isna(i[2]) == False:
                for a in s[0]:
                    sokui = ''
                    if a == i[0]:
                        sokui= str(i[2]) + '(' +str(i[0])+ ')'
                        sokui_cd2_list.append(sokui)
        new_list.append(s[0])
        new_list.append(s[1])   
        new_list.append(sokui_cd2_list)   
        news_list.append(new_list)                              
    return news_list     


def read_data_shozoku():
    df = pandas.read_csv(CSV_FOLDER + '/' + '70B.csv',usecols=[1,3,23],dtype={'OA_NO': str})
    data = df.values.tolist()
    return data
def read_data_people():
    df = pandas.read_csv(CSV_FOLDER + '/' + '70A.csv',dtype={'ID_NO': str})
    data = df.values.tolist()
    return data
def read_data_user():
    df = pandas.read_csv(CSV_FOLDER + '/' + 'use.csv',encoding = "ISO-8859-1", engine='python')
    data = df.values.tolist()
    return data   
def read_convert_file ():
    df = pandas.read_csv(CSV_FOLDER + '/' + 'convert_file.csv')
    data = df.values.tolist()
    return data 

def save_file(filename,file):
    new_file_name = filename[0:3]
    filename = new_file_name+'.csv'
    fs = FileSystemStorage()
    if fs.exists(filename) == True:
        fs.delete(filename)                 
    f = fs.save(filename, file)
    fileurl = fs.url(f)

