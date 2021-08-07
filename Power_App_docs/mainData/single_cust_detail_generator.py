# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 19:18:26 2021

@author: HENRY
"""
from datetime import datetime, timedelta, time, date
import random
import numpy as np
import pandas as pd

# importing initial generated data
main_data = pd.read_csv("C:/Users/HENRY/Documents/Python Scripts/BEDC/Power_App/Power_App_docs/Total_cust_info_600.csv")
# seperating the imported data into two for iteration. this is to get acc type as a series and to get acc number as a series also
acc_type = main_data["acc_type"]
acc_no = main_data["Account Number"] 

#_____________________________________________________________
# Data for prepaid accounts
Transaction_type = ["Vend"] * 73

# general date
date = [20160114093312]
n = len(date)-1
m = 10000000000

# calculating the date for all vending type of acc (date of vend)
for years in range(6):
    for months in range(11):
        date_nw = date[n] + 100000000
        date.append(date_nw)
        n +=1
    date_nw = date[0] + m
    date.append(date_nw)
    m +=10000000000
    n +=1
# for mysql does not accept date format in plain int. this iteration below has to be done to add date char.
vend_date = []
for dates in date:
    onion = str(dates)
    onions = onion[:4]+"-"+onion[4:6]+"-"+onion[6:8]+" "+onion[8:10]+":"+onion[10:12]+":"+onion[12:14]
    vend_date.append(onions)
    
# function to generate unique amount for all account when its called
def amount_generator():      
    return np.random.randint(2000, high=100000, size=73)

prepaid_amount = amount_generator()
# general tariff to divide the amount for the unit vend
tariff = 40

# dividing the generated amount by the amount generated func.
# generating a list function that will generate fresh amount for bill and payment and append them to a list of 146
def unit_maker():
    unit_61 = []
    for rand_amount in prepaid_amount:
        unit_61.append(rand_amount/tariff)
    return unit_61

unit_61 = unit_maker()

#_____________________________________________________________
# Data for postpaid customers   
Transaction_type_2 = ["Billed", "Payment"]

# generating a 146 list of transaction type by: billed and payment
postpaid_trans_type = []
for item in range(73):
    postpaid_trans_type.append(Transaction_type_2[0])
    postpaid_trans_type.append(Transaction_type_2[1])

# generating a payment date thats different from billed date. billed date = vend date
date_2 = [20160126110423]
n_2 = len(date_2)-1
m_2 = 10000000000
print("working....")
for years in range(6):
    for months in range(11):
        date_nw = date_2[n_2] + 100000000
        date_2.append(date_nw)
        n_2 +=1
    date_nw = date_2[0] + m_2
    date_2.append(date_nw)
    m_2 +=10000000000
    n_2 +=1

# for mysql does not accept date format in plain int. this iteration below has to be done to add date char.
payment_date = []
for dates in date_2:
    onion = str(dates)
    onions = onion[:4]+"-"+onion[4:6]+"-"+onion[6:8]+" "+onion[8:10]+":"+onion[10:12]+":"+onion[12:14]
    payment_date.append(onions)

# appending the payment date and the billed date together
postpaid_date = []
for x in range(73):
    postpaid_date.append(vend_date[x])
    postpaid_date.append(payment_date[x])
print (postpaid_date)
#generating a random payment and billed amount together in a function
def amount_generator1(typ):
    if typ == 1:
        return np.random.randint(2000, high=100000, size=73)
    if typ == 2:
        return np.random.randint(-100000, high=-2000, size=73)

# The idea of a func for amounts is for easy refresh and generating unique numbers for each acc
# generating a list function that will generate fresh amount for bill and payment and append them to a list of 146
def postpaid_amounter():
    postpaid_amount = []
    for x in range(73):
        postpaid_amount.append(amount_generator1(1)[x])
        postpaid_amount.append(amount_generator1(2)[x])
    return postpaid_amount

# calling the function to have the data on a variable
postpaid_amountBP = postpaid_amounter()


# using old tariff for prepaid
# to make the tariff unique to each amount, a function is made out of it
def unit_maker1():
    unit_146 = []
    for rand_amount in postpaid_amountBP:
        if rand_amount <= 0:
            unit_146.append("")
        else:
            unit_146.append(rand_amount/tariff)
    return unit_146

unit_146 = unit_maker1()

#postpaid_unit = []
#for units in unit146:
    #postpaid_unit.append(unit_146[units])
    #postpaid_unit.append("")
    
       
#____________________________________________________________
# account type 1|post paid, 2|prepaid
n = 0
for accounts in acc_no:
    if acc_type[n] == 1:
        accounts = pd.DataFrame({"Type": Transaction_type, "Date": vend_date, "Amount": prepaid_amount,"Unit": unit_61 })
        accounts.to_csv(f'{acc_no[n]}.csv')
        prepaid_amount = amount_generator()
        unit_61 = unit_maker()
        n += 1
        
    elif acc_type[n] == 2:
        accounts = pd.DataFrame({"Type": postpaid_trans_type, "Date": postpaid_date, "Amount": postpaid_amountBP,"Unit": unit_146 })
        accounts.to_csv(f'{acc_no[n]}.csv')
        postpaid_amountBP = postpaid_amounter()
        unit_146 = unit_maker1()
        n += 1
    