# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 06:19:24 2021

@author: HENRY
"""
import mysql.connector
import pandas as pd
import pymysql
import os


try:
    connect = mysql.connector.connect(host="localhost", user="tg", passwd="t")
    cursor = connect.cursor()
except:
    print("Error")
    
    
if connect:
    print("success")

        #uploading dss general info
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
        sql = ("CREATE DATABASE IF NOT EXISTS {};".format(DBs))
        #cursor.execute(sql)
    print("success with db creation")
except:
    print("error creating DB")

#def file_upload(self):

directory = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs"

try:
    sql = " USE Customers_info_DB"
    #cursor.execute(sql)
    
    for file in os.listdir(directory):
        if len(file) == 14:
            sql = "CREATE TABLE IF NOT EXISTS `Customers_info_DB`.`{}` ( `id` INT(40) NOT NULL AUTO_INCREMENT , `type` VARCHAR(40) NOT NULL , `date` DATETIME NOT NULL , `amount` FLOAT(40) NOT NULL , `unit` FLOAT(40) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;".format(file[:10])
            #sql = ("CREATE TABLE IF NOT EXISTS {}(id int(20) NOT NULL AUTO_INCREMENT, type VARCHAR(20), date DATE(10), amount int(30), unit int(30), PRIMARY KEY (id));".format(file[:10]))
            #cursor.execute(sql)
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
                #cursor.execute(sql)
                #connect.commit()
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
    #cursor.execute(sql)
    #connect.commit()
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
        #cursor.execute(sql)
        #connect.commit()
        n +=1
        x +=1
except:
    print("error uploading su info")
    
# dss info table making
try:
    sql = "CREATE TABLE IF NOT EXISTS `DSS_general_info_DB`.`dss_info`(`id` INT NOT NULL ATO_INCREMENT, `dss_id` VARCHAR(40) NOT NULL, `dss_name` VARCHAR(40) NOT NULL,`dss_address` VARCHAR(40) NOT NULL, `dss_gps_coor` POINT NOT NULL, SPATIAL INDEX `SPATIAL` (`dss_gps_coor`) `bu_id` VARCHAR(40) NOT NULL, `staff_id` VARCHAR(40) NOT NULL, `su_id` VARCHAR(40) NOT NULL,)"
    #cursor.execute(sql)
    #connect.commit()
    print ("dss general table creation successful")
except:
    print("can not create dss general table")
#________________________________________________________________________________________________________________________________

#try:
    #sql = "CREATE TABLE `DSS_general_info_DB`.`dss_info`(`id` IN(40) NOT NULL AUTO_INCREMENT, `dss_id` VARCHAR(40) NOT NULL, `dss_name` VARCHAR(40) NOT NULL,`dss_address` VARCHAR(40) NOT NULL, `dss_gps_coor` POINT(40) NOT NULL, `staff_id` VARCHAR(40) NOT NULL, `su_id` VARCHAR(40) NOT NULL, PRIMARY KEY (`id`)) ENGINE = InnoDB;" 
sql = "CREATE TABLE IF NOT EXISTS `dss_general_info_db`.`dss_info` ( `id` INT(40) NOT NULL AUTO_INCREMENT, `dss_id` VARCHAR(40) NOT NULL , `dss_name` VARCHAR(40) NOT NULL , `dss_address` VARCHAR(40) NOT NULL , `dss_gps_coor` POINT(40) NOT NULL , `staff_id` VARCHAR(40) NOT NULL , `su_id` VARCHAR(40) NOT NULL , PRIMARY KEY (`id`), SPATIAL INDEX `SPATIAL` (`dss_gps_coor`)) ENGINE = myISAM; "
cursor.execute(sql)
connect.commit()

print ("dss general table creation successful")
#except:
print("can not create dss general table")    

      
#file uploading    
#try:
    #os_dir = os.curdir
    # for dss table
dir = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs"
file = pd.read_csv(dir+"/"+"dss_general_info.csv")
file = pd.read_csv("C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/dss_general_info.csv")
dss_id = file["dss_id"]
dss_name = file["dss_name"]
dss_address = file["dss_address"]
dss_gps_loc = file["dss_loc"]
staff_id = file["staff_id"]
su_id = file["su_id"]

# converting gps coordinates(su_gps_loc) to integers without special characters
char = ",]"
space = " []"
letters = '-+1234567890.'
dss_coor = []
n = 0
x = 0

for num_words in dss_gps_loc:
    cs = ""
    for strings in num_words:
        if strings in letters:
            cs = cs + strings
        elif strings in char:
            dx = float(cs)
            dss_coor.append(dx)
            cs = ""
        elif strings in space:
            cs = ""
            
print(dss_coor)
#conversion ends here


for file in dss_id:
    sql = "INSERT INTO `DSS_general_info_DB`.`dss_info`(`id`, `dss_id`, `dss_name`, `dss_address`, `dss_gps_coor`, `staff_id`, `su_id`) VALUES (NULL, '{}', '{}', '{}', POINT({},{}),'{}', '{}')".format(dss_id[n], dss_name[n], dss_address[n], dss_coor[x], dss_coor[x+1], staff_id[n], su_id[n])# for su gps coor (POINT(40.71727401 -74.00898606))
    #sql = "INSERT INTO `DSS_general_info_DB`.`dss_info` (`id`, `dss_id`, `dss_name`, `dss_address`, `dss_gps_coor`, `staff_id`, `su_id`) VALUES (NULL, 'as23', 'thunder', ' iu9iueruer8iugeqiuqdiuhdqsuqd', '\'POINT(329.32423 32.485484848)\',0', 'r56', 's34')"
    #sql = "INSERT INTO `dss_info` (`id`, `dss_id`, `dss_name`, `dss_address`, `dss_gps_coor`, `staff_id`, `su_id`) VALUES (NULL, 'as23', 'thunder dss', '5 benin', '\'POINT(-12.456657 13.45655)\',0', 'r56', 's34')"
    #cursor.execute(sql)
    #connect.commit()
    n +=1
    x +=2
#except:
   #print("error uploading dss info")

# this section is to update the gps_coor(point) values which defaults to null after upload
x = 0
for item in dss_id:
    print (dss_coor[x], dss_coor[x+1], item)
    sql = """UPDATE `DSS_general_info_DB`.`dss_info`
            SET dss_gps_coor = ST_GeomFromText('POINT({} {})', 0)
            WHERE dss_id = '{}'""".format(dss_coor[x], dss_coor[x+1], item)
    #cursor.execute(sql)
    #connect.commit()
    x +=2

sql2 = "SELECT `dss_id` FROM `DSS_general_info_DB`.`dss_info` WHERE `dss_id` = 'A101'"
cor = cursor.execute(sql2)
print(cursor.fetchall())
print(f' this is {cor}')

sql = "SELECT `dss_id` FROM `DSS_general_info_DB`.`dss_info` WHERE ST_X(dss_gps_coor) = -77.27592"
cursor.execute(sql)
print(cursor.fetchall())
sql1 = "SELECT `dss_id` FROM `DSS_general_info_DB`.`dss_info` WHERE ST_Y(dss_gps_coor) = 108.11537" 
#`ST_Y(dss_gps_coor)` IS 'NULL'""" #OR ST_Y(coordinates) IS NULL;""" ST_AsText(ST_Y())
cor1 = cursor.execute(sql1)
print(cursor.fetchall())

sql = "SELECT ST_X(dss_gps_coor) FROM `DSS_general_info_DB`.`dss_info` WHERE `staff_id` = 7441"
cursor.execute(sql)
print(cursor.fetchall())


#_________________________________________________________
# for staff table
sql = """CREATE TABLE IF NOT EXISTS `staff_info_db`.`staff_table`
        (
        `id` INT(40) NOT NULL AUTO_INCREMENT,
        `staff_firstName` VARCHAR(40) NULL,
        `staff_lastName` VARCHAR(40) NULL,
        `staff_gender` CHAR(40) NULL,
        `staff_email` VARCHAR(60),
        `staff_phoneNo` VARCHAR(40)),
        `staff_address` VARCHAR(224),
        `staff_age` INT(3),
        `staff_id` VARCHAR(40) NOT NULL,
        `staff_rank` VARCHAR(40) NULL,
        `staff_bu` VARCHAR(40) NULL,
        `staff_su` VARCHAR(40) NULL,
        PRIMARY KEY (`id`)
        ) ENGINE = InnoDB;"""
#connect.commit()

#try:
staff_file = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/staff_table.csv"
file = pd.read_csv(staff_file)
staff_name_1 = file["First Name"]
staff_name_2 = file["Last Name"]
staff_gender = file["Gender"]
staff_email = file["Email"]
staff_phone = file["Phone"]
staff_address = file["Street Address"]
staff_age = file["Age"]
staff_id = file["staff_id"]
staff_rank = file["rank"]
staff_bu = file["bu_id"]
staff_su = file["su_id"]
n = 0
for file in staff_id:
    
    sql = """INSERT INTO `staff_info_db`.`staff_table`
    (`staff_firstName`, `staff_lastName`, `staff_gender`, `staff_email`, `staff_phoneNo`, `staff_address`, `staff_age`, `staff_id`, `staff_rank`, `staff_bu`, `staff_su`)
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}')""".format(staff_name_1[n], staff_name_2[n], staff_gender[n], staff_email[n], staff_phone[n], staff_address[n], staff_age[n], staff_id[n], staff_rank[n], staff_bu[n], staff_su[n])
    #cursor.execute(sql)
   #connect.commit()
    n +=1 

#except:
    #print("Error in staff tbale upload")
    
            
#______________________________________________________________________________________________________
# for bu table
sql = """CREATE TABLE IF NOT EXISTS `bu_info_db`.`bu_table`
        (`id` INT(40) NOT NULL AUTO_INCREMENT, `bu_name` VARCHAR(40) NOT NULL, `bu_id` VARCHAR(40) NOT NULL, `bu_gps_point` POINT(40) NOT NULL, PRIMARY KEY (`id`), SPATIAL INDEX `SPATIAL` (`bu_gps_point`)) ENGINE = myISAM"""
cursor.execute(sql)
connect.commit()


bu_table = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/bu_info.csv"
file = pd.read_csv(bu_table)
bu_name = file["name"]
bu_id = file["bu_id"]
bu_gps_coor = file["gps_loc"]
n = 0
x = 0
print(bu_name)

for file in range(2):
    sql = """INSERT INTO `bu_info_db`.`bu_table` (`bu_name`, `bu_id`, `bu_gps_point`)
        VALUES ('{}', '{}', POINT({}, {}))""".format(bu_name[n], bu_id[n], bu_gps_coor[x], bu_gps_coor[x+1])
    n +=1
    x +=2
    #cursor.execute(sql)
    #connect.commit()

sql = """SELECT *,ST_X(bu_gps_point) FROM `bu_info_db`.`bu_table` WHERE ST_Y(bu_gps_point) = -39.82472"""
cursor.execute(sql)
print (cursor.fetchall())



#_______________________________________________________________________________________________________________________________
#for su table

sql = """CREATE TABLE IF NOT EXISTS `su_info_db`.`su_table`
        (`id` INT(40) NOT NULL AUTO_INCREMENT, `su_name` VARCHAR(40) NOT NULL, `su_id` VARCHAR(40) NOT NULL, `bu_id` VARCHAR(40) NOT NULL, `su_gps_point` POINT(40) NOT NULL, PRIMARY KEY (`id`), SPATIAL INDEX `SPATIAL` (`su_gps_point`)) ENGINE = myISAM"""
cursor.execute(sql)
connect.commit()

su_table = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/mainData/su_info.csv"
file = pd.read_csv(su_table)
su_name = file["name"]
su_id = file["su_id"]
su_gps_coor = file["gps loc"]
bu_id = file["bu_id"]
n = 0
x = 0
print(su_name)

for file in range(2):
    sql = """INSERT INTO `su_info_db`.`su_table` (`su_name`, `su_id`, `bu_id`, `su_gps_point`)
        VALUES ('{}', '{}', '{}', POINT({}, {}))""".format(su_name[n], su_id[n], bu_id[n], su_gps_coor[x], su_gps_coor[x+1])
    n +=1
    x +=2
    #cursor.execute(sql)
    #connect.commit()



#___________________________________________________________________________________________________________________________________
#for total customer infomation upload:
#creating the table:

sql = """CREATE TABLE IF NOT EXISTS `customers_general_info_db`.`total_customer_table`
    (
    `id` INT(26) NOT NULL AUTO_INCREMENT,
    `cutomerFirstName` VARCHAR(60) NULL,
    `customerLastName` VARCHAR(60) NULL,
    `customerMiddleName` VARCHAR(60) NULL,
    `customerGender` VARCHAR(60) NULL,
    `customerAge` INT(3),
    `customerEmail` VARCHAR(60) NULL,
    `customerPhoneNo` VARCHAR(60) NOT NULL,
    `customerCity` VARCHAR(60) NOT NULL,
    `customerAdress` VARCHAR(60) NOT NULL,
    `customerGPSpoint` POINT(60) NOT NULL,
    `customerZIPcode` VARCHAR(60) NULL,
    `customerAccNO` INT(16) NOT NULL,
    `customerSetupDate` DATE NOT NULL,
    `customerBU` VARCHAR(14) NOT NULL,
    `customerSU` VARCHAR(14) NOT NULL,
    `customerMarketer` VARCHAR(14) NOT NULL,
    `customerAccMode` VARCHAR(26) NOT NULL,
    `customerAccType` INT(3) NOT NULL,
    `customerDSS` VARCHAR(14) NOT NULL,
    PRIMARY KEY (`id`),
    SPATIAL INDEX `SPATIAL` (`customerGPSpoint`)
    ) ENGINE = myISAM"""

cursor.execute(sql)

#uploading the files
#First Name  Last Name   Gender  Age Email   Phone   City    Street Address  LAT/LON Zip Code    Account Number  Date Opened BU_id   
#SU_id   staff_id    acc_Mode    acc_type    dss_id

dir_path = "C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/Total_cust_info_600.csv"
customers = pd.read_csv(dir_path)

firstname = customers["First Name"]
lastname = customers["Last Name"]
gneder = customers["Gender"]
age = customers["Age"]
email = customers["Email"]
phoneNo = customers["Phone"]
city = customers["City"]
address = customers["Street Address"]
geo_loc = customers["LAT/LON"]
zipcode = customers["Zip Code"]
acc = customers["Account Number"]
date = customers["Date Opened"]
bu = customers["BU_id"]
su = customers["SU_id"]
marketer = customers["staff_id"]
acc_mode = customers["acc_Mode"]
acc_type = customers["acc_type"]
dss_id = customers["dss_id"]


# converting gps coordinates(su_gps_loc) to integers without special characters

new_date = []       #*****************

for dates in date:
    onion = str(dates)
    onions = onion[:4]+"-"+onion[4:6]+"-"+onion[6:8]
    new_date.append(onions)

# converting gps coordinates(su_gps_loc) to integers without special characters
char = ","
space = " "
letters = '-1234567890.'
new_geo_loc = []        #******************

print(geo_loc[0])

for gps_points in geo_loc:
    cs = ""
    no = len(gps_points)
    n = 0

    for strings in gps_points:
        if strings in letters:
            cs = cs + strings
            n +=1
            if no == n:
                dx = float(cs)
                new_geo_loc.append(dx)
                cs = ""
        elif strings in char:
            dx = float(cs)
            new_geo_loc.append(dx)
            cs = ""
            n +=1
        elif strings in space:
            cs = ""
            n +=1
        elif no == n:
            dx = float(cs)
            new_geo_loc.append(dx)
            cs = ""


n = 0
x = 0

print(len(geo_loc))
print(len(new_date))
print(len(new_geo_loc))
print(len(firstname))
print(len(lastname))
print(len(gneder))
print(len(email))
print(len(age))
print(len(phoneNo))
print(len(city))
print(len(address))
print(len(zipcode))
print(len(acc))
print(len(bu))
print(len(su))
print(len(marketer))
print(len(acc_type))
print(len(dss_id))

print(new_geo_loc[0], new_geo_loc[1])

for accs in acc:
    sql = """ INSERT INTO `customers_general_info_db`.`total_customer_table`
        (
        `cutomerFirstName`,
        `customerLastName`,
        `customerGender`,
        `customerAge`,
        `customerEmail`,
        `customerPhoneNo`,
        `customerCity`,
        `customerAdress`,
        `customerGPSpoint`,
        `customerZIPcode`,
        `customerAccNO`,
        `customerSetupDate`,
        `customerBU`,
        `customerSU`,
        `customerMarketer`,
        `customerAccMode`,
        `customerAccType`,
        `customerDSS`) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', POINT({}, {}), '{}', {}, {}, '{}', '{}', '{}', '{}', {}, '{}'  )""".format(firstname[n], lastname[n], gneder[n], age[n], email[n], phoneNo[n], city[n], address[n], new_geo_loc[x], new_geo_loc[x+1], zipcode[n], acc[n], new_date[n], bu[n], su[n], marketer[n], acc_mode[n], acc_type[n], dss_id[n])
    #cursor.execute(sql)
    #connect.commit()
    n +=1
    x +=2
    #to avoid errors in string upload in db, always check that there is no quote ie ' within the string to avoid mysql syntax error

    sql = 'SELECT staff_rank FROM `staff_info_db`.`staff_table` WHERE staff_id = 1031'
    cursor.execute(sql)
    cursor.fetchall()