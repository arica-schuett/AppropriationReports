#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:30:01 2022

@author: aricaschuett
"""

import requests

from bs4 import BeautifulSoup


# I think I have to make a loop for all of these to read all the argriculture documents
# I have a loop that might work in AppropriationsScrape.py

r = requests.get('https://www.congress.gov/congressional-report/109th-congress/house-report/463/1')

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())

#print(soup.title)  # this will be useful

 

# Finding by id
s = soup.find('div', id= 'container')

data = s.find('div', {"class": "main-wrapper"})

data_str = str(data)
# initializing sub string --- This cuts off the report after TITLE VII
sub_str_End = "TITLE VII--GENERAL PROVISIONS"

re = data_str.split(sub_str_End)
res_front =re[0]
re[1]
re[0]
# This cuts off the report After TITLE I
sub_str_Start = "TITLE I--AGRICULTURAL PROGRAMS"

re = res_front.split(sub_str_Start)
re[0]
re[1]
rept_body_dirty=re[1]
rept_body_no_lnbrk = rept_body_dirty.replace('\n', '')
import re

your_string = rept_body_no_lnbrk

#(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))

regex = r'(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))'

result = re.sub(regex, '', your_string)#.replace('\n', '')
result = result.replace(',,', '')
result = result.replace('COMMITTEE PROVISIONS', '\n\n\n\nCOMMITTEE PROVISIONS\n\n\n')
result = result.replace('$,', '')

print(result)

file=open('HR109-463-2007.txt','w')
file.writelines([result])

file.close()
result = result.replace(',,', '')
file=open('HR109-463-2007.txt','w')
file.writelines([result])


import csv
import glob

# This writes a CSV where the first column is the document name and the 
# Second column contains the text and "committee provisions"
with open('HR109-463-2007.csv', 'w', newline="", encoding="utf-16") as out_file:
    csv_out = csv.writer(out_file)
    csv_out.writerow(['filename', 'Content'])
    for result in glob.iglob('HR109-463-2007.txt'):
        with open(result, 'r') as txt:
            for line in txt.read().split('\n\n'):
                csv_out.writerow([result, line])
                
file.close()

import pandas as pd
 
# reading the CSV file
csvFile = pd.read_csv('HR109-463-2007.csv', sep = ".txt", encoding='utf-16')
 
# displaying the contents of the CSV file
print(csvFile)


#delete i
CF = csvFile.drop("HR109-463-2007")

CF['new'] = CF.index
#Creates duplicate of text line
CF['new2'] = CF.new

CF['agency'] = CF['new2'].str.split(",")


# this prints what I want for the first row, but I want it for all the rows 
# and to make it a new column
print(CF['agency'][0][0])


agency_name = []
for i in range(CF.shape[0]):
    agency_name.append(CF['agency'][i][0])
print(agency_name)


text = CF['new'].values.tolist()


df1 = pd.DataFrame (agency_name, columns = ['agency_name'])
df2 = pd.DataFrame (text, columns = ['text'])


dfTest = pd.concat([df1,df2], axis=1)



# write dataFrame to CSV file
dfTest.to_csv("/Users/aricaschuett/Documents/Alex/ArgReportsByAgency.csv")

# This leaves us with a csv file that needs more cleaning
# next, I will sort the columns by the agency or at least analyze them by the catyeory . 