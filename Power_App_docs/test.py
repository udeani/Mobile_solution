# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 13:31:41 2021

@author: HENRY
"""
import pymysql# as mysql
import mysql.connector
import os
import pandas as pd
from datetime import timedelta
class MysqlDbCon:
    
    def __init__(self, host='localhost', user="tg", password="t", **args):
        try:
            db_connect = mysql.connector.connect(host=host,user=user,passwd=password)
            cursor = db_connect.cursor()
            self.cursor = cursor
            self.connect = db_connect
            print("Login Success")
            #cursor.execute("SELECT * FROM **")  # this is the variable that will check the user rank for his menu
        except:
            print("error") # to be edited later for kivy

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
            print("login success")
            
            for DBs in db_names:
                sql = ("CREATE DATABASE IF NOT EXISTS {};".format(DBs))
                self.cursor.execute(sql)
            print("success with db creation")
        except:
            print("error creating DB")

    #def file_upload(self):

        directory = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs"
        
        try:
            sql = " USE Customers_info_DB"
            self.cursor.execute(sql)
            
            for file in os.listdir(directory):
                if len(file) == 14:
                    sql = "CREATE TABLE IF NOT EXISTS `Customers_info_DB`.`{}` ( `id` INT(40) NOT NULL AUTO_INCREMENT , `type` VARCHAR(40) NOT NULL , `date` DATETIME NOT NULL , `amount` FLOAT(40) NOT NULL , `unit` FLOAT(40) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(file[:10])
                    #sql = ("CREATE TABLE IF NOT EXISTS {}(id int(20) NOT NULL AUTO_INCREMENT, type VARCHAR(20), date DATE(10), amount int(30), unit int(30), PRIMARY KEY (id));".format(file[:10]))
                    self.cursor.execute(sql)
        except:
            print("error creating table")
        
    #def pandas_write2sql(self):
        try:
            for file in os.listdir(directory):
                if len(file) == 14:
                    n = 0
                    open_file = pd.read_csv("{}".format(file))
                    print("file {} at number-{} uploading".format(file[:10], n))
                    #ids = open_data["0"]
                    types = open_file["Type"]
                    dates = open_file["Date"]
                    amount = open_file["Amount"]
                    unit = open_file["Unit"]
              
                    #n = 0
                    for item in unit:
                        sql = "INSERT INTO `customers_info_db`.`{}` (`id`, `type`, `date`, `amount`, `unit`) VALUES (NULL, '{}', '{}', '{}', '{}');".format(file[:10], types[n], dates[n], amount[n], unit[n])
                        self.cursor.execute(sql)
                        db_connect.commit()
                        n +=1
                    print("Success")
            print ("Success uploading all account table values")
                #open_file.to_sql("{}".format(file),db_connect)
        except:
            print("Can't write to sql")
 
        
 
    #def su_file_upload(self):
        #table creation
        try:
            sql = "CREATE TABLE IF NOT EXISTS `SU_info_DB`.`su_info`(`id` INT NOT NULL ATO_INCREMENT, `su_id` VARCHAR(40) NOT NULL, `su_name` VARCHAR(40) NOT NULL, `su_gps_coor` POINT NOT NULL, SPATIAL INDEX `SPATIAL` (`su_gps_coor`) `bu_id` VARCHAR(40) NOT NULL)"
            self.cursor.execute(sql)
            db_connect.commit()
            print ("su table creation successful")
        except:
            print("can not create su table")
            
        #file uploading    
        try:
            #os_dir = os.curdir
            # for su table
            dir = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/mainData"
            file = pd.read_csv(dir+"/"+"su_info.csv")
            su_id = file["su_id"]
            su_name = file["name"]
            su_gps_loc = file["gps loc"]
            bu_id = file["bu_id"]
            
            # converting gps coordinates(su_gps_loc) to integers without special characters
            char = ",]"
            space = " []"
            letters = '-+1234567890.'
            su_coor = []
            n = 0
            x = 0
            
            for num_words in su_gps_loc:
                cs = ""
                for strings in num_words:
                    if strings in letters:
                        cs = cs + strings
                    elif strings in char:
                        dx = float(cs)
                        su_coor.append(dx)
                        cs = ""
                    elif strings in space:
                        cs = ""
            #conversion ends here
            
            
            for file in su_name:
                sql = "INSERT INTO `SU_info_DB`.`su_info`(`su_id`, `su_name`, `su_gps_coor`, `bu_id`) VALUES ('{}', '{}', 'POINT({} {})', '{}')".format(su_id[n], name[n], su_coor[x], su_coor[x+1] , bu_id)# for su gps coor (POINT(40.71727401 -74.00898606))
                self.cursor.execute(sql)
                db_connect.commit()
                n +=1
                x +=1
        except:
            print("error uploading su info")
            
        # dss info table making
        try:
            sql = "CREATE TABLE IF NOT EXISTS `DSS_general_info_DB`.`dss_info`(`id` INT NOT NULL ATO_INCREMENT, `dss_id` VARCHAR(40) NOT NULL, `dss_name` VARCHAR(40) NOT NULL,`dss_address` VARCHAR(40) NOT NULL, `dss_gps_coor` POINT NOT NULL, SPATIAL INDEX `SPATIAL` (`dss_gps_coor`) `bu_id` VARCHAR(40) NOT NULL, `staff_id` VARCHAR(40) NOT NULL, `su_id` VARCHAR(40) NOT NULL,)"
            self.cursor.execute(sql)
            db_connect.commit()
            print ("dss general table creation successful")
        except:
            print("can not create dss general table")

        #uploading dss general info

                        
    def maintain_connection(self):
        pass

    def fetch_menu(self):
        # MysqlDbCon.sql =
        MysqlDbCon.cursor

    def log_out(self):
        MysqlDbCon.server.close()


    def CustomerInfo():
        pass

    def PaymentHistory():
        pass


    def MeterReading():
        pass

    def ReportIssue():
        pass

    def NewSetup():
        pass

    def DeliverBills():
        pass


db = MysqlDbCon()#host="localhost", user="ty", passwd="t")
#print(MysqlDbCon.server)
#print(MysqlDbCon.user)
#db.open_connection()
#db.create_database()
#db.file_upload()
