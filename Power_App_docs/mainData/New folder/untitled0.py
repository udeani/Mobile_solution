# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 06:19:24 2021

@author: HENRY
"""
import mysql.connector
import pandas as pd
import pymysql
import os
import sqlite3


"""try:
    connect = mysql.connector.connect(host="localhost", user="tg", passwd="t")
    cursor = connect.cursor()
except:
    print("Error")
    
    
if connect:
    print("success")

        #uploading dss general info
        """
#___________________________________________________________________________________________
#def create_database(self):
try:
    database1 = "BU_info_DB"
    database2 = "SU_info_DB"
    database3 = "Staff_info_DB"
    database4 = "DSS_general_info_DB"
    database5 = "Customers_general_info_DB"
    database6 = "Customers_info_DB"
    database7 = "Meter_reading_DB"
    db_names = [database1, database2, database3, database4, database5, database6, database7]
    
    for DBs in db_names:
        #ql = ("CREATE DATABASE IF NOT EXISTS {}.db;".format(DBs))
        sqlite3.connect("{}.db".format(DBs))
        #sqlite3.execute(sql)
    print("success with db creation")
except:
    print("error creating DB")

#def file_upload(self):

directory = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/mainData/New folder"
