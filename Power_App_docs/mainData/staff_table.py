# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 19:33:01 2021

@author: HENRY
"""
import random
import numpy as np
import pandas as pd


main_data = pd.read_csv("C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/Total_cust_info_600.csv")


# temp = main_data.loc[0:14] i.e copying random name from my gen documents
temp_data = main_data[["First Name", "Last Name", "Gender", "Email", "Age", "Phone", "Street Address",]][0:12]

staff_id = [5060,6110,573,7441,6013,2520,1031,6566,5250,760,4859,9634]

su_id = ["S0023","S0012"]
su_id_ = []

for item in range(3):
    su_id_.append(su_id[0])
for item in range(5):
    su_id_.append(su_id[1])
for items in range(4):
    su_id_.append("")
    
bu = "B0109"
bu_ = []
# Appending the general bu code to a list of 600 items
for numbers in range(12):
    bu_.append(bu)
    
rank = ["Route Marshal", "Service Manager", "Human Resources", "Data Analyst"]
rank_ = []
for no in range(8):
    rank_.append(rank[0])
for no in range(2):
    rank_.append(rank[1])
for no in range(1):
    rank_.append(rank[2])
for no in range(1):
    rank_.append(rank[3])
    
staff_table = pd.concat([temp_data,pd.DataFrame({"staff_id": staff_id, "rank": rank_, "bu_id": bu_, "su_id": su_id_})],axis=1)
staff_table.to_csv("staff_table.csv")