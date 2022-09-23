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
        


with open('HouseAppropriationsReports.txt','w') as file_list:
    for rept in data:
        file_list.write(data[1])
