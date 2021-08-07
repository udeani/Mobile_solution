# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 19:18:26 2021

@author: HENRY
"""
###### data not generated for this excel was generated and downloaded from:
    ######http://randat.com/
    ######https://generatedata.com/
import random
import numpy as np
import pandas as pd

# Loading the csv file into console
data1 = pd.read_csv("C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/Bello Layout.csv")
data2 = pd.read_csv("C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/San Fransisco.csv")
data3 = pd.read_csv("C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/Sundrie.csv")

# Appending the three data  sets together to avoid multiple iterations on file
data4 = data1.append(data2)
data5 = data4.append(data3)

# Generating arange of random intergers from certian range to serve as acc numbers
np_acc_no = np.random.randint(1000000000, high=1200000000, size=600)
# Converting the certain intergers to dataframe
acc_no_series = pd.DataFrame(np_acc_no, columns=["Account Number"])


#________________________________________________________________________
""" Working on date
    a general date of 20120114 was chosen for easy iteration and calculation"""
gen_date = 20160114


date = []

# Appending the general date to a list of 600 items
for numbers in range(600):
    date.append(gen_date)

# Converting the list of 600 to pandas series    
date_open = pd.Series(date)

# Converting it back to dataframe for easy concatonation
date_open = pd.DataFrame(date_open, columns=["Date Opened"])

# Dropping the index(numbering) in the whole dataframse for homogeneraty
acc_no_series.reset_index(drop=True, inplace=True)
date_open.reset_index(drop=True, inplace=True)
data5.reset_index(drop=True, inplace=True)

# Appending the generated dataframse to a final data6
data6 = pd.concat([data5, acc_no_series, date_open], axis=1)#, join='left')

#_______________________________________________________________
bu = "B0109"

bu_ = []

# Appending the general bu code to a list of 600 items
for numbers in range(600):
    bu_.append(bu)

# Converting the list of 600 to pandas series    
bu_id = pd.Series(bu_)

# Converting it back to dataframe for easy concatonation
bu_id = pd.DataFrame(bu_id, columns=["BU_id"])

#_______________________________________________________________
#for two su id
su = ["S0023","S0012"]

su_ = []

# Appending the general bu code to a list of 600 items
for numbers in range(170):
    su_.append(su[0])
    
for numbers in range(430):
    su_.append(su[1])    
    
# Converting the list of 600 to pandas series    
su_id = pd.Series(su_)

# Converting it back to dataframe for easy concatonation
su_id = pd.DataFrame(su_id, columns=["SU_id"])

#_______________________________________________________________
# generating staff id for staff size of 12 (ie 2 su managers, 8 route marshals, and 1 HR)
staff_id = np.random.randint(0000, high=9999, size=12)
id_temp = staff_id

staff_id_ = []

for numbers in range(60):
    staff_id_.append(staff_id[0])

for numbers in range(20):
    staff_id_.append(staff_id[1])

for numbers in range(90):
    staff_id_.append(staff_id[2])

for numbers in range(150):
    staff_id_.append(staff_id[3])

for numbers in range(80):
    staff_id_.append(staff_id[4])
    
for numbers in range(45):
    staff_id_.append(staff_id[5])

for numbers in range(76):
    staff_id_.append(staff_id[6])

for numbers in range(79):
    staff_id_.append(staff_id[7])
    
# Converting the list of 600 to pandas series    
staff_id = pd.Series(staff_id_)

# Converting it back to dataframe for easy concatonation
staff_id = pd.DataFrame(staff_id, columns=["staff_id"])
    
#_______________________________________________________________
#generating dss serial ]|identifer for 15 dss
dss_id = ["A101","A102","A103","A104","A105","A106","A107","A108","A109","A110","A111","A112","A113","A114","A115"]

dss_id_ = []

for numbers in range(32):
    dss_id_.append(dss_id[0])
    
for numbers in range(28):
    dss_id_.append(dss_id[1])
    
for numbers in range(20):
    dss_id_.append(dss_id[2])
    
for numbers in range(49):
    dss_id_.append(dss_id[3])

for numbers in range(41):
    dss_id_.append(dss_id[4])
    
for numbers in range(73):
    dss_id_.append(dss_id[5])
    
for numbers in range(22):
    dss_id_.append(dss_id[6])
    
for numbers in range(26):
    dss_id_.append(dss_id[7])
    
for numbers in range(29):
    dss_id_.append(dss_id[8])
    
for numbers in range(80):
    dss_id_.append(dss_id[9])
    
for numbers in range(20):
    dss_id_.append(dss_id[10])
    
for numbers in range(25):
    dss_id_.append(dss_id[11])
    
for numbers in range(76):
    dss_id_.append(dss_id[12])
    
for numbers in range(31):
    dss_id_.append(dss_id[13])
    
for numbers in range(48):
    dss_id_.append(dss_id[14])
    
# Converting the list of 600 to pandas series    
dss_id = pd.Series(dss_id_)

# Converting it back to dataframe for easy concatonation
dss_id = pd.DataFrame(dss_id, columns=["dss_id"])

#______________________________________________________________
# account mode active|inactive
mode = "active"

mode_ = []

for numbers in range(600):
    mode_.append(mode)
    
mode = pd.Series(mode_)

mode = pd.DataFrame(mode, columns=["acc_Mode"])

#______________________________________________________________
# account type 1|post paid, 2|prepaid
acc_type_ = []

for numbers in range(600):
    acc_type_.append(random.randint(1,2))
    
acc_type = pd.Series(acc_type_)

acc_type = pd.DataFrame(acc_type, columns=["acc_type"])

#______________________________________________________________
# appending the whole data to one dataframe
data6 = pd.concat([data6, bu_id, su_id, staff_id, mode, acc_type, dss_id], axis=1)
print(data6.shape)

#______________________________________________________________
# Saving to file
data6.to_csv("Total_cust_info_600.csv")

    