#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:28:50 2022

@author: aricaschuett
"""


# This scrapes the argriculture subcommitte Bills and puts them in a csv
import requests
import os
from bs4 import BeautifulSoup

os.chdir('/Users/aricaschuett/Documents/Alex')

## Create list of URls
import pandas
ReportCSV = pandas.read_csv('/Users/aricaschuett/Documents/Alex/committee reports - Appropriations-RowsDropped.csv')

URLs = ReportCSV['URL'].to_list()

## Loop over all URLs
data = []
data_clean = ""
provision = []
agency = []

# name the output file to write to local disk
out_filename = "AppropriationReports.csv"
# header of csv file to be written
headers = "Report_Text,\n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

for URL in URLs:

    r = requests.get(URL)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(soup.prettify())

    s = soup.find('div', {"class": "main-wrapper"})
    data_str = str(s)

    #checks that the file is cleaned the same way as the origional
    file=open('newData','w')
    file.writelines([ data_str])
    file.close()

    # initializing sub string --- This cuts off the report after TITLE VII
    sub_str_End = "GENERAL PROVISIONS"

    re = data_str.split(sub_str_End)
    res_front =re[0]
    # This cuts off the report After TITLE I
    #sub_str_Start = "TITLE I--AGRICULTURAL PROGRAMS"
    sub_str_Start = "TITLE I"

    re = res_front.split(sub_str_Start)


    rept_body_dirty=re[1:4]      # 1:4 is hardcoded I may need to modify this

    re_str = ""
    re_str = ''.join(map(str, rept_body_dirty))

    import re
    re_str_no_lnbrk = re_str.replace('\n', '')

    your_string = re_str_no_lnbrk

    regex = r'(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))'

    result = re.sub(regex, '', your_string)#.replace('\n', '')
    result = result.replace(',,', '')
    result = result.replace('COMMITTEE PROVISIONS', 'COMMITTEE PROVISIONS\n')
    result = result.replace('$,', '')
    result = result.replace('$', '')
    result = result.replace(',,', '')
    sub_result_end = "          "
    re = result.split(sub_result_end)

    # Remove emtpy rows and rows that are not Committee provisions
    re = list(filter(None, re))
    re = [k for k in re if 'COMMITTEE PROVISIONS' in k] 



    import pandas as pd


    split = "\n"
    text = []

    for i in re:
        text.append(i.split(split))

    for i in text:
        provision.append(i[1])

    prov_split = []
    agency_name =[]
    for i in provision:
        prov_split.append(i.split(","))

    for i in prov_split:
        agency_name.append(i[0])

    # create a df for provision
    provisionDF = pd.DataFrame(provision, columns = ['provision'])
    agencyDF = pd.DataFrame(agency_name, columns = ['agency_name'])


    df_clean = pd.concat([agencyDF,provisionDF], axis=1)
    

# write dataFrame to SalesRecords CSV file
df_clean.to_csv("/Users/aricaschuett/Documents/Alex/AllArgReports.csv")
