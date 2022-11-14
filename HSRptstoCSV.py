#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:27:47 2022

@author: aricaschuett
"""

# This scrapes the argriculture subcommitte Bills and puts them in a csv
import os
import pandas as pd
import numpy as np

# Folder Path
path = r"/Users/aricaschuett/Documents/Alex/Appropriation Txt Files/House/Homeland_Security"
os.chdir(path)

# empty list to store files that we will read
files = []


agency_name_fg = []
file_name_fg = []
provision_fg = []
#directory = []
#directory = os.listdir()
file_name =[]

for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        files.append(file)   
 
for file in files:
    f = open(file, "r")
    data = f.read()    
    
    
    # initializing sub string --- This cuts off the report after TITLE VII
    #sub_str_End = "GENERAL PROVISIONS"
    sub_str_End = "(INCLUDING RESCISSIONS AND TRANSFERS OF FUNDS)"

    re = data.split(sub_str_End)
    res_front =re[0]
    sub_str_Start ="TITLE I--DEPARTMENTAL MANAGEMENT, OPERATIONS, INTELLIGENCE, AND"
        
    re = res_front.split(sub_str_Start)  


    rept_body_dirty=re[1]      # 1:4 is hardcoded I may need to modify this

    re_str = ""
    re_str = ''.join(map(str, rept_body_dirty))
    
    import re
    re_str_no_lnbrk = rept_body_dirty.replace('\n', '')
    
    your_string = re_str_no_lnbrk
    
    #regex= r'(\w*\,*\s\w*\s\w*\s\d*\.*\s*(\$|\+|\d)|\d*\,\d*\n\w*\s\w*(\,|\s)(\w*|\s)(\s|\:)(\w*|\s)(\t|\w*)|(Appropriation|year)(\s|\,)(\s|\w)(\,|\d*))'
    
    #result = re.sub(regex, '', your_string)#.replace('\n', '')
    #result = result.replace(',,', '')
    result = your_string.replace(',,', '')
    result = result.replace('Mission', 'Mission\n\n\n')
    result = result.replace('$,', '')
    result = result.replace('$', '')
   #result = result.replace(',,', '')
    
    re = result.replace(',,', '')
    sub_result_end = "\n"
    re = result.split(sub_result_end)
    re = pd.DataFrame(re, columns = ['Value'])
    re['Value'].replace("", np.nan, inplace = True)

    re = re.dropna()
        

    # Remove emtpy rows and rows that dont contain Mission
    #re = list(filter(None, re))
    #re = [k for k in re if 'Mission' in k] 


    split = "\n "
    text = []
    data_clean = ""
    provision = []
    agency = []

   # for i in re:
   #     text.append(i.split(split))

    text = re.values.tolist()
    
    for i in text:

        provision.append(i[0])

    prov_split = []
    agency_name =[]
    file_name =[]
   
    for i in provision:
        prov_split.append(i.split("."))

    for i in prov_split:
        agency_name.append(i[0])
        file_name.append(file)
    
    # these are lists of lists that are appended to with each document
    agency_name_fg.append(agency_name)
    file_name_fg.append(file_name)
    provision_fg.append(provision)


file_all = []
provision_all = []
agency_name_all = []

# this joins the lists within the lists and makes one list for each variable type (**implode**)
file_all = sum(file_name_fg, []) 
provision_all = sum(provision_fg, [])
agency_name_all = sum(agency_name_fg, [])
      

            
# create a df for each column    
provisionDF = pd.DataFrame(provision_all, columns = ['provision'])
agencyDF = pd.DataFrame(agency_name_all, columns = ['agency_name'])
fileDF = pd.DataFrame(file_all, columns = ['files'])
   
    
            
# join all the columns into one data frame
df_clean = pd.concat([fileDF, agencyDF,provisionDF], axis=1)

df_final = df_clean.dropna()
    
# write dataFrame to CSV file
df_final.to_csv("/Users/aricaschuett/Documents/Alex/HSRpt11-14-test4.csv")
    

  
