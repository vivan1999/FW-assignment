#!/usr/bin/env python
# coding: utf-8

# In[8]:


import threading
import json
from threading import*
import time
from argparse import ArgumentParser
from os import path,makedirs


# Creates a directory recursively.
def create_folder(file_path):
    try:
        makedirs(file_path, mode=0o777, exist_ok=True)
    except PermissionError:
        return False
    return True



DEFAULT_DB_PATH='C:\\Users\\hp\\Desktop\\CRD\\New DATABASE'
DEFAULT_DB_NAME='database.json'
db_path=DEFAULT_DB_PATH


# Create a datastore directory.
directory_created = create_folder(db_path)
if not directory_created:
    print(f"Permission denied: You can not create the directory `{db_path}`.\n")
    exit(0)


datastore = path.join(db_path, DEFAULT_DB_NAME)
data={}
#for create operation 
#use syntax "create(key_name,value,timeout_value)" timeout is optional you can continue by passing two arguments without timeout

def create(key,value,timeout=0):
    if path.isfile(datastore):
        with open(datastore,'r+',encoding='utf-8-sig') as f:
            try:
                data=json.load(f)
                if key in data:
                    print("error: this key already exists") #error message1
                else:
                    if(key.isalpha()):
                        if len(data)<(1024*1024*1024) and value<=(16*1024*1024): #constraints for file size less than 1GB and Jasonobject value less than 16KB
                            if timeout==0:
                                l=[value,timeout]
                            else:
                                l=[value,time.time()+timeout]
                                if len(key)<=32:
                                    data[key]=l
                                    with open(datastore,'w+') as f:
                                        json.dump(data,f)
                        else:
                            print("error: Memory limit exceeded!! ")#error message2
                    else:
                         print("error: Invalid key_name!! key_name must contain only alphabets and no special characters or numbers")#error message3
            except json.decoder.JSONDecodeError:
                print("json file error")
    
    
#for read operation
#use syntax "read(key_name)"
            
def read(key):
    with open(datastore,'r+',encoding='utf-8-sig') as f:
        try:
            data=json.load(f)
            if key not in data:
                print("error: given key does not exist in database. Please enter a valid key") #error message4
            else:
                b=data[key]
                if b[1]!=0:
                    if time.time()<b[1]: #comparing the present time with expiry time
                        stri=str(key)+":"+str(b[0]) #to return the value in the format of JasonObject i.e.,"key_name:value"
                        return stri
                    else:
                        print("error: time-to-live of",key,"has expired") #error message5
                else:
                    stri=str(key)+":"+str(b[0])
                    return stri
        except json.decoder.JSONDecodeError:
            print("no data stored")
#for delete operation
#use syntax "delete(key_name)"

def delete(key):
    with open(datastore,'r+',encoding='utf-8-sig') as f:
        try:
            data=json.load(f)
        except json.decoder.JSONDecodeError:
            pass
    if key not in data:
        print("error: given key does not exist in database. Please enter a valid key") #error message4
    else:
        b=data[key]
        if b[1]!=0:
            if time.time()<b[1]: #comparing the current time with expiry time
                del data[key]
                print("key is successfully deleted")
            else:
                print("error: time-to-live of",key,"has expired") #error message5
        else:
            del data[key]
            print("key is successfully deleted")

#I have an additional operation of modify in order to change the value of key before its expiry time if provided

#for modify operation 
#use syntax "modify(key_name,new_value)"

def modify(key,value):
    with open(datastore,'r+',encoding='utf-8-sig') as f:
        try:
            data=json.load(f)
        except json.decoder.JSONDecodeError:
            pass
    b=data[key]
    if b[1]!=0:
        if time.time()<b[1]:
            if key not in data:
                print("error: given key does not exist in database. Please enter a valid key") #error message6
            else:
                l=[]
                l.append(value)
                l.append(b[1])
                data[key]=l
        else:
            print("error: time-to-live of",key,"has expired") #error message5
    else:
        if key not in data:
            print("error: given key does not exist in database. Please enter a valid key") #error message6
        else:
            l=[]
            l.append(value)
            l.append(b[1])
            data[key]=l


# In[ ]:





# In[ ]:




