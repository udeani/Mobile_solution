# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:18:40 2021

@author: HENRY
"""
import random
import numpy as np
import pandas as pd


dss_serial = ["A101","A102","A103","A104","A105","A106","A107","A108","A109","A110","A111","A112","A113","A114","A115"]
dss_name = ["Safe Heaven", "Courage Close","Mauris Ave", "Eros Road", "Nec Avenue", "Tellus Road", "Lectus Street", "Rimbey", "Morbi Close", "Quis Street","Cras Ave", "Commodo Road", "Ladan Crescent","Libero Ave", "Bolano Way"]

dss_address = ["622-5795 Luctus, Ave", "Ap #907-8812 Sed St.","9453 Suspendisse Ave","6802 Non Street","358-6095 Eu, Avenue","3979 Vehicula Ave","1016 Lacinia Avenue","210-5822 Auctor St.","8878 Natoque St.","2454 Mauris. Avenue","Ap #921-2942 In, St.","750-9422 Pellentesque Av","P.O. Box 479, 6345 Aliquet Street","409-9460 Aenean Ave","Ap #107-9743 Faucibus Ave"]
dss_loc = [[61.74799, -88.02611], [-15.93638, 150.43514], [54.61332, -72.94483], [61.81387, 117.05839], [-20.24052, -125.94663], [-81.27152, -152.52305], [-30.05637, 81.58996], [-43.30233, 87.92463], [-14.79259, -13.23224], [74.71732, 20.30435], [-2.79214, -168.87808], [27.39991, 108.11537], [-77.27592, 12.22097], [-12.06512, -32.37299], [27.39487, -145.79505]]

staff_id = [5060,6110,573,7441,6013,2520,1031,6566,5250,760,4859,9634]

su_id = ["S0023","S0012"]
su_id_ = []

for item in range(5):
    su_id_.append(su_id[0])
for item in range(10):
    su_id_.append(su_id[1])
    
staff_id_ = []
for items in range(1):
    staff_id_.append(staff_id[0])
    staff_id_.append(staff_id[0])
    staff_id_.append(staff_id[1])
    staff_id_.append(staff_id[2])
    staff_id_.append(staff_id[2])
    staff_id_.append(staff_id[3])
    staff_id_.append(staff_id[3])
    staff_id_.append(staff_id[3])
    staff_id_.append(staff_id[3])
    staff_id_.append(staff_id[4])
    staff_id_.append(staff_id[5])
    staff_id_.append(staff_id[5])
    staff_id_.append(staff_id[6])
    staff_id_.append(staff_id[7])
    staff_id_.append(staff_id[7])
  
dss_general_info = pd.DataFrame({"dss_id":dss_serial, "dss_name":dss_name, "dss_address":dss_address, "dss_loc":dss_loc, "staff_id":staff_id_, "su_id":su_id_})
dss_general_info.to_csv("dss_general_info.csv")