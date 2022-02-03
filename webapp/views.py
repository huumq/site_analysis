from django.shortcuts import render
from webapp.services import watson_discovery
from webapp.services import excel_reader_services
import csv
import os 
from django.http import HttpResponse
import pandas
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
import base64
import codecs
import json
from django.http.response import JsonResponse

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, "resources",'csv')
def index(request):
    return render(request, 'webapp/index.html')

def analysis_data(request):
    if "GET" == request.method:
        return render(request, 'webapp/analysis.html')
    else:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_url = fs.url(filename)
        excel_data_df = pandas.read_excel(excel_file, sheet_name='longlist')
        excel_website_list = excel_data_df['Website'].tolist()
        excel_website_list = [x for x in excel_website_list if str(x) != 'nan']
        list_data = []
        list_data = excel_reader_services.run_thread(excel_website_list)
        print(list_data)
        write_csv_url_check(list_data)
        with open(CSV_FOLDER + '/' + 'check_url.csv',encoding="utf-8_sig" ,newline='') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=check_url.csv'
        return response
        
def search_data(request):
    collections = watson_discovery.get_collections()
    if request.method == 'GET':
        return render(request, 'webapp/search.html' ,{'collections': collections} )
    if request.method == 'POST':
        print(request.POST["language"])
        language = request.POST["language"]
        if language == "Language":
            language = 'news-ja' 
        search = request.POST["search"]
        data = watson_discovery.search_news(language,search,50)
        return render(request, 'webapp/search.html' ,
                       {'data' : data.result['results'] ,
                        'collections': collections ,
                        'language' : language ,
                        'search' : search,
                        'matching_results' : data.result['matching_results']})

def trending_topic(request):
    data = watson_discovery.trending_news()
    return render(request, 'webapp/trending.html',{'data' : data.result['results']})

def export_csv(request):
    data,matching_results = watson_discovery.search_news_tesla()
    write_csv_file(data,matching_results)
    with open(CSV_FOLDER + '/' + 'data.csv',encoding="utf-8_sig" ,newline='') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'
    return response
    
def export_csv_news(request):
    data,matching_results = watson_discovery.search_news_to_csv(request.POST["search"])
    write_csv_file(data,matching_results)
    with open(CSV_FOLDER + '/' + 'data.csv',encoding="utf-8_sig" ,newline='') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'
    return response    
    
def write_csv_url_check(data):
    with open(CSV_FOLDER + '/' + 'check_url.csv', mode='w' ,encoding="utf-8_sig" ,newline='') as csv_file:
        fieldnames =['url' , 'working']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for _, obj in data.items():
            writer.writerow({'url' : obj['url'] , 'working' : obj['accessible']})
            
def write_csv_file(data,matching_results):
    with open(CSV_FOLDER + '/' + 'data.csv', mode='w' ,encoding="utf-8_sig" ,newline='') as csv_file:
        fieldnames = ['matching_results','id', 'publication_date', 'text' , 'title','enriched_text.relations.type',
                      'enriched_text.relations.sentence',
                      'enriched_text.relations.score',
                      'enriched_text.relations.arguments.0.location.0',
                      'enriched_text.relations.arguments.0.location.1',
                      'enriched_text.relations.arguments.0.entities.type',
                      'enriched_text.relations.arguments.0.entities.text',
                      'enriched_text.relations.arguments.1.location.0',
                      'enriched_text.relations.arguments.1.location.1',
                      'enriched_text.relations.arguments.1.entities.type',
                      'enriched_text.relations.arguments.1.entities.text'
                      ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for obj in data:
            for item in obj['data']:
                if 'enriched_text' in item and 'relations' in item['enriched_text']:
                    for relation in item['enriched_text']['relations']:
                        writer.writerow({'matching_results' :matching_results ,'id': item['id'], 'publication_date': item['publication_date'], 'text': item['text'] , 'title' : item['title'],
                                         'enriched_text.relations.type' : relation['type'],
                                         'enriched_text.relations.sentence' :relation['sentence'],
                                         'enriched_text.relations.score' : relation['score'] ,
                                         'enriched_text.relations.arguments.0.location.0' : relation['arguments'][0]['location'][0],
                                         'enriched_text.relations.arguments.0.location.0' : relation['arguments'][0]['location'][1],
                                         'enriched_text.relations.arguments.0.entities.type' : relation['arguments'][0]['entities'][0]['type'],
                                         'enriched_text.relations.arguments.0.entities.text' : relation['arguments'][0]['entities'][0]['text'] ,
                                         'enriched_text.relations.arguments.1.location.0' : relation['arguments'][1]['location'][0] ,
                                         'enriched_text.relations.arguments.1.location.1' : relation['arguments'][1]['location'][1] ,
                                         'enriched_text.relations.arguments.1.entities.type' : relation['arguments'][1]['entities'][0]['type'],
                                         'enriched_text.relations.arguments.1.entities.text' : relation['arguments'][1]['entities'][0]['text']})

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
                    'SHINSEI_USER_ID','SHINSEI_SEIMEI_NM','SHONIN_USER_ID','SHONIN_SEIMEI_NM','SHINSEI_KAISHA_CD','BIKOU']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
#         writer.writeheader()
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
                             'SHINSEI_KAISHA_CD':  1, 'BIKOU': ''
                             })

def check_nan_data(item):
    if pandas.isna(item) == True:
        item = ''
    return item  
  
def write_user_csv(data_list,data_user):
    news_list = []
    news_list_added = []
    news_list_deleted = []
    data_user_ids = [row[3] for row in data_user]
    for x in data_list:
        for y in data_user:
            if x[3] == y[3]:
                if y[20] == "modified":
                    for i in range(0,21):
                        x[i] = y[i]
                else:
                    x[0] = y[0]
                    x[5] = y[5]
                    x[19] = ''
                    x[20] = y[20]
        if x[3] in data_user_ids:
            news_list.append(x)
            data_user_ids.remove(x[3])
        else:
            news_list_added.append(x)
    
    for user in data_user: 
        if user[3] in data_user_ids:
            new_data = ["" for _ in range(len(data_list[0]))]
            for i in range(0,21):
                new_data[i] = user[i]
            news_list_deleted.append(new_data)
    write_data_to_csv('new_file1.csv', data_list)
    write_data_to_csv('new_file.csv', news_list)
    write_data_to_csv('new_file_added.csv', news_list_added)
    write_data_to_csv('new_file_deleted.csv', news_list_deleted)
    

def write_data_to_csv(file_name, data_list):
    with open(CSV_FOLDER + '/' + file_name, mode='w' ,encoding="utf-8_sig" ,newline='') as csv_file:
        fieldnames=['HANEI_DATE', 'SEI_NM','MEI_NM','ID_NO' ,'PRIORITY_MAILADDRESS', 'SHAIN_HAKEN_KBN','GROUP_ID','JINJI_SHOKUI_CD2',
                    'SEI_NMK','MEI_NMK',
                    'SEI_MCC_NME',
                    'MEI_MCC_NME',
                    'SEI_NME',
                    'MEI_NME',
                    'INTERNET_SUB_DOMAIN',
                    'SHINSEI_USER_ID','SHINSEI_SEIMEI_NM','SHONIN_USER_ID','SHONIN_SEIMEI_NM','SHINSEI_KAISHA_CD','BIKOU']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
#         writer.writeheader()
        for obj in data_list:
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
                             'BIKOU' : check_nan_data(obj[20])
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

def convert_csv_to_other(request):
    if "GET" == request.method:
        return render(request, 'webapp/convert_csv.html')
    else:
        list_table=[]
        csv_file = request.FILES['csv_file']
        df = pandas.read_csv(csv_file,header=None, skiprows=[0])
        list_table = df.values.tolist()
        data_new =read_data_csv() 
        convert_file_csv_to_other(list_table,data_new)
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = fs.url(filename)
        with open(CSV_FOLDER + '/' + 'convert_file.csv',encoding="utf-8_sig" ,newline='') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=convert_file.csv'
        return response


def read_data_shozoku():
    data = []
    for file in os.listdir(CSV_FOLDER):
        if file.startswith("70B") and file.endswith(".csv"):
            df = pandas.read_csv(os.path.join(CSV_FOLDER, file),usecols=[1,3,23],dtype={'OA_NO': str})
            data = df.values.tolist()
            break
    return data

def read_data_people():
    data = []
    file = ""
    for file in os.listdir(CSV_FOLDER):
        if file.startswith("70A") and file.endswith(".csv"):
            df = pandas.read_csv(os.path.join(CSV_FOLDER, file),dtype={'ID_NO': str})
            data = df.values.tolist()
            break
    return file, data

def read_data_user():
    data = []
    for file in os.listdir(CSV_FOLDER):
        if file.startswith("user") and file.endswith(".csv"):
            with codecs.open(os.path.join(CSV_FOLDER, file), mode='r', encoding='shift-jis') as file:
                lines = file.read()
            with codecs.open(os.path.join(CSV_FOLDER, "user_temp.csv"), mode='w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line)
            df = pandas.read_csv(os.path.join(CSV_FOLDER, "user_temp.csv"), dtype=str)
            data = df.values.tolist()
            break
    return data
  
def read_convert_file ():
    df = pandas.read_csv(CSV_FOLDER + '/' + 'convert_file.csv')
    data = df.values.tolist()
    return data 

def save_file(filename,file):
    if filename.startswith("70A"):
        for file_in_dir in os.listdir(CSV_FOLDER):
            if file_in_dir.startswith("70A"):
                os.remove(os.path.join(CSV_FOLDER, file_in_dir))
    if filename.startswith("70B"):
        for file_in_dir in os.listdir(CSV_FOLDER):
            if file_in_dir.startswith("70B"):
                os.remove(os.path.join(CSV_FOLDER, file_in_dir))
    if filename.startswith("user"):
        for file_in_dir in os.listdir(CSV_FOLDER):
            if file_in_dir.startswith("user"):
                os.remove(os.path.join(CSV_FOLDER, file_in_dir))
    fs = FileSystemStorage(CSV_FOLDER)
    if fs.exists(filename) == True:
        fs.delete(filename)       
    print(filename)          
    _ = fs.save(filename, file)
    
def convert_csv_to_other_new(request):
    if "GET" == request.method:
        return render(request, 'webapp/convert_csv_new.html')
    else:
        data_new = []
        data_shozoku = []
        data_people = []
        data_user = []
        for key in request.FILES:
            try:
                print("request.FILES[key].name")
                print(request.FILES[key].name)
                save_file(request.FILES[key].name,request.FILES[key])
            except ValueError:
                pass
        file_name, data_people = read_data_people()
        data_shozoku = read_data_shozoku()
        data_new = read_data_csv(data_shozoku)
        data_user = read_data_user()
                           
        convert_file_csv_to_other(data_people,data_new)
        data_list = read_convert_file();
        write_user_csv(data_list,data_user)
        new_file_name = os.path.splitext(file_name)[0] + "_converted"
        
        with ZipFile(os.path.join(CSV_FOLDER, new_file_name + '.zip'), 'w') as myzip:
            myzip.write(os.path.join(CSV_FOLDER, "new_file.csv"), new_file_name + ".csv")
            myzip.write(os.path.join(CSV_FOLDER, "new_file_added.csv"), new_file_name +  "_added.csv")
            myzip.write(os.path.join(CSV_FOLDER, "new_file_deleted.csv"), new_file_name + "_deleted.csv")
        
        with open(os.path.join(CSV_FOLDER,new_file_name + '.zip'), "rb") as f:
            bytes_data = f.read()
            encode_string = base64.b64encode(bytes_data).decode("utf-8")
        serialized_q = json.dumps({"file_name": new_file_name + '.zip', "data": encode_string}, ensure_ascii=False)
        return JsonResponse(serialized_q, safe=False)
            