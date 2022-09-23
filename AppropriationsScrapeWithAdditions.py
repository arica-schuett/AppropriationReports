#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 16:00:53 2022

@author: aricaschuett
"""

# This scrapes the argriculture subcommitte Bills and puts them in a csv
import requests
import os
from bs4 import BeautifulSoup

os.chdir('/Users/aricaschuett/Documents/Alex')

## Create list of URls
import pandas
ReportCSV = pandas.read_csv('committee reports - loop tester.csv')

URLs = ReportCSV['URL'].to_list()

## Loop over all URLs
data = []
data_clean = []

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


    #my_table = soup.find_all(soup.title)       # this finds the titles of each report
    my_table = soup.find_all('div', {"class": "main-wrapper"})

    
    for tag in my_table:
        data.append(tag.get_text())
        
        # prints the dataset to console
        #print("Report_Text: " + data[0] + "\n")

        # writes the dataset to file
        f.write(data[0] + "\n")
        
        for i in data:
            data_str = i
            # initializing sub string --- This cuts off the report after TITLE VII
            sub_str_End = "GENERAL PROVISIONS"
        
            n = data_str.split(sub_str_End)
            res_front =n[0]
        
            # This cuts off the report After TITLE I
            sub_str_Start = "TITLE I"
        
            res_front.replace('\n', ' ')
        
            n = res_front.split(sub_str_Start)
            
            
            your_string =  ' '.join(map(str, n[1:4]))
            import re

            #(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))

            regex = r'(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))'

            result = re.sub(regex, '', your_string)
            result = result.replace(',,', '')
            result = result.replace('COMMITTEE PROVISIONS', '\n\n\n\nCOMMITTEE PROVISIONS\n\n\n')
            result = result.replace('$,', '')
            result = result.replace('$', '')


            data_clean.append(result)
 
 

            your_string = rept_body_no_lnbrk
        
            #(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))
        
            regex = r'(((2006 appropriation)\.*\s*\$\d*\,\d*\,\d*|\s2007 budget estimate\.*\s*.|\d*))'
        
            result = re.sub(regex, '', your_string)#.replace('\n', '')
            result = result.replace(',,', '')
            result = result.replace('COMMITTEE PROVISIONS', '\n\n\n\nCOMMITTEE PROVISIONS\n\n\n')
            result = result.replace('$,', '')
            
            
            
            
            
            
            
            data_clean.append(result)