'''
Created on 20-Jan-2016

@author: Amey
'''
import hashlib, sys, sqlite3
from getpass import getpass
from Login_Authentication.apDatabaseConnect import *


def authenticate(conn,table_name,login_id,pwd):
    dataset = sql_Execute(conn,"SELECT pwd FROM {} WHERE id='{}'".format(table_name,login_id))
    row = dataset.fetchone()
    if type(row)==type(None):
        print("No values exists. Signup first!")
        return
    else:
        db_pwd= row[0]
        input_pwd=hashlib.sha1(pwd.encode(encoding='utf_8')).hexdigest()
        print(input_pwd)
        if db_pwd==input_pwd:
            print("SUCCESSFUL LOGIN!!")
        else:
            print("Either login_id or password was wrong try again!")
    
def signup(conn,table_name,new_id,new_pwd):
    new_db_pwd=hashlib.sha1(new_pwd.encode(encoding='utf_8')).hexdigest()
    credentials=(new_id, new_db_pwd)
    query="INSERT INTO {} VALUES ".format(table_name)+str(credentials)
    sql_Execute(conn,query)
    
def idExists(conn,table_name,login_id):
    query="select COUNT(id) from users where id='{}'".format(login_id)
    dataset=sql_Execute(conn,query)
    row = dataset.fetchone()
    if type(row)==type(None):
        return False
    elif int(row[0])>0:
        return True
    else:
        return False

def main():
    #Connecting the database
    conn=sqlite3.connect('login.db')
    
    #creating the database
    sql_Execute(conn,"DROP TABLE IF EXISTS users")
    sql_Execute(conn,"CREATE TABLE users (id VARCHAR(25), pwd VARCHAR(40))");
    insert_Into(conn,'users','(id,pwd)','("amey","patil")')
    
    #MyLogin Program
    display_table(conn,'users')
    flag=True
    while(flag):
        print("1-Login\n2-Signup\n3-Exit\nChoose your option: ")
        choice=int(input())
        if choice==1:
            login_id= input("Enter your login id:")
            login_pwd= getpass("Enter your password")
            authenticate(conn, "users", login_id, login_pwd)
        elif choice==2:
            new_id=input("Enter your id:")
            new_pwd=getpass("Enter your password:")
            confirm_pwd=getpass("Enter your password:")
            if new_pwd==confirm_pwd:
                if idExists(conn,'users',new_id):
                    print("ID already exists. Please choose a new one.")
                    break
                else:
                    signup(conn, 'users', new_id, new_pwd)
            else:
                print("Passwords do not match. Try again.")
        elif choice==3:
            sys.exit(0)
        else:
            print("Expected input either 1, 2, or 3. Please try again.")
            
    #closing the database
    close(conn)
    
if __name__=="__main__": main()
