# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 20:07:48 2021

@author: HENRY
"""
import pandas as pd

bu = "B0109"
bu_ = []
# Appending the general bu code to a list of 600 items
for numbers in range(2):
    bu_.append(bu)
su_info = pd.DataFrame({"su_id": ["S0023","S0012"], "name": ["Greenland", "West Land"], "gps loc": [[-21.11854, 88.17881],[-72.363, 82.52391]], "bu_id": bu_})
su_info.to_csv("su_info.csv")
