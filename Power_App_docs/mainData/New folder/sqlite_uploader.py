# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 06:19:24 2021

@author: HENRY
"""
import pandas as pd
import os
import sqlite3

#___________________________________________________________________________________________

directory = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/mainData/New folder"

con = sqlite3.connect("Power_App_DB.db")

cur = con.cursor()

