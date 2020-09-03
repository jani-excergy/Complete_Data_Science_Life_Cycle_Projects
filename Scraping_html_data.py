# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:01:04 2020

@author: Unify
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from Hours_to_Day import Day_values_2013,Day_values_2014,Day_values_2015,Day_values_2016,Day_values_2017,Day_values_2018
import sys
from bs4 import BeautifulSoup
import os
import csv


def html_scraping(month,year):
    
    # To scrap the data we need to give the path of flies
    file_path=open('Data_collection/Html_data/{}/{}.html'.format(year,month),'rb')
    
    #After scraping the data we need to store it in a variable
    
    Scaraped_data=file_path.read()
    
    # Now I create two empty lists for future purpose
    
    Sample_data=[]
    Finale_data=[]

    # Now I intialise the beautifulsoup class beautifulsoup(Scrapedtext,filetype)
    
    soup=BeautifulSoup(Scaraped_data,"lxml")
    
    # We need the table data from html so we loop through the table tag and it's class from scraped html data
    
    for table in soup.findAll('table',{'class':'medias mensuales numspan'}):
        
        # In table data we need body of the table to find the features so we loop through the table body
        
        for tbody in table:
            
            # In table body we need the rows to get features data so we loop through the table rows
            
            for tr in tbody:
                
                # Now we extract the row data 
                
                Extract_data=tr.get_text()
                
                # Now we append the row data into Sample_data list
                
                Sample_data.append(Extract_data)
                
                
    # If we manually check in the html we have 15 features so to check the if we are getting 15 features or not
    # No of row
    
    No_rows=len(Sample_data)/15
    
    
    # Now to get the feature values first we need to go through the rows so we loop through the rows
    for iterate in range(round(No_rows)):
        
        # Creating empty list store feature values of each rows
        
        lst=[]
        
        # we loop through the feature to get each value 
        
        for i in range(15):
            # we add the each row data in to empty lst
            
            
            lst.append(Sample_data[0])
            
            #Now we remove data from Sample_data
            
            Sample_data.pop(0)
            
        # Now we we add the each row values of 15 features in Finale list  
        
        Finale_data.append(lst)

    Length_Finale_data=len(Finale_data)
    
    Finale_data.pop(Length_Finale_data-1)
    Finale_data.pop(0)
    
    # Now we remove the empty features from table beacause this features doesn't contain any value
    
    for feature in range(len(Finale_data)):
        Finale_data[feature].pop(6)
        Finale_data[feature].pop(13)
        Finale_data[feature].pop(12)
        Finale_data[feature].pop(11)
        Finale_data[feature].pop(10)
        Finale_data[feature].pop(9)
        Finale_data[feature].pop(0)
        
    return Finale_data

# Once scrapiing the html table data
# html table features are independet variables
# Hours_to_Day PM2.5 feature is dependent features
# we need to combine both independent features and dependent features in csv file
# for that we write a data

def combine_dependent_independent(year, cs):
    for i in pd.read_csv('Data_collection/Html_scraping_data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=i)
        mylist = df.values.tolist()
    return mylist
        

if __name__=="__main__":
   
    # We need to create a directory to store the csv files 
    if not os.path.exists("Data_collection/Html_scraping_data"):
        os.makedirs("Data_collection/Html_scraping_data")
        
        
    # After creating directory we need to write the csv file 
    # we need years from 2013 t0 2018 so for that we create loop for year
    for year in range(2013,2019):
        final_data=[]
        with open ("Data_collection/Html_scraping_data/real_"+str(year)+".csv",'w') as csvfile:
            writting_csv=csv.writer(csvfile, dialect='excel')
            writting_csv.writerow(['T','TM','Tm','SLP','H','VV','V','VM','PM2.5'])
            
            
        # To add the data to the csv files we call the html_scraping function    
        for month in range(1,13):
            temp=html_scraping(month, year)
            final_data=final_data+temp
            
        # To get PM2.5 avg values we need to call the corresponding function 
        # For the we dinamically write it with getattr
        
        dependent=getattr(sys.modules[__name__], 'Day_values_{}'.format(year))()
        
        # To add the dependent feature PM2.5 to the independent features 
        for i in range(len(final_data)-1):
            final_data[i].insert(8,dependent[i])
            
        with open('Data_collection/Html_scraping_data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
                    
    # We call the combine_dependent_independent function to combine the both                 
    data_2013 = combine_dependent_independent(2013, 600)
    data_2014 = combine_dependent_independent(2014, 600)
    data_2015 = combine_dependent_independent(2015, 600)
    data_2016 = combine_dependent_independent(2016, 600)
    data_2017 = combine_dependent_independent(2017, 600)
    data_2018 = combine_dependent_independent(2018, 600)
    
    
    # combining the all years data into single csv
    total=data_2013+data_2014+data_2015+data_2016+data_2017+data_2018
    
    with open('Data_collection/Html_scraping_data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
df=pd.read_csv('Data/Real-Data/Real_Combine.csv')
                    
    
    
    
    
    