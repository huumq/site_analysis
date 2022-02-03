'''
Created on 2020/10/05

@author: DXG
'''
# import the PostgreSQL adapter for Python

import psycopg2

def connect_to_postgresql (host,database,user,password,port):
    try:
        postgresConnection  = psycopg2.connect(host=host,
        database=database,
        user=user,
        password=password,
        port = port)
        return True,postgresConnection 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False,error
    
def create_tables(list_table):
    postgresConnection  = psycopg2.connect(host="127.0.0.1",
    database="mchc",
    user="postgres",
    password="Lu@nnq1910"
    )
    cursor  = postgresConnection.cursor()
    # Create table statement
    for table in list_table:
        cols=''
        key = ''
        table_name = table["table_name"]
        for column in table['columns']:
            data_type = ""
            if column["data_type"] == "text" or column["data_type"] == "int":
                data_type = column["data_type"]
            else:
                data_type = column["data_type"]+"("+str(column["type"]) +")"    
            cols += column["column_name"] + " " + data_type  +","
        for column in table['columns']:
            if column["key"] == "○":
                key +=column["column_name"] +","
        sqlCreateTable = "CREATE TABLE " + table_name + "(" + cols + "PRIMARY KEY" + "("+key.rstrip(',')+")" +")"  
        cursor.execute(sqlCreateTable)
        postgresConnection.commit()
        print(sqlCreateTable)

def create_index(list_table): 
    postgresConnection   = psycopg2.connect(host="127.0.0.1",
    database="mchc",
    user="postgres",
    password="Lu@nnq1910")
    cursor  = postgresConnection.cursor()
    # Create table statement
    for table in list_table:
        index_name=''
        index_column = ''
        table_name = table["table_name"]
        for column in table['columns']:
            if column["key"] == "○":
                index_column +=column["column_name"] +","
                index_name += column["column_name"] +"_"
        sqlCreateIndex = "CREATE INDEX " + table_name +"_"+index_name.rstrip('_') + " ON " + table_name +" USING btree " +"(" +index_column.rstrip(',') + ")"
        cursor.execute(sqlCreateIndex)
        postgresConnection.commit()
        print(sqlCreateIndex)
        
def copy_data(connection,file,table_name):
    f = open(file, "r", encoding="utf-8")
    postgresConnection  = psycopg2.connect(host=connection["host-name"],
    database=connection["db-name"],
    user=connection["user-name"],
    password=connection["password"],
    port = connection["port"])

    cursor  = postgresConnection.cursor()
    copy_sql = f"copy {table_name} from stdin  with csv HEADER delimiter E'\t' quote e'\x08'"
    try:
        cursor.copy_expert(copy_sql, f)
        postgresConnection.commit()
        cursor.close()
        postgresConnection.close()
    except psycopg2.Error as e:
        replace_file(file,e.pgerror)
        cursor.close()
        postgresConnection.close()
        copy_data(connection,file,table_name)    
    f.close()   

def get_line_number_error(error):
    errors_context = error.splitlines()[2]
    line_error = errors_context.split("line",1)[1]
    line_number = int(line_error[:2])-1
    return line_number

def replace_file(file,error):
    line = get_line_number_error(error)
    print(file)
    open_file = open(file,"r",encoding="utf-8")
    lines = open_file.readlines()
    print(len(lines))
    open_file.close()
    del lines[line]
    new_file = open(file, "w" ,encoding="utf-8") 
    for line in lines:
        new_file.write(line)
    new_file.close()
    
def replace_file2(file):  
    NUM_OF_LINES=40000
    with open(file) as fin:
        fout = open(file + "output0.txt","wb")
        for i,line in enumerate(fin):
          fout.write(line)
          if (i+1)%NUM_OF_LINES == 0:
            fout.close()
            fout = open("output%d.txt"%(i/NUM_OF_LINES+1),"wb")
        fout.close()
                                            