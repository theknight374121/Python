'''
Created on 19-Jan-2016

@author: Amey Patil
'''
import sqlite3

def sql_Execute(conn,query,*params):
    '''
        sql_Execute(sql query,*paramerters)
        
        This function executes the query in the database.
    '''
    dbo=conn.cursor()
    if len(params)>0:
        #print("Query executed!")
        return dbo.execute(query,params)
    else:
        return dbo.execute(query)
    
    
    
def insert_Into(conn,table_name, items, values):
    '''
        insert_Into( table_name, columns of table, values to set)
                    
        This function takes 3 parameters as input, out of which initial two only need to be calculated once.
        items= columns of table in order
        values= tuple containing the values to be stored.
    '''
    dbo=conn.cursor()
    query="INSERT INTO {} {} VALUES {}".format(table_name, items, values)
    
    dbo.execute(query) #Executing the query
    conn.commit()
    #print("Values Inserted!")
    
def update(conn,table_name,set_dict,where_dict):
    '''
        update(table_name, dict_to_set_values, dict_where_value)
        
        This fucntion takes 3 inputs,
        table_name = name of the table
        set_dict = dict that contains values to set
        where_dict = dict that contains the where string from the query
    '''
    dbo=conn.cursor()
    #generating the update query
    set_string=''
    where_string=''
    for items in set_dict:
        set_string+=" "+str(items)+"='{}'".format(set_dict[items])+","
    set_string=set_string[:-1] #to get rid of the last comma in the query
    for items in where_dict:
        where_string=str(items)+"='{}'".format(where_dict[items])
    query="UPDATE {} SET".format(table_name)+set_string+" WHERE "+where_string
    print(query)
    
    #executing the update query
    dbo.execute(query)
    conn.commit()
    #print("Values Updated!")
    
def delete(conn,table_name, dict_obj):
    '''
        delete(table_name, dict_obj)
        
        This function has two parameters,
        dict_obj= the dict obj that gives the condition from where to delete.
    '''
    dbo=conn.cursor()
    for items in dict_obj:
        dict_string="{}='{}'".format(items,dict_obj[items])
    query="DELETE FROM {} WHERE ".format(table_name)+dict_string
            
    #Executing the query
    dbo.execute(query)
    conn.commit()
    #print("Values Deleted!")

def display_table(conn,table_name):
    dbo=conn.cursor()
    query="SELECT * FROM {}".format(table_name)
    row = dbo.execute(query)
    for line in row:
        print(line)
        
           
def close(conn):
    dbo=conn.cursor()
    dbo.close()
 
def main():
    
    conn = sqlite3.connect('test')
        
    print("Database Created and Initialized!") 
    
    #initialize() #creating the database
    sql_Execute(conn,"DROP TABLE if EXISTS test")
    sql_Execute(conn,"CREATE TABLE test (id,pwd,name,age)")
    
    items='(id,pwd,name,age)'
    insert_Into(conn,'test', items, "('sensei','patil','amey',22)")
    insert_Into(conn,'test', items, "('usp','patel','urvi',22)")
    insert_Into(conn,'test', items, "('noob','neel','gala',22)")
    display_table(conn,"test")
    set_dict=dict(
                  id='theknight',
                  age=21
    )
    where_dict=dict(
                    name='amey'
                    )
    update(conn,'test', set_dict, where_dict)
    
    display_table(conn,"test")
    delete(conn,'test', dict(name='gala'))
    display_table(conn,'test')
    
    close(conn) #closing the database connection
    
    
if __name__=='__main__':
    main()